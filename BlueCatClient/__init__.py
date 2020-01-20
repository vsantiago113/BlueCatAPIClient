import requests
import urllib3
import re


class BlueCatAuthError(Exception):
    pass


class BlueCatError(Exception):
    pass


class Client:
    def __init__(self, verify=bool(), warnings=bool(), api_version='v1'):
        self.verify = bool(verify)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) if warnings is False else None

        self.api_version = api_version
        self.base_url = None
        self.token = None
        self.session = None

    def connect(self, server=None, username=None, password=None):
        server = server.replace('https://', '').replace('http://', '').rstrip('/')
        self.base_url = f'https://{server.rstrip("/")}/Services/REST/{self.api_version}'
        session = requests.Session()
        session.headers.update({'Content-Type': 'application/json'})
        session.verify = self.verify
        response = session.get(self.base_url + '/login', params={'username': username,
                                                                 'password': password})
        token = re.search(r'->\s(\w+:\s\w+(?:==)?)\s<-', response.text, flags=re.I)
        if token:
            token = token.group(1)
            session.headers.update({'Authorization': token})
            self.session = session
            return response.status_code
        else:
            raise BlueCatAuthError('Authentication Error!')

    def close(self) -> int:
        response = self.session.get(self.base_url + '/logout')
        return response.status_code

    @staticmethod
    def properties_to_json(properties: str) -> dict:
        return {i[0]: i[1] for i in [i.split('=') for i in properties.split('|') if i]}

    @staticmethod
    def json_to_properties(properties: dict) -> dict:
        return {'properties': '|'.join([f'{k}={v}' for k, v in properties.items()])}

    def get(self, method=None, **kwargs) -> dict:
        response = self.session.get(f'{self.base_url}/{method}', params=kwargs)
        if response.status_code in [200]:
            return response.json()
        else:
            raise BlueCatError(response.text, response.status_code)

    def add(self, method=None, **kwargs):
        response = self.session.post(f'{self.base_url}/{method}', params=kwargs)
        if response.status_code in [200]:
            return 'The Entity was created successfully!'
        else:
            raise BlueCatError(response.text, response.status_code)

    def update(self, entity: dict) -> str:
        response = self.session.put(f'{self.base_url}/update', json=entity)
        if response.status_code in [200]:
            return 'The Entity was updated successfully!'
        else:
            raise BlueCatError(response.text, response.status_code)

    def delete(self, **kwargs) -> str:
        response = self.session.delete(f'{self.base_url}/delete', params=kwargs)
        if response.status_code in [200]:
            return 'The Entity was deleted successfully!'
        else:
            raise BlueCatError(response.text, response.status_code)
