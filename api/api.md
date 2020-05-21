# API Usage with Python

To use an `api` paired with python you first need to install a suitable package. The suggestes choice would be `requests`.

Within the suitable environment:
```python
conda install -c anaconda requests 
```

## Usage

First you need to import the package of course
```
import requests
```

An example for a request would be this
```
request = requests.get('http://api.open-notify.org')
print(request.text)
print(request.status_code)
```
To handle the given putput in the easiest way possible just transform it to a `json` object

```
people_json  = people.json()
print(people_json)
```

This enables to possibility to work in a more sophisticated way with the object

```
#To print the number of people in space

print("Number of people in space:",people_json['number'])
#To print the names of people in space using a for loop
for p in people_json['people']:
    print(p['name'])
```