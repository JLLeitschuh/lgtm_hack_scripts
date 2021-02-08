from typing import List
from lgtm import LGTMSite

import utils.github_dates
import utils.github_api
import sys
import time

def save_project_to_lgtm(site: 'LGTMSite', repo_name: str):
    print("Adding: " + repo_name)
    # Another throttle. Considering we are sending a request to Github
    # owned properties twice in a small time-frame, I would prefer for
    # this to be here.
    time.sleep(1)

    repo_url: str = 'https://github.com/' + repo_name
    site.follow_repository(repo_url)
    print("Saved the project: " + repo_name)

def find_and_save_projects_to_lgtm(language: str):
    github = utils.github_api.create()
    site = LGTMSite.create_from_file()

    for date_range in utils.github_dates.generate_dates():
        repos = github.search_repositories(query=f'stars:>500 created:{date_range} fork:false sort:stars language:{language}')

        for repo in repos:
            # Github has rate limiting in place hence why we add a sleep here. More info can be found here:
            # https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting
            time.sleep(1)

            if repo.archived or repo.fork:
                continue

            save_project_to_lgtm(site, repo.full_name)

if len(sys.argv) < 2:
    print("Please provide a language you want to search")
    exit

language = sys.argv[1].capitalize()

print('Following the top repos for %s' % language)
find_and_save_projects_to_lgtm(language)
