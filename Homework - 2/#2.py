import requests
from bs4 import BeautifulSoup
from pprint import pprint, saferepr
import json


params = {
    'keyword': 'чипсы',
    'page': 1
}
headers = {
    'User-Agent': 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'
}
url = 'https://roscontrol.com'
parsed_data = []


def parametres_parser(parametres:list):
    product_metrics = {}
    product_metrics['Безопасность'] = int(parametres[0]['data-width'])
    product_metrics['Пищевая ценность'] = int(parametres[1]['data-width'])
    product_metrics['Натуральность'] = int(parametres[2]['data-width'])
    product_metrics['Качество'] = int(parametres[3]['data-width'])

    return product_metrics

for page in range(int(input())):
    response = requests.get(url + '/testlab/search', params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    products_list = dom.find_all('div', {'class': 'wrap-product-catalog__item'})
    
    for product in products_list:
        product_info = {}

        info = product.find('div', {'class': 'product__item-link'})
        name = info.getText()
        parametres = parametres_parser(product.find_all('i'))
        try:
            rating = int(product.find('div', {'class': 'rate'}).getText())
        except:
            rating = None
        website = response.url

        product_info['name'] = name
        product_info['parametres'] = parametres
        product_info['rating'] = rating
        product_info['website'] = website

        parsed_data.append(product_info)

    params['page'] += 1

with open('Homework - 2\\roscontrol_product.json', 'w') as f:
    json.dump(parsed_data, f)