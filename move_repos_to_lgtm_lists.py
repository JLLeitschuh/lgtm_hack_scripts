#     - new script:
#         - we need a script that will take a text file, loop through the text file,
#         and for each item in the text file add the item to the lgtm list (the list name
#         is derived from the name of the ext file)
#

from typing import List
from lgtm import LGTMSite

import sys
import time

site = LGTMSite.create_from_file()

file_name = "test.txt"
project_list_name = file_name.split(".")[0]

# We want to find or create a project list based on the the name of
# the text file that holds all of the projects we are currently following.
project_list_data = site.get_or_create_project_list(project_list_name)
project_list_id = project_list_data['realProject'][0]['key']
file = open(file_name, "r")

project_ids = file.read()
# With the project list id and the project ids, we now want to save the repos
# we currently follow to the project list
site.load_into_project_list(project_list_id, project_ids)

for project_id in project_ids:
    print(project_id)
    # The last thing we need to do is tidy up and unfollow all the repositories
    # we just added to our project list.
    site.unfollow_repository_by_id(project_id)


# lgtm methods we need to use
#   get_or_create_project_list
#   unfollow_repository_by_id
#   load_into_project_list


#
# def save_project_to_lgtm(site: 'LGTMSite', repo_name: str):
#     print("Adding: " + repo_name)
#     # Another throttle. Considering we are sending a request to Github
#     # owned properties twice in a small time-frame, I would prefer for
#     # this to be here.
#     time.sleep(1)
#
#     repo_url: str = 'https://github.com/' + repo_name
#     site.follow_repository(repo_url)
#     print("Saved the project: " + repo_name)
#
# def find_and_save_projects_to_lgtm(language: str):
#     github = utils.github_api.create()
#     site = LGTMSite.create_from_file()
#
#     for date_range in utils.github_dates.generate_dates():
#         repos = github.search_repositories(query=f'stars:>500 created:{date_range} fork:false sort:stars language:{language}')
#
#         for repo in repos:
#             # Github has rate limiting in place hence why we add a sleep here. More info can be found here:
#             # https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting
#             time.sleep(1)
#
#             if repo.archived or repo.fork:
#                 continue
#
#             save_project_to_lgtm(site, repo.full_name)
#
# if len(sys.argv) < 2:
#     print("Please provide a language you want to search")
#     exit
#
# language = sys.argv[1].capitalize()
#
# print('Following the top repos for %s' % language)
# find_and_save_projects_to_lgtm(language)
