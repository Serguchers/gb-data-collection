import json
from pprint import pprint

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as DKE

client = MongoClient("127.0.0.1", 27017)
db = client["hh_vacancies_python"]

vacancies = db.vacancies

with open("Homework - 3\hh_parsed.json", "r") as f:
    data_json = json.load(f)

vacancies.create_index("link", unique=True)

for vacancy in data_json:
    try:
        vacancies.insert_one(vacancy)
    except DKE:
        print("Вакансия уже есть в базе.")
        continue
