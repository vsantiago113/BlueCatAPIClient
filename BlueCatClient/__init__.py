import requests
import urllib3
import re
from urllib.parse import urlencode, quote_plus


class BlueCatAuthError(Exception):
    pass


class BlueCatError(Exception):
    pass


class Client:
    def __init__(self, verify=False, warnings=False, api_version='v1', proxy_http=None, proxy_https=None):
        if verify is False:
            self.verify = verify
        elif verify is True:
            self.verify = verify
            
        if warnings is False:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        elif warnings is True:
            pass

        self.api_version = api_version
        self.headers = {'Content-Type': 'application/json'}
        self.proxies = {'http': proxy_http, 'https': proxy_https}
        self.base_url = None
        self.token = None
        self.session = None
        
    def connect(self, server=None, username=None, password=None):
        server = server.replace('https://', '').replace('http://', '').rstrip('/')
        self.base_url = 'https://{}/Services/REST/{}/'.format(server.rstrip('/'), self.api_version)
        session = requests.Session()
        session.headers.update(self.headers)
        session.proxies = self.proxies
        session.verify = self.verify
        response = session.get(self.base_url + 'login', params={'username': username,
                                                                'password': password})
        token = re.search(r'->\s(\w+:\s\w+==)\s<-', response.text, flags=re.I)
        if token:
            token = token.group(1)
            session.headers.update({'Authorization': token})
            self.session = session
            return response.status_code
        else:
            raise BlueCatAuthError('Authentication Error!')

    def close(self):
        response = self.session.get(self.base_url + 'logout')
        return response.status_code

    @staticmethod
    def properties_to_json(properties):
        return {i[0]: i[1] for i in [i.split('=') for i in properties.split('|') if i]}

    @staticmethod
    def json_to_properties(properties):
        return {'properties': '|'.join(['{}={}'.format(k, v) for k, v in properties.items()])}

    def get(self, method=None, **kwargs):
        kwargs = '?' + urlencode(kwargs, quote_via=quote_plus) if urlencode(kwargs, quote_via=quote_plus) else ''
        response = self.session.get('{}{}{}'.format(self.base_url, method, kwargs))
        if response.status_code in [200]:
            return response.json()
        else:
            raise BlueCatError(response.status_code)
