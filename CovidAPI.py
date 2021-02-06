import json
import requests
from urllib.request import urlopen

with urlopen('https://api.covid19api.com/summary') as response:
    source = response.read()

data = json.loads(source)

for country in data['Countries']:
    print(country['Country'])