from typing import List

from github import Github

from lgtm import LGTMSite
import sys
import yaml


def create_github() -> Github:
    with open("config.yml") as config_file:
        config = yaml.safe_load(config_file)
        github: dict = config['github']
        return Github(github['api_key'])


def load_repository_list(org: str) -> List[str]:
    github = create_github()
    repos = github.get_organization(org).get_repos(type='public')

    repos_to_load: List[str] = []
    for repo in repos:
        if not repo.archived and not repo.fork and repo.language in ['Kotlin', 'Groovy', 'Java']:
            print("Adding: " + repo.full_name)
            repos_to_load.append(repo.full_name)

    return repos_to_load


org_to_follow = sys.argv[1]
print('Following Org: %s' % org_to_follow)

repository_list = load_repository_list(org_to_follow)

site = LGTMSite.create_from_file()

for repo_name in repository_list:
    repo_url: str = 'https://github.com/' + repo_name
    print(repo_url)
    site.follow_repository(repo_url)
