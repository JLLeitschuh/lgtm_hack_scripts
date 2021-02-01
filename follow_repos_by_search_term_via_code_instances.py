from typing import List
from github import Github
from lgtm import LGTMSite
import sys
import yaml
import time


def create_github() -> Github:
    with open("config.yml") as config_file:
        config = yaml.safe_load(config_file)
        github: dict = config['github']
        return Github(github['api_key'])

def find_and_save_projects_to_lgtm(language: str, search_term: str) -> List[str]:
    github = create_github()
    site = LGTMSite.create_from_file()

    code_found = github.search_code(query=f'language:{language} {search_term}')

    # This totalCount should end up at roughly 10,197 if we are able to loop through
    # the dates starting in 2008.
    print("total code_found count")
    print(code_found.totalCount)

    # at this point we can get the repo full name by running the following code below:
    # code_found[0].repository.full_name

    #
    # for repo in repos:
    #     # Github has rate limiting in place hence why we add a sleep here. More info can be found here:
    #     # https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting
    #     time.sleep(1)
    #
    #     global gh_counter
    #     gh_counter += 1
    #     print("gh_counter at ", gh_counter)
    #
    #     if repo.archived or repo.fork:
    #         continue
    #
    #     repo_name = repo.full_name
    #
    #     print("About to save: " + repo_name)
    #
    #     repo_url: str = 'https://github.com/' + repo_name
    #     # print(repo_url)
    #
    #     # global lgtm_counter
    #     global lgtm_counter
    #     lgtm_counter += 1
    #     print("lgtm_counter at ", lgtm_counter)
    #
    #     time.sleep(1)
    #     follow_repo_result = site.follow_repository(repo_url)
    #     print("Saved the project: " + repo_name)

if len(sys.argv) < 3:
    print("Please make sure you provided a language and search term")
    exit

language = sys.argv[1].capitalize()
search_term = sys.argv[2]

print(f'Following repos for the {language} language using the \'{search_term}\' search term.')
find_and_save_projects_to_lgtm(language, search_term)
