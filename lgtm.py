from dataclasses import dataclass
from typing import Optional, List, Dict

import requests
import yaml


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
        url = 'https://lgtm.com/internal_api/v0.2/getMyProjects?apiVersion=' + self.api_version
        data = self._make_lgtm_get(url)
        if data['status'] == 'success':
            return data['data']
        else:
            raise Exception('LGTM GET request failed with response: %s' % str(data))

    def _make_lgtm_post(self, url: str, data: dict) -> dict:
        api_data = {
            'apiVersion': self.api_version
        }
        full_data = {**api_data, **data}
        print(data)
        r = requests.post(
            url,
            full_data,
            cookies=self._cookies(),
            headers=self._headers()
        )
        data_returned = r.json()
        print(data_returned)
        return data_returned

    def load_into_project_list(self, into_project: int, lgtm_project_ids: List[str]):
        url = "https://lgtm.com/internal_api/v0.2/updateProjectSelection"
        # Because LGTM uses some wacky format for it's application/x-www-form-urlencoded data
        list_serialized = ', '.join([('"' + elem + '"') for elem in lgtm_project_ids])
        data = {
            'projectSelectionId': into_project,
            'addedProjects': '[' + list_serialized + ']',
            'removedProjects': '[]',
        }
        self._make_lgtm_post(url, data)

    def follow_repository(self, repository_url: str):
        url = "https://lgtm.com/internal_api/v0.2/followProject"
        data = {
            'url': repository_url,
            'apiVersion': self.api_version
        }
        self._make_lgtm_post(url, data)

    def unfollow_repository_by_id(self, project_id: int):
        url = "https://lgtm.com/internal_api/v0.2/unfollowProject"
        data = {
            'project_key': project_id,
            'apiVersion': self.api_version
        }
        self._make_lgtm_post(url, data)

    @staticmethod
    def retrieve_project_id(gh_project_path: str) -> Optional[int]:
        url = "https://lgtm.com/api/v1.0/projects/g/" + gh_project_path
        r = requests.get(url)
        data_returned = r.json()
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


class LGTMDataFilters:

    @staticmethod
    def org_to_ids(projects: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Converts the output from :func:`~lgtm.LGTMSite.get_my_projects` into a dic of GH org
        to list of projects including their GH id and LGTM id.
        """
        org_to_ids = {}
        for project in projects:
            if 'protoproject' in project:
                print('skipping %s' % project['protoproject']['displayName'])
                continue
            if 'realProject' not in project:
                raise KeyError('\'realProject\' not in %s' % str(project))
            the_project = project['realProject'][0]
            if the_project['repoProvider'] != 'github_apps':
                # Not really concerned with BitBucket right now
                continue
            org = str(the_project['slug']).split('/')[1]
            ids_list: List[Dict]
            if org in org_to_ids:
                ids_list = org_to_ids[org]
            else:
                ids_list = []
                org_to_ids[org] = ids_list
            ids_list.append({
                'display_name': the_project['displayName'],
                'key': the_project['key']
            })

        return org_to_ids
