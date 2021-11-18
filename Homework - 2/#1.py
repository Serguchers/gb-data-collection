import json
from pprint import pprint, saferepr

import requests
from bs4 import BeautifulSoup

params = {
    "fromSearchLine": "true",
    "text": "python",
    "search_field": ["description", "company_name", "name"],
    "page": 0,
}
headers = {"User-Agent": "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14"}
url = "https://kaliningrad.hh.ru"
parsed_data = []


def currency_handler(value: list):
    cur_dict = {"min": None, "max": None, "cur": value[-1]}

    if len(value) == 7 and "до" in value[0]:
        curr = int("".join(el for el in value[2] if el.isdecimal()))
        cur_dict["max"] = curr

        return cur_dict

    if len(value) == 7 and "от" in value[0]:
        curr = int("".join(el for el in value[2] if el.isdecimal()))
        cur_dict["min"] = curr

        return cur_dict

    if len(value) == 3:
        min = value[0].replace(" ", "").split("–")[0]
        curr = int("".join(el for el in min if el.isdecimal()))
        cur_dict["min"] = curr

        max = value[0].replace(" ", "").split("–")[1]
        curr = int("".join(el for el in max if el.isdecimal()))
        cur_dict["max"] = curr

        return cur_dict


def vacancy_handler(vacancy):
    result = {}

    info = vacancy.find("a", {"class": "bloko-link"})
    name = info.getText()
    try:
        salary = vacancy.find("span", {"data-qa": "vacancy-serp__vacancy-compensation"}).contents
        salary = currency_handler(salary)
    except AttributeError:
        salary = None
    link = info["href"]
    main_site = response.url

    result["name"] = name
    result["salary"] = salary
    result["link"] = link
    result["main_site"] = main_site

    return result


for page in range(int(input())):
    response = requests.get(url + "/search/vacancy", params=params, headers=headers)
    dom = BeautifulSoup(response.text, "html.parser")
    vacancies_list = dom.find_all("div", {"class": "vacancy-serp-item"})

    for vacancy in vacancies_list:
        parsed_data.append(vacancy_handler(vacancy))

    params["page"] += 1


with open("Homework - 2\hh_parsed.json", "w") as f:
    json.dump(parsed_data, f)
