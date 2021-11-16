from pprint import pprint
import json
from typing import Collection
import requests
from github import Github
from collections import defaultdict

user_in = input()
url = f'https://api.github.com/users/{user_in}/repos'


user_data = requests.get(url).json()

with open('Homework - 1\git_repos_req.json', 'w') as f:
    repos = defaultdict(list)
    for i in user_data:
        repos[user_in].append(i.get('full_name'))
    json.dump(repos, f)


with open('Homework - 1\git_repos_Github.json', 'w') as f:
    g_obj = Github()
    user = g_obj.get_user(user_in)
    repos = defaultdict(list)
    for repo in user.get_repos():
        repos[user_in].append(repo.name)
    json.dump(repos, f)
