from web3.providers import BaseProvider
import requests

import json
import os


class RESTProvider(BaseProvider):

    def __init__(self, rest_url=None):
        provider_url = os.environ.get('WEB3_PROVIDER_URI', '')
        if rest_url is None and provider_url.startswith('rest+'):
            rest_url = provider_url[len('rest+'):]
        self.api = rest_url

    def make_request(self, method, params):
        p = {'params': json.dumps(params)}
        try:
            response = requests.get(f'{self.api}/{method}', params=p)
        except Exception:
            return {'error': 'An Exception Occured ....'}

        if response.status_code == 200:
            return response.json()
        else:
            return {'error': response.text}

    def isConnected(self):
        response = self.make_request('web3_clientVersion', [])

        if 'error' in response:
            return False
        else:
            return True
