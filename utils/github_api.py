import os

from github import Github
import yaml


def create() -> Github:
    hub_config_file = f'{os.path.expanduser("~")}/.config/hub'
    if os.path.exists(hub_config_file):
        with open(f'{os.path.expanduser("~")}/.config/hub') as hub_file:
            hub_config = yaml.safe_load(hub_file)
        return Github(login_or_token=hub_config['github.com'][0]['oauth_token'])
    else:
        with open("config.yml") as config_file:
            config = yaml.safe_load(config_file)
            github: dict = config['github']
            return Github(github['api_key'])
