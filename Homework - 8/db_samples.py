import sys
from pymongo import MongoClient
from pprint import pp, pprint

client = MongoClient('127.0.0.1', 27017)

db = client['instagram_1012']
users = db.users

sample = users.find({'target_name': sys.argv[1], 'status': sys.argv[2]})
for i in sample:
    pprint(i)