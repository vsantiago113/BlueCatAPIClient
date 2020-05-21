# BlueCatAPIClient
[Proteus_API_Guide_3.7.1](http://timlossev.com/attachments/Proteus_API_Guide_3.7.1.pdf "Proteus_API_Guide_3.7.1")<br />
[Making APIs Work for You](https://github.com/bluecatlabs/making-apis-work-for-you "Making APIs Work for You")<br />
[BlueCat Gateway](https://www.bluecatnetworks.com/resources_doc/whitepaper/bluecat-gateway.pdf "BlueCat Gateway")

---

![PyPI - Status](https://img.shields.io/pypi/status/BlueCatAPIClient)
![PyPI - Format](https://img.shields.io/pypi/format/BlueCatAPIClient)
![GitHub](https://img.shields.io/github/license/vsantiago113/BlueCatAPIClient)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/vsantiago113/BlueCatAPIClient)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/BlueCatAPIClient)

An API Client for BlueCat to be able to easily use the API in a more standard way.

## How to install
```ignorelang
$ pip install BlueCatAPIClient
```

## Usage
The argument "method" must be specify every time.

#### Default arguments and attributes
```python
import BlueCatAPIClient

client = BlueCatAPIClient.Client(verify=False, warnings=False, api_version='v1')

client.get(url=None, method='', data=None, auth = None)

# client.headers
# client.url_base
# client.token
# client.session

```

#### Getting entities
```python
import BlueCatAPIClient
import json

client = BlueCatAPIClient.Client()
client.connect(url='https://BlueCat-server.local', username='admin', password='Admin123')

response = client.get(method='searchByCategory', keyword='MyIPV4Block', category='all')
print(json.dumps(response.json(), indent=4))

client.disconnect()
```

#### Paging
```python
import BlueCatAPIClient
import json

client = BlueCatAPIClient.Client()
client.connect(url='https://BlueCat-server.local', username='admin', password='Admin123')

response = client.get(method='searchByCategory', keyword='MyIPV4Block', category='all', start=0, count=1)
print(json.dumps(response.json(), indent=4))

client.disconnect()
```

#### Filtering entities
```python
import BlueCatAPIClient
import json

client = BlueCatAPIClient.Client()
client.connect(url='https://BlueCat-server.local', username='admin', password='Admin123')

response = client.get(method='getEntityById', id='12345')
print(json.dumps(response.json(), indent=4))

client.disconnect()
```

#### How to work with properties
```python
import BlueCatAPIClient
import json

client = BlueCatAPIClient.Client()
client.connect(url='https://BlueCat-server.local', username='admin', password='Admin123')

response = client.get(method='searchByCategory', keyword='MyIPV4Block', category='all', start=0, count=1)
if response.status_code == 200:
    properties = client.properties_to_json(response.json()[0].get('properties', ''))
    print(properties)

    print(client.json_to_properties(properties))

client.disconnect()
```

#### Creating entities
```python
import BlueCatAPIClient
import json

client = BlueCatAPIClient.Client()
client.connect(url='https://BlueCat-server.local', username='admin', password='Admin123')

response = client.post(method='addIP4BlockByCIDR', parentId='12345', CIDR='10.0.0.1/24', properties='name=MyIPV4Block')
print(json.dumps(response.json(), indent=4))

client.disconnect()
```

#### Updating entities
```python
import BlueCatAPIClient
import json

client = BlueCatAPIClient.Client()
client.connect(url='https://BlueCat-server.local', username='admin', password='Admin123')

response = client.get(method='searchByCategory', keyword='MyIPV4Block', category='all', start=0, count=1)
update_entity = response.json()[0]
update_entity['name'] = 'MyIPV4Block_TEST'
response = client.put(update_entity)
print(json.dumps(response.json(), indent=4))

client.disconnect()
```

#### Deleting entities
```python
import BlueCatAPIClient
import json

client = BlueCatAPIClient.Client()
client.connect(url='https://BlueCat-server.local', username='admin', password='Admin123')

response = client.delete(ObjectId=12345)
print(json.dumps(response.json(), indent=4))

client.disconnect()
```
