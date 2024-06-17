import requests
from typing import Optional


class Connection(object):
    def __init__(self, url: Optional[str] = None,
                 token: Optional[str] = None):
        self.url = url
        self.token = token
        self.headers = {'Authorization': 'Bearer ' + token,
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'}
        self.verify = True
        self.timeout: Optional[int] = None

    def get(self, endpoint, params: Optional[dict] = None):
        request_url = f'{self.url}/{endpoint}'
        response = requests.get(request_url,
                                headers=self.headers,
                                params=params,
                                verify=self.verify,
                                timeout=self.timeout
                                )

        return response
