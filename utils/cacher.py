from typing import List
import os
import time
from lgtm import LGTMSite, LGTMRequestException, LGTMDataFilters, SimpleProject

# This is very similar to SimpleProject. If I had discovered SimpleProject earlier
# I would have built this code around that.
class ProjectBuild(SimpleProject):
    def build_successful(self, followed_projects: List[dict]) -> bool:
        if self.is_protoproject():
            # A throttle that although may not be necessary a nice plus.
            time.sleep(2)
            site = LGTMSite.create_from_file()
            data = site.retrieve_project(self.display_name)

            # A failed protoproject build will always be intrepreted to LGTM as a project that can't be found.
            if 'code' in data and data['code'] == 404:
                return False

            # In this case, the protoproject likely succeeded. To confirm this,
            # we check the language status to confirm the build succeeded.
            for language in data['languages']:
                if language['status'] == "success":
                    self.key = data['id']
                    return True

        return (
            not self.build_in_progress(followed_projects) and
            not self.build_failed(followed_projects)
        )

    def build_in_progress(self, followed_projects: List[dict]) -> bool:
        return (
            self.project_currently_followed(followed_projects) and
            self.project_state("build_attempt_in_progress", followed_projects)
        )

    def build_failed(self, followed_projects: List[dict]) -> bool:
        return (
            self.project_currently_followed(followed_projects) and
            self.project_state("build_attempt_failed", followed_projects)
        )

    def project_state(self, state: str, followed_projects: List[dict]) -> bool:
        in_state = False

        for project in followed_projects:
            simple_project = LGTMDataFilters.build_simple_project(project)

            if not simple_project.is_valid_project:
                continue

            if not simple_project.display_name == self.display_name:
                continue

            if simple_project.is_protoproject() and simple_project.state == state:
                in_state = True
                break

            # Real projects always have successful builds, or at least as far as I can tell.
            if not simple_project.is_protoproject():
                in_state = not (state == "build_attempt_in_progress" or state == "build_attempt_failed")
                break

        return in_state

    def project_currently_followed(self, followed_projects: List[dict]) -> bool:
        currently_followed = False
        for project in followed_projects:
            simple_project = LGTMDataFilters.build_simple_project(project)

            if not simple_project.is_valid_project:
                continue

            if simple_project.display_name == self.display_name:
                currently_followed = True
                break

        return currently_followed

class ProjectBuilds:
    def __init__(self, projects: List[ProjectBuild]):
        self.projects = projects

    def unfollow_projects(self, site: 'LGTMSite'):
        for project in self.projects:
            time.sleep(2)

            if project.is_protoproject():
                # Protoprojects are gnarly because I believe LGTM updates the key
                # if the protoproject succeeds. In case it does, we retrieve the
                # latest id from LGTM then unfollow it.
                data = site.retrieve_project(project.display_name)

                # A failed protoproject build will be intrepreted to LGTM
                # as a project that can't be found.
                if 'code' in data and data['code'] == 404:
                    continue

                self.unfollow_proto_project(site, data['id'])
            else:
                self.unfollow_real_project(site, project.key)


    def unfollow_proto_project(self, site: 'LGTMSite', id: int):
        try:
            time.sleep(2)

            site.unfollow_proto_repository_by_id(id)
        except LGTMRequestException as e:
            # In some cases even though we've recorded the project as a protoproject
            # it's actually a realproject. So we can't unfollow it via a proto-project
            # unfollow API call. We can however unfollow it via the real project API call.
            self.unfollow_real_project(site, id)

    def unfollow_real_project(self, site: 'LGTMSite', id: int):
        try:
            time.sleep(2)

            site.unfollow_repository_by_id(id)
        except LGTMRequestException as e:
            print(f"An unknown issue occurred unfollowing {project.display_name}")

    def return_successful_project_builds(self, site: 'LGTMSite') -> List[str]:
        filtered_project_keys: List[str] = []
        followed_projects = site.get_my_projects()

        for project in self.projects:
            if project.build_successful(followed_projects):
                filtered_project_keys.append(project.key)

        return filtered_project_keys

    def build_processes_in_progress(self, followed_projects: List[dict]) -> bool:
        in_progress = False

        for project in self.projects:
            if project.build_in_progress(followed_projects):
                in_progress = True
                break

        return in_progress

def create_cache_folder():
    if not os.path.exists('cache'):
        os.makedirs('cache')

def write_project_data_to_file(project_keys: List[str], file_name: str):
    create_cache_folder()

    file = open("cache/" + file_name + ".txt", "a")

    for project_key in project_keys:
        file.write(project_key + "\n")

    file.close()

def get_project_builds(cached_file: str) -> ProjectBuilds:
    file = open(cached_file, "r")

    cached_projects = file.read().split("\n")

    while("" in cached_projects):
        cached_projects.remove("")

    for i, project in enumerate(cached_projects):
        cached_projects[i] = ProjectBuild(
            display_name=project.split(",")[0],
            key=project.split(",")[1],
            project_type=project.split(",")[2],
            is_valid_project=True,
            org="",
            state=""
        )

            # display_name: str
            # key: str
            # project_type: str
            # is_valid_project: bool
            # org: str
            # state: str

    file.close()

    return ProjectBuilds(cached_projects)

def remove_file(file_name: str):
    os.remove(file_name)
