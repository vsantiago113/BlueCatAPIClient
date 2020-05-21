import BlueCatAPIClient
import unittest
import os
import json

url = 'https://BlueCat-server.local'
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')


def run_full_test():
    client = BlueCatAPIClient.Client(api_version='v3')

    print(f'***** Testing: Login '.ljust(60, '*'))
    client.connect(url, username, password)

    print(f'***** Testing: GET method '.ljust(60, '*'))
    response = client.get(method='searchByCategory', keyword='MyIPV4Block', category='all')
    print(json.dumps(response.json(), indent=4))

    print(f'***** Testing: Logout '.ljust(60, '*'))
    client.disconnect()


class TestBlueCatAPIWrapper(unittest.TestCase):

    def test_authentication(self):
        client = BlueCatAPIClient.Client()

        response = client.connect(url, username, password)
        self.assertEqual(response.status_code, 200)

        response = client.disconnect()
        self.assertEqual(response.status_code, 200)

    def test_methods_get(self):
        client = BlueCatAPIClient.Client()

        client.connect(url, username, password)

        response = client.get(method='searchByCategory', keyword='MyIPV4Block', category='all', start=0, count=1)
        self.assertEqual(response.status_code, 200)

        client.disconnect()


if __name__ == '__main__':
    unittest.main()
