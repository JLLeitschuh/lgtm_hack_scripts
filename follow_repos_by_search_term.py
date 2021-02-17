from typing import List
from lgtm import LGTMSite

import utils.cacher
import utils.github_dates
import utils.github_api

import sys
import time

def save_project_to_lgtm(site: 'LGTMSite', repo_name: str) -> dict:
    print("About to save: " + repo_name)
    # Another throttle. Considering we are sending a request to Github
    # owned properties twice in a small time-frame, I would prefer for
    # this to be here.
    time.sleep(1)

    repo_url: str = 'https://github.com/' + repo_name
    project = site.follow_repository(repo_url)
    print("Saved the project: " + repo_name)
    return project

def find_and_save_projects_to_lgtm(language: str, search_term: str) -> List[str]:
    github = utils.github_api.create()
    site = LGTMSite.create_from_file()
    saved_project_ids: List[str] = []
    for date_range in utils.github_dates.generate_dates():
        repos = github.search_repositories(query=f'language:{language} fork:false created:{date_range} {search_term}')
        print(f'language:{language} fork:false created:{date_range} {search_term}')
        for repo in repos:
            # Github has rate limiting in place hence why we add a sleep here. More info can be found here:
            # https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting
            time.sleep(1)

            if repo.archived or repo.fork:
                continue

            saved_project = save_project_to_lgtm(site, repo.full_name)
            print('--------------------')
            print('--------------------')
            print('--------------------')
            print(saved_project)
            print('--------------------')
            print('--------------------')
            print('--------------------')
            saved_project_id = saved_project['realProject'][0]['key']
            saved_project_ids.append(saved_project_id)

    return saved_project_ids

if len(sys.argv) < 3:
    print("Please make sure you provided a language and search term")
    exit

language = sys.argv[1].capitalize()
search_term = sys.argv[2]

print(f'Following repos for the {language} language that contain the \'{search_term}\' search term.')
saved_project_ids = find_and_save_projects_to_lgtm(language, search_term)

# If the user provided a second arg then they want to create a custom list.
if len(sys.argv) <= 4:
    # print
    custom_list_name = sys.argv[3]
    utils.cacher.write_project_ids_to_file(saved_project_ids, custom_list_name)
