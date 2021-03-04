from dataclasses import dataclass
from typing import Optional, List, Dict

import requests
import yaml
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

class LGTMRequestException(Exception):
    pass


@dataclass
class LGTMSite:
    nonce: str
    long_session: str
    short_session: str
    api_version: str

    def _cookies(self):
        return {
            'lgtm_long_session': self.long_session,
            'lgtm_short_session': self.short_session
        }

    def _headers(self):
        return {
            'LGTM-Nonce': self.nonce
        }

    def _make_lgtm_get(self, url: str) -> dict:
        r = requests.get(
            url,
            cookies=self._cookies(),
            headers=self._headers()
        )
        return r.json()

    def get_my_projects(self) -> List[dict]:
        '''
        Returns a user's followed projects that are not in a custom list.

                Returns:
                        data (List[dict]): Response data from LGTM
        '''

        url = 'https://lgtm.com/internal_api/v0.2/getMyProjects?apiVersion=' + self.api_version
        data = self._make_lgtm_get(url)
        if data['status'] == 'success':
            return data['data']
        else:
            raise LGTMRequestException('LGTM GET request failed with response: %s' % str(data))

    def get_my_projects_under_org(self, org: str) -> List['SimpleProject']:
        '''
        Given an org name, returns a user's projects that are part of an org.

                Parameters:
                        org (str): An organization

                Returns:
                        projects (['SimpleProject']): List of SimpleProject's from LGTM part of an org.
        '''

        projects_sorted = LGTMDataFilters.org_to_ids(self.get_my_projects())
        return LGTMDataFilters.extract_project_under_org(org, projects_sorted)

    def _make_lgtm_post(self, url: str, data: dict) -> dict:
        '''
        Makes a HTTP post request to LGTM.com

                Parameters:
                        url (str): A URL representing where the HTTP request goes
                        data (dict): Data that will be sent to LGTM.com in the request..

                Returns:
                        data (dict): Data returned from LGTM.com response.
        '''

        api_data = {
            'apiVersion': self.api_version
        }
        full_data = {**api_data, **data}

        session = requests.Session()

        retries = Retry(total=3,
            backoff_factor=0.1,
            status_forcelist=[ 500, 502, 503, 504 ])

        session.mount('https://', HTTPAdapter(max_retries=retries))

        r = session.post(
            url,
            full_data,
            cookies=self._cookies(),
            headers=self._headers()
        )

        try:
            data_returned = r.json()
        except ValueError as e:
            response_text = r.text
            raise LGTMRequestException(f'Failed to parse JSON. Response was: {response_text}') from e

        if data_returned['status'] == 'success':
            if 'data' in data_returned:
                return data_returned['data']
            else:
                return {}
        else:
            raise LGTMRequestException('LGTM POST request failed with response: %s' % str(data_returned))

    def load_into_project_list(self, into_project: int, lgtm_project_ids: List[str]):
        '''
        Given a project list id and a list of project ids, add the projects to the project list on LGTM.com.

                Parameters:
                        into_project (int): Project list id
                        lgtm_project_ids (List[str]): List of project ids
        '''

        url = "https://lgtm.com/internal_api/v0.2/updateProjectSelection"
        # Because LGTM uses some wacky format for it's application/x-www-form-urlencoded data
        list_serialized = ', '.join([('"' + str(elem) + '"') for elem in lgtm_project_ids])
        data = {
            'projectSelectionId': into_project,
            'addedProjects': '[' + list_serialized + ']',
            'removedProjects': '[]',
        }
        self._make_lgtm_post(url, data)

    def force_rebuild_all_proto_projects(self):
        org_to_projects = LGTMDataFilters.org_to_ids(self.get_my_projects())
        for org in org_to_projects:
            for project in org_to_projects[org]:
                if not project.is_protoproject():
                    continue
                self.force_rebuild_project(project)

    def force_rebuild_project(self, simple_project: 'SimpleProject'):
        url = 'https://lgtm.com/internal_api/v0.2/rebuildProtoproject'
        data = {
            **simple_project.make_post_data(),
            'config': ''
        }
        try:
            self._make_lgtm_post(url, data)
        except LGTMRequestException:
            print('Failed rebuilding project. This may be because it is already being built. `%s`' % simple_project)

    def follow_repository(self, repository_url: str) -> dict:
        url = "https://lgtm.com/internal_api/v0.2/followProject"
        data = {
            'url': repository_url,
            'apiVersion': self.api_version
        }
        return self._make_lgtm_post(url, data)

    def unfollow_repository_by_id(self, project_id: str):
        '''
        Given a project id, unfollows a repository.

                Parameters:
                        project_id (str): A project id
        '''

        url = "https://lgtm.com/internal_api/v0.2/unfollowProject"
        data = {
            'project_key': project_id,
        }
        self._make_lgtm_post(url, data)

    def unfollow_proto_repository_by_id(self, project_id: str):
        '''
        Given a project id, unfollows the proto repository.

                Parameters:
                        project_id (str): A project id
        '''

        url = "https://lgtm.com/internal_api/v0.2/unfollowProtoproject"
        data = {
            'protoproject_key': project_id,
        }
        self._make_lgtm_post(url, data)

    def unfollow_repository(self, simple_project: 'SimpleProject'):
        url = "https://lgtm.com/internal_api/v0.2/unfollowProject" if not simple_project.is_protoproject() \
            else "https://lgtm.com/internal_api/v0.2/unfollowProtoproject"
        data = simple_project.make_post_data()
        self._make_lgtm_post(url, data)

    def unfollow_repository_by_org(self, org: str, include_protoproject: bool = False):
        projects_under_org = self.get_my_projects_under_org(org)
        for project in projects_under_org:
            if not include_protoproject and project.is_protoproject():
                print("Not unfollowing project since it is a protoproject. %s" % project)
                continue
            print('Unfollowing project %s' % project.display_name)
            self.unfollow_repository(project)

    def get_project_lists(self):
        url = 'https://lgtm.com/internal_api/v0.2/getUsedProjectSelections'
        return self._make_lgtm_post(url, {})

    def get_project_list_by_name(self, list_name: str) -> Optional[int]:
        project_lists = self.get_project_lists()
        for project_list in project_lists:
            if project_list['name'] == list_name:
                return int(project_list['key'])
        return None

    def get_or_create_project_list(self, list_name: str) -> int:
        project_list_id = self.get_project_list_by_name(list_name)
        if project_list_id is not None:
            print('Found Project List with name: %s' % list_name)
        else:
            print('Creating Project List with name: %s' % list_name)
            project_list_id = self.create_project_list(list_name)
        return project_list_id

    def create_project_list(self, name: str) -> int:
        """
        :param name: Name of the project list to create.
        :return: The key id for this project.
        """
        url = 'https://lgtm.com/internal_api/v0.2/createProjectSelection'
        data = {
            'name': name
        }
        response = self._make_lgtm_post(url, data)
        return int(response['key'])

    def add_org_to_project_list_by_list_key(self, org: str, project_list_key: int):
        projects_under_org = self.get_my_projects_under_org(org)
        ids = []
        for project in projects_under_org:
            print('Adding `%s` project to project list' % project.display_name)
            ids.append(project.key)
        self.load_into_project_list(project_list_key, ids)

    def add_org_to_project_list_by_list_name(self, org: str, project_name: str):
        pass

    @staticmethod
    def retrieve_project(gh_project_path: str):
        url = "https://lgtm.com/api/v1.0/projects/g/" + gh_project_path

        session = requests.Session()

        retries = Retry(total=3,
            backoff_factor=0.1,
            status_forcelist=[ 500, 502, 503, 504 ])

        session.mount('https://', HTTPAdapter(max_retries=retries))

        r = session.get(url)
        return r.json()

    @staticmethod
    def retrieve_project_id(gh_project_path: str) -> Optional[int]:
        data_returned = LGTMSite.retrieve_project(gh_project_path)
        if 'id' in data_returned:
            return int(data_returned["id"])
        else:
            return None

    @staticmethod
    def create_from_file() -> 'LGTMSite':
        with open("config.yml") as config_file:
            config = yaml.safe_load(config_file)
            lgtm: dict = config['lgtm']
            return LGTMSite(
                nonce=lgtm['nonce'],
                long_session=lgtm['long_session'],
                short_session=lgtm['short_session'],
                api_version=lgtm['api_version'],
            )


@dataclass
# TODO: this SimpleProject is no longer 'simple'. Some refactoring here could be nice.
class SimpleProject:
    display_name: str
    key: str
    project_type: str
    is_valid_project: bool
    org: str
    state: str

    def make_post_data(self):
        data_dict_key = 'protoproject_key' if self.is_protoproject() else 'project_key'
        return {
            data_dict_key: self.key
        }

    def is_protoproject(self):
        # The values for project_type should be hardcoded in one central location
        return self.project_type == "protoproject"

class LGTMDataFilters:

    @staticmethod
    def org_to_ids(projects: List[Dict]) -> Dict[str, List[SimpleProject]]:
        """
        Converts the output from :func:`~lgtm.LGTMSite.get_my_projects` into a dic of GH org
        to list of projects including their GH id and LGTM id.
        """
        org_to_ids = {}
        for project in projects:
            simple_project = LGTMDataFilters.build_simple_project(project)
            if not simple_project.is_valid_project:
                continue

            ids_list: List[SimpleProject]
            if simple_project.org in org_to_ids:
                ids_list = org_to_ids[simple_project.org]
            else:
                ids_list = []
                org_to_ids[simple_project.org] = ids_list
            ids_list.append(simple_project)

        return org_to_ids

    @staticmethod
    def extract_project_under_org(org: str, projects_sorted: Dict[str, List[SimpleProject]]) -> List[SimpleProject]:
        if org not in projects_sorted:
            print('org %s not found in projects list' % org)
            return []
        return projects_sorted[org]

    @staticmethod
    def build_simple_project(project: dict) -> SimpleProject:
        org: str
        display_name: str
        key: str
        project_type: str
        is_valid_project: bool = True
        state: str = ""

        if 'protoproject' in project:
            the_project = project['protoproject']
            if 'https://github.com/' not in the_project['cloneUrl']:
                # Not really concerned with BitBucket right now
                is_valid_project = False
            display_name = the_project['displayName']
            state = the_project['state']
            org = display_name.split('/')[0]
            key = the_project['key']
            project_type = 'protoproject'
        elif 'realProject' in project:
            the_project = project['realProject'][0]
            if the_project['repoProvider'] != 'github_apps':
                # Not really concerned with BitBucket right now
                is_valid_project = False
            org = str(the_project['slug']).split('/')[1]
            display_name = the_project['displayName']
            key = the_project['key']
            project_type = "realProject"
        else:
            # We raise this in cases where we can't intrepret the data we get
            # back from LGTM.
            is_valid_project = False

        return SimpleProject(
            display_name=display_name,
            key=key,
            project_type=project_type,
            is_valid_project=is_valid_project,
            org=org,
            state=state
        )
