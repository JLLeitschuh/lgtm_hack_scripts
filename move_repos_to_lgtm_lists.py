from typing import List
from lgtm import LGTMSite

import os

def get_project_list_id(cached_file_name: str) -> str:
    project_list_name = cached_file_name.split(".")[0]

    # We want to find or create a project list based on the the name of
    # the text file that holds all of the projects we are currently following.
    return site.get_or_create_project_list(project_list_name)

def get_project_ids(cached_file: str) -> List[str]:
    file = open(cached_file, "r")

    project_ids = file.read().split("\n")

    # remove any "" in the array
    while("" in project_ids):
        project_ids.remove("")

    return project_ids

def cleanup(file_name: str):
    # Since we are done with the file, we can now delete it from the cache.
    os.remove(file_name)

def unfollow_projects(project_ids: List[str]):
    for project_id in project_ids:
        # The last thing we need to do is tidy up and unfollow all the repositories
        # we just added to our project list.
        site.unfollow_repository_by_id(project_id)

def process_cached_file(cached_file_name):
    cached_file = "cache/" + cached_file_name
    project_list_id = get_project_list_id(cached_file_name)
    project_ids = get_project_ids(cached_file)

    # With the project list id and the project ids, we now want to save the repos
    # we currently follow to the project list
    site.load_into_project_list(project_list_id, project_ids)

    unfollow_projects(project_ids)
    cleanup(cached_file)

site = LGTMSite.create_from_file()

projects = site.get_my_projects()

# build_still_in_progess = False
#
# for project in projects:
#     if project.get('protoproject') is not None and project.get('protoproject')['displayName']:
#         if project['protoproject']['state'] == "build_attempt_in_progress":
#             build_still_in_progess = True
#             break
#
# if build_still_in_progess:
#     print("There are projects still being processed by LGTM. It's not safe ")
#     return

cached_file_names = os.listdir("cache")

for cached_file_name in cached_file_names:
    process_cached_file(cached_file_name)
