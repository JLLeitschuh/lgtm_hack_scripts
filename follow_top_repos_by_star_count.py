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

    # Github was formed in 2008
    year_range = list(range(2008, current_year() + 1))

    for i, year in enumerate(year_range):
        date_ranges.append(f'{year}-01-01..{year}-12-31')

    return date_ranges

def find_and_save_projects_to_lgtm(language: str):
    github = create_github()
    site = LGTMSite.create_from_file()

    for date_range in generate_dates():
        repos = github.search_repositories(query=f'stars:>500 created:{date_range} sort:stars language:{language}')

        for repo in repos:
            # Github has rate limiting in place hence why we add a sleep here. More info can be found here:
            # https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting
            time.sleep(1)

            if repo.archived or repo.fork:
                continue

            repo_name = repo.full_name

            print("Adding: " + repo_name)

            repo_url: str = 'https://github.com/' + repo_name
            print(repo_url)

            time.sleep(1)

            site.follow_repository(repo_url)


if len(sys.argv) < 2:
    print("Please provide a language you want to search")
    exit

language = sys.argv[1].capitalize()

print('Following the top repos for %s' % language)
find_and_save_projects_to_lgtm(language)
