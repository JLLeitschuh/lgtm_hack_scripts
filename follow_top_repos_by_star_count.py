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
    saved_project_data: List[str] = []

    for date_range in utils.github_dates.generate_dates():
        repos = github.search_repositories(query=f'stars:>500 created:{date_range} fork:false sort:stars language:{language}')

        for repo in repos:
            # Github has rate limiting in place hence why we add a sleep here. More info can be found here:
            # https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting
            time.sleep(1)

            if repo.archived or repo.fork:
                continue

            saved_project = save_project_to_lgtm(site, repo.full_name)

            # TODO: This process is duplicated elsewhere and should be under one location
            if "realProject" in saved_project:
                saved_project_name = saved_project['realProject'][0]['displayName']
                saved_project_id = saved_project['realProject'][0]['key']
                saved_project_data.append(f'{saved_project_name},{saved_project_id},realProject')

            if "protoproject" in saved_project:
                saved_project_name = saved_project['protoproject']['displayName']
                saved_project_id = saved_project['protoproject']['key']
                saved_project_data.append(f'{saved_project_name},{saved_project_id},protoproject')

    return saved_project_data

if len(sys.argv) < 2:
    print("Please provide a language you want to search")
    exit

language = sys.argv[1].capitalize()

print('Following the top repos for %s' % language)
saved_project_data = find_and_save_projects_to_lgtm(language)

# If the user provided a second arg then they want to create a custom list.
if len(sys.argv) <= 3:
    # print
    custom_list_name = sys.argv[2]
    utils.cacher.write_project_data_to_file(saved_project_data, custom_list_name)
