from typing import List
from lgtm import LGTMSite

import sys
import time
import os

cached_files = os.listdir("cache")
site = LGTMSite.create_from_file()

for cached_file_name in cached_files:
    # This is dirty. Is there an easier way to do this?
    cached_file = "cache/" + cached_file_name

    project_list_name = cached_file_name.split(".")[0]

    # We want to find or create a project list based on the the name of
    # the text file that holds all of the projects we are currently following.
    project_list_id = site.get_or_create_project_list(project_list_name)

    file = open(cached_file, "r")

    project_ids = file.read().split("\n")

    # remove any "" in the array
    while("" in project_ids):
        project_ids.remove("")
    # With the project list id and the project ids, we now want to save the repos
    # we currently follow to the project list

    site.load_into_project_list(project_list_id, project_ids)

    for project_id in project_ids:
        # The last thing we need to do is tidy up and unfollow all the repositories
        # we just added to our project list.
        site.unfollow_repository_by_id(project_id)

    os.remove(cached_file)
