from typing import List
from lgtm import LGTMSite

import utils.cacher
import os
import time

def get_project_list_id(cached_file_name: str, site: 'LGTMSite') -> str:
    project_list_name = cached_file_name.split(".")[0]

    return site.get_or_create_project_list(project_list_name)

def process_cached_file(cached_file_name: str, site: 'LGTMSite'):
    cached_file = "cache/" + cached_file_name
    project_builds = utils.cacher.get_project_builds(cached_file)
    followed_projects = site.get_my_projects()

    if project_builds.build_processes_in_progress(followed_projects):
        print(f'The {cached_file_name} can\'t be processed at this time because a project build is still in progress.')
        return

    project_list_id = get_project_list_id(cached_file_name, site)
    print("Moving followed projects to the project list")

    # site.load_into_project_list(project_list_id, project_builds.return_successful_project_builds(site))
 
    # If a project fails to be processed by LGTM, we still unfollow the project.
    print("Unfollowing projects")
    project_builds.unfollow_projects(site)
    print("Removing the cache file.")
    utils.cacher.remove_file(cached_file)
    print("Done processing cache file.")

site = LGTMSite.create_from_file()

for cached_file_name in os.listdir("cache"):
    process_cached_file(cached_file_name, site)

print("Finished!")
