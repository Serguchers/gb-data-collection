import json
import requests
from pprint import pp, pprint


token = ''
method = 'groups.get'
v = '5.131'

url = f'https://api.vk.com/method/{method}'
parametres = {
    'access_token': token,
    'v': v,
    'extended': 1
}

data = requests.get(url, params=parametres).json()
with open('Homework - 1\\vk_groups.json', 'w') as f:
    json.dump(data, f)