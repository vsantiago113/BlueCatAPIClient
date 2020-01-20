# BlueCat Client

### Description
This is a wrapper to make it easier to use the API to interact with BlueCat to get, update, delete and create records.

---

### Class Usage

#### Import
Import the package BlueCatClient then create an instance of the class Client and use the class instance to create a connection. To close the connection use the close method.
```python
import BlueCatClient

client = BlueCatClient.Client()
client.connect(server='mybluecat.local', username='myusername', password='mypassword')

client.close()
```

### Usage of GET class method
Use the get method to query BlueCat, the first parameter is the method and the rest are the kwargs of the parameters in the BlueCat documentation.

#### BlueCat Documentation of searchByCategory
"Search by Category<br />
searchByCategory() returns an array of entities by searching for keywords associated with objects of
a specified object category.<br />
APIEntity[] searchByCategory ( String keyword, String category, int start, int
count )<br />
Parameters<br />
keyword—the search keyword string. This value cannot be null or empty.<br />
category—the entity category to be searched. This must be one of the entity categories listed in
Entity Categories on page 227.<br />
start—indicates where in the list of returned objects to start returning objects. The list begins at an
index of 0. This value cannot be null or empty.<br />
count—the maximum number of objects to return. The default value is 10. This value cannot be null or
empty.<br />
Output/Response<br />
Returns an array of entities matching the keyword text and the category type, or returns an empty
array."
```python
import BlueCatClient

client = BlueCatClient.Client()
client.connect(server='mybluecat.local', username='myusername', password='mypassword')

response = client.get(method='searchByCategory', keyword='MyIPV4Block',
                      category='all', start=0, count=1000)
print(response[0])

client.close()
```

---

### How to work with properties
How to convert properties from string into json and from json back into string.

```python
import BlueCatClient

client = BlueCatClient.Client()
client.connect(server='mybluecat.local', username='myusername', password='mypassword')

response = client.get(method='searchByCategory', keyword='MyIPV4Block',
                      category='all', start=0, count=1000)
print(response[0])

if response:
    properties = client.properties_to_json(response[0].get('properties', ''))
    print(properties)

    print(client.json_to_properties(properties))

client.close()
```

---

### How to use the ADD class method
The ADD method is used to create entities and objects in BlueCat.

```python
import BlueCatClient

client = BlueCatClient.Client()
client.connect(server='mybluecat.local', username='myusername', password='mypassword')

response = client.add(method='addIP4BlockByCIDR', parentId='199999', CIDR='10.1.1.0/24',
                      properties='name=MyIPV4Block')
print(response)

client.close()
```

---

### How to use the UPDATE class method
When updating an entity, query the entity to get the data as a json object, then modify the values and send the entity back with the new values. If you don't send everything in the json you will get an error.

```python
import BlueCatClient

client = BlueCatClient.Client()
client.connect(server='mybluecat.local', username='myusername', password='mypassword')

response = client.get(method='searchByCategory', keyword='MyIPV4Block',
                      category='all', start=0, count=1000)

update_entity = response[0]
update_entity['name'] = 'MyIPV4Block_TEST'
response = client.update(update_entity)
print(response)

response = client.get(method='searchByCategory', keyword='MyIPV4Block_TEST',
                      category='all', start=0, count=1000)
print(response[0])


client.close()
```

---

### How to use the DELETE class method

```python
import BlueCatClient

client = BlueCatClient.Client()
client.connect(server='mybluecat.local', username='myusername', password='mypassword')

response = client.delete(ObjectId=1678894)
print(response)

client.close()
```
