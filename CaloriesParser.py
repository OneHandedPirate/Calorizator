from bs4 import BeautifulSoup
import requests
import random
import csv
from time import sleep
import json

def prd():
    products = bscat.find('table').find_all('tr')
    for product in products[1:]:
        name = product.find_all('a')[-1].text
        protein = product.find(class_="views-field views-field-field-protein-value").text.strip()
        fat = product.find(class_='views-field views-field-field-fat-value').text.strip()
        carbs = product.find(class_="views-field views-field-field-carbohydrate-value").text.strip()
        ccal = product.find(class_='views-field views-field-field-kcal-value').text.strip()
        products_list.append([name, protein, fat, carbs, ccal])
        products_all.append([name, protein, fat, carbs, ccal])

URL = 'https://calorizator.ru/product'
headers = {
        'Accept': '*/*',
        'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
 }

req = requests.get(URL, headers=headers)
scr = req.text

categories_dict = {}
bs = BeautifulSoup(scr, 'lxml')
categories = bs.find_all(class_='product')
for gcat in categories[:-1]:
    global_category = gcat.find_all('li')
    for cat in global_category:
        category_text = cat.find('a').text
        category_url = cat.find('a').get('href')
        categories_dict.update({f'{category_text}': 'https://calorizator.ru/' + category_url})

with open('all_categories.json', 'w') as file:
    json.dump(categories_dict, file, indent=4, ensure_ascii=False)

with open('all_categories.json') as file:
    all_categories = json.load(file)

count = 0
shrums = {"Colbasi": "https://calorizator.ru/product/sausage"}
products_all = []
for cat_name, cat_href in all_categories.items():
    category_scr = requests.get(cat_href, headers=headers).text
    bscat = BeautifulSoup(category_scr, 'lxml')
    pages = bscat.find(class_='pager')
    products_list = []
    if pages:
        for page in range(len(pages.find_all('li'))-1):
            page_url = f'{cat_href}?page={page}'
            page_req = requests.get(page_url, headers=headers).text
            bscat = BeautifulSoup(page_req, 'lxml')
            prd()
    else:
        prd()
    count += 1
    with open (f'data/{count} {cat_name}.csv', 'w', encoding='utf-8-sig', newline='') as csvtab:
        writer = csv.writer(csvtab, delimiter=',', dialect='excel')
        writer.writerow(['Продукт', 'Белки', 'Жиры', 'Углеводы', 'Калорийность'])
        for prod in products_list:
            writer.writerow(prod)

    print(f'Осталось спарсить {len(all_categories)-count} категорий')
    sleep(random.choice(range(2, 5)))

with open (f'data/products_all.csv', 'w', encoding='utf-8-sig', newline='') as csvtab:
    writer = csv.writer(csvtab, delimiter=',', dialect='excel')
    writer.writerow(['Продукт', 'Белки', 'Жиры', 'Углеводы', 'Калорийность'])
    for prod in products_all:
        writer.writerow(prod)


