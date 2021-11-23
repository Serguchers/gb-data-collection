import json
from os import name
from pprint import pprint

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as DKE

client = MongoClient("127.0.0.1", 27017)
db = client["hh_vacancies_python"]
vacancies = db.vacancies


def salary_filter(wage: int):
    for doc in vacancies.find({}):
        try:
            if doc["salary"]["min"] >= wage or doc["salary"]["max"] >= wage:
                pprint(doc)
        except:
            continue


if __name__ == "__main__":
    salary_filter(350000)

# Вероятно в этом задании подразумевалось использование операторов непосредственно в запросе mongo,
# но я не нашел простых путей для написания вложенных запросов, поэтому применил обычное сравнение.
