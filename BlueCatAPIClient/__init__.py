from BlueCatAPIClient.api_interface import APIPlugin
import requests
import re


class Client(APIPlugin):
    headers = {'Content-Type': 'application/json'}
    base_url = None
    token = None
    session = None

    def connect(self, url: [str, bytes] = '', username: [str, bytes] = '', password: [str, bytes] = ''):
        self.base_url = f'{url.strip("/")}/Services/REST/{self.api_version}'
        session = requests.Session()
        session.headers = self.headers
        session.verify = self.verify
        response = session.get(f'{self.base_url}/login', params={'username': username, 'password': password})
        token = re.search(r'->\s(\w+:\s\w+(?:==)?)\s<-', response.text, flags=re.I)
        if token:
            self.token = token.group(1)
            session.headers.update({'Authorization': self.token})
            self.session = session

        return response

    def disconnect(self):
        response = self.session.get(f'{self.base_url}/logout')
        return response

    @staticmethod
    def properties_to_json(properties: str) -> dict:
        return {i[0]: i[1] for i in [i.split('=') for i in properties.split('|') if i]}

    @staticmethod
    def json_to_properties(properties: dict) -> dict:
        return {'properties': '|'.join([f'{k}={v}' for k, v in properties.items()])}

    def get(self, url: [str, None] = None, method: [str, bytes] = '', data: dict = None,
            **kwargs) -> requests.Response:
        """

        :param url: The URL of the resource you are trying to access. Defaults to base_url + method.
        :param method: The method is the part of the url that changes and is appended to basic_url.
        :param data: The data to change or update as a Python dictionary. Defaults to None.
        :param kwargs: All parameters required by the API call.
        :return: The requests.Response of the API call.
        """
        url = f'{self.base_url}/{method.strip("/")}' if url is None else url
        return self.session.get(url, json=data, params=kwargs)

    def post(self, url: [str, None] = None, method: [str, bytes] = '', data: [dict, list] = None,
             **kwargs) -> requests.Response:
        """

        :param url: The URL of the resource you are trying to access. Defaults to base_url + method.
        :param method: The method is the part of the url that changes and is appended to basic_url.
        :param data: The data to change or update as a Python dictionary. Defaults to None.
        :param kwargs: All parameters required by the API call.
        :return: The requests.Response of the API call.
        """
        url = f'{self.base_url}/{method.strip("/")}' if url is None else url
        return self.session.post(url, json=data, params=kwargs)

    def put(self, url: [str, None] = None, method='update', data: [dict, list] = None,
            **kwargs) -> requests.Response:
        """

        :param url: The URL of the resource you are trying to access. Defaults to base_url + method.
        :param method: The method is the part of the url that changes and is appended to basic_url.
        :param data: The data to change or update as a Python dictionary. Defaults to None.
        :param kwargs: All parameters required by the API call.
        :return: The requests.Response of the API call.
        """
        url = f'{self.base_url}/{method.strip("/")}' if url is None else url
        return self.session.put(url, json=data, params=kwargs)

    def delete(self, url: [str, None] = None, method='delete', data: [dict, list] = None,
               **kwargs) -> requests.Response:
        """

        :param url: The URL of the resource you are trying to access. Defaults to base_url + method.
        :param method: The method is the part of the url that changes and is appended to basic_url.
        :param data: The data to change or update as a Python dictionary. Defaults to None.
        :param kwargs: All parameters required by the API call.
        :return: The requests.Response of the API call.
        """
        url = f'{self.base_url}/{method.strip("/")}' if url is None else url
        return self.session.delete(url, json=data, params=kwargs)
