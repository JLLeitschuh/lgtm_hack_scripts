from dataclasses import dataclass
from typing import Optional, List

import requests
import yaml


@dataclass
class LGTMSite:
    nonce: str
    long_session: str
    short_session: str
    api_version: str

    def _cookies(self):
        return {
            'lgtm_long_session': self.long_session,
            'lgtm_short_session': self.short_session
        }

    def _headers(self):
        return {
            'LGTM-Nonce': self.nonce

        }

    def load_into_project_list(self, into_project: int, lgtm_project_ids: List[str]):
        url = "https://lgtm.com/internal_api/v0.2/updateProjectSelection"
        # Because LGTM uses some wacky format for it's application/x-www-form-urlencoded data
        list_serialized = ', '.join([('"' + elem + '"') for elem in lgtm_project_ids])
        data = {
            'projectSelectionId': into_project,
            'addedProjects': '[' + list_serialized + ']',
            'removedProjects': '[]',
            'apiVersion': self.api_version
        }
        print(data)
        r = requests.post(url, data, cookies=self._cookies(), headers=self._headers())
        data_returned = r.json()
        print(data_returned)

    def load_repository(self, repository_url: str):
        url = "https://lgtm.com/internal_api/v0.2/followProject"
        data = {
            'url': repository_url,
            'apiVersion': self.api_version
        }
        r = requests.post(url, data, cookies=self._cookies(), headers=self._headers())
        data_returned = r.json()
        print(data_returned)

    @staticmethod
    def retrieve_project_id(gh_project_path: str) -> Optional[str]:
        url = "https://lgtm.com/api/v1.0/projects/g/" + gh_project_path
        r = requests.get(url)
        data_returned = r.json()
        if 'id' in data_returned:
            return str(data_returned["id"])
        else:
            return None

    @staticmethod
    def create_from_file() -> 'LGTMSite':
        with open("config.yml") as config_file:
            config = yaml.safe_load(config_file)
            lgtm: dict = config.lgtm
            return LGTMSite(
                nonce=lgtm['nonce'],
                long_session=lgtm['long_session'],
                short_session=lgtm['short_session'],
                api_version=lgtm['api_version'],
            )
