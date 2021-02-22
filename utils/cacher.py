from typing import List
import os
import time
from lgtm import LGTMSite

class ProjectBuild:
    def __init__(self, project: dict):
        self.project = project
        self.name = project["name"]
        self.id = project["id"]
        self.type = project["type"]

    def realProject(self) -> bool:
        return self.type == "realProject"

    def protoproject(self) -> bool:
        return self.type == "protoproject"

    def build_successful(self, followed_projects: List[dict]) -> bool:
        if self.protoproject:
            # A throttle that although may not be necessary a nice plus.
            time.sleep(2)
            site = LGTMSite.create_from_file()
            data = site.retrieve_project(self.name)

            # A failed protoproject build will always be intrepreted to LGTM as a project that can't be found.
            if 'code' in data and data['code'] == 404:
                return False

        # I don't know the name of the build successful status.
        return (
            not self.build_in_progress(followed_projects) and
            not self.build_failed(followed_projects)
        )

    def build_in_progress(self, followed_projects: List[dict]) -> bool:
        return (
            self.project_part_of_cache(followed_projects) and
            self.project_state("build_attempt_in_progress", followed_projects)
        )

    def build_failed(self, followed_projects: List[dict]) -> bool:
        return (
            self.project_part_of_cache(followed_projects) and
            self.project_state("build_attempt_failed", followed_projects)
        )

    def project_state(self, state: str, followed_projects: List[dict]) -> bool:
        in_state = False

        for project in followed_projects:
            if project.get('protoproject') is not None and project.get('protoproject')['state'] == state:
                in_state = True
                break

        return in_state

    def project_part_of_cache(self, followed_projects: List[dict]) -> bool:
        part_of_cache = False
        for project in followed_projects:
            if (
                project.get('protoproject') is not None and project.get('protoproject')['displayName'] == self.name or
                project.get('realProject') is not None and project.get('realProject')[0]['displayName'] == self.name
                ):
                part_of_cache = True
                break

        return part_of_cache

class ProjectBuilds:
    def __init__(self, projects: List[ProjectBuild]):
        self.projects = projects

    def unfollow_projects(self, site: 'LGTMSite'):
        for project in self.projects:
            time.sleep(1)
            if project.realProject():
                site.unfollow_repository_by_id(project.id)
            else:
                data = site.retrieve_project(project.name)

                # A failed protoproject build will always be intrepreted to LGTM as a project that can't be found.
                if 'code' in data and data['code'] == 404:
                    return

                site.unfollow_proto_repository_by_id(project.id)

    def return_successful_project_builds(self, site: 'LGTMSite') -> List[str]:
        filtered_project_ids: List[str] = []
        followed_projects = site.get_my_projects()

        for project in self.projects:
            if project.build_successful(followed_projects):
                filtered_project_ids.append(project.id)

        return filtered_project_ids

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

def write_project_data_to_file(project_ids: List[str], file_name: str):
    create_cache_folder()

    file = open("cache/" + file_name + ".txt", "a")

    for project_id in project_ids:
        file.write(project_id + "\n")

    file.close()

def get_project_builds(cached_file: str) -> ProjectBuilds:
    file = open(cached_file, "r")

    project_data = file.read().split("\n")

    while("" in project_data):
        project_data.remove("")

    for i, project in enumerate(project_data):
        project_data[i] = ProjectBuild({
            "name": project.split(",")[0],
            "id": project.split(",")[1],
            "type": project.split(",")[2],
        })

    file.close()

    return ProjectBuilds(project_data)

def remove_file(file_name: str):
    os.remove(file_name)
