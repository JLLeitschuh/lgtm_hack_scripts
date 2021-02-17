# ## How the script currently works:
# - We first get all the github repos.
# - We then take each repo and follow the repository in lgtm
#
#
# ## changes that need to be made
# - Since we are adding lists to lgtm, we also need to store someplace every
# repo that we added to lgtm.
# - once teh script is done the list of lgtm saved projects will be stored in a txt file
# - after a period of time, say 24 hrs, we then run a companion script that moves
# lgtm followed projects into their own lists. this script will take the text file name
# and use that to create a list. it will then move the lgtm projects into that list and
# unfollow them from the lgtm list. this script can be used universally.
#
# - explicit changes:
#     - current scripts:
#         - each script must now accept a list arg that represents the list name that you want
#           your repos to be saved to.
#         - each script must now add the lgtm project id to a file that stores repos (txt file)
#     - new script:
#         - we need a script that will take a text file, loop through the text file,
#         and for each item in the text file add the item to the lgtm list (the list name
#         is derived from the name of the ext file)
#

from typing import List
from lgtm import LGTMSite

import utils.github_dates
import utils.github_api
import utils.cacher
import sys
import time

def save_project_to_lgtm(site: 'LGTMSite', repo_name: str) -> dict:
    print("Adding: " + repo_name)
    # Another throttle. Considering we are sending a request to Github
    # owned properties twice in a small time-frame, I would prefer for
    # this to be here.
    time.sleep(1)

    repo_url: str = 'https://github.com/' + repo_name
    project = site.follow_repository(repo_url)

    print("Saved the project: " + repo_name)
    return project

def find_and_save_projects_to_lgtm(language: str) -> List[str]:
    github = utils.github_api.create()
    site = LGTMSite.create_from_file()
    saved_project_ids: List[str] = []

    for date_range in utils.github_dates.generate_dates():
        repos = github.search_repositories(query=f'stars:>500 created:{date_range} fork:false sort:stars language:{language}')

        for repo in repos:
            # Github has rate limiting in place hence why we add a sleep here. More info can be found here:
            # https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting
            time.sleep(1)

            if repo.archived or repo.fork:
                continue

            saved_project = save_project_to_lgtm(site, repo.full_name)

            # Proto projects can't be saved to a project list, so instead we only grab real projects.
            if "realProject" in saved_project:
                saved_project_id = saved_project['realProject'][0]['key']
                saved_project_ids.append(saved_project_id)

    return saved_project_ids

if len(sys.argv) < 2:
    print("Please provide a language you want to search")
    exit

language = sys.argv[1].capitalize()

print('Following the top repos for %s' % language)
saved_project_ids = find_and_save_projects_to_lgtm(language)

# If the user provided a second arg then they want to create a custom list.
if len(sys.argv) <= 3:
    # print
    custom_list_name = sys.argv[2]
    utils.cacher.write_project_ids_to_file(saved_project_ids, custom_list_name)
