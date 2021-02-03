from typing import List
from github import Github
from lgtm import LGTMSite
from datetime import datetime

import sys
import yaml
import time

def create_github() -> Github:
    with open("config.yml") as config_file:
        config = yaml.safe_load(config_file)
        github: dict = config['github']
        return Github(github['api_key'])

def current_year() -> int:
    now = datetime.now()
    return now.year

def generate_dates() -> List[str]:
    date_ranges: List[str] = []

    # Github started in 2008
    year_range = list(range(2008, current_year() + 1))

    for i, year in enumerate(year_range):
        date_ranges.append(f'{year}-01-01..{year}-12-31')

    return date_ranges

def save_project_to_lgtm(site: 'LGTMSite', repo_name: str):
    print("About to save: " + repo_name)
    # Another throttle. Considering we are sending a request to Github
    # owned properties twice in a small time-frame, I would prefer for
    # this to be here.
    time.sleep(1)

    repo_url: str = 'https://github.com/' + repo_name
    site.follow_repository(repo_url)
    print("Saved the project: " + repo_name)

def find_and_save_projects_to_lgtm(language: str, search_term: str):
    github = create_github()
    site = LGTMSite.create_from_file()

    for date_range in generate_dates():
        repos = github.search_repositories(query=f'language:{language} created:{date_range} {search_term}')

        for repo in repos:
            # Github has rate limiting in place hence why we add a sleep here. More info can be found here:
            # https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting
            time.sleep(1)

            if repo.archived or repo.fork:
                continue

            save_project_to_lgtm(site, repo.full_name)

if len(sys.argv) < 3:
    print("Please make sure you provided a language and search term")
    exit

language = sys.argv[1].capitalize()
search_term = sys.argv[2]

print(f'Following repos for the {language} language that contain the \'{search_term}\' search term.')
find_and_save_projects_to_lgtm(language, search_term)
