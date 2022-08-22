import time
import requests
from bs4 import BeautifulSoup
from time import sleep
import xlsxwriter



headers = {'User-Agent':
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

# stat_time = time()
# count = 0
def get_url():
    url = 'https://mesopharm-shop.ru/catalog/_mesopharm_professional/'
    sleep(0.1)
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    data = soup.find_all('table', class_='bxr-element-container')
    print(data)
    # for i in data:
    #     url_cat = i.find('a').get('href')
    #     print(url_cat)
        # yield url_cat

# def get_next_url():
#     sleep(0.1)
#     for url_cat in get_first_url():
#         url = 'https://mesopharm-shop.ru' + url_cat
#         response = requests.get(url=url, headers=headers)
#         soup = BeautifulSoup(response.text, "lxml")
#         data = soup.find_all('li', class_='bxr-children-color-hover')
#         for i in data:
#             url_lib = i.find('a').get('href')
#             if url_lib == 'https://mesopharm.ru/kontakty/offices/':
#                 print()
#             else:
#                 yield url_lib
#
# def get_cat_url():
#     sleep(1)
#     for url_lib in get_next_url():
#         url = 'https://mesopharm-shop.ru' + url_lib
#         response = requests.get(url=url, headers=headers)
#         soup = BeautifulSoup(response.text, "lxml")
#         data = soup.find_all('table', class_='bxr-element-container')
#         for i in data:
#             html = i.find('a').get('href')
#             yield html
#
# def array():
#     sleep(0.1)
#     for html in get_cat_url():
#         url = 'https://mesopharm-shop.ru/' + html
#         response = requests.get(url=url, headers=headers)
#         soup = BeautifulSoup(response.text, "lxml")
#         data = soup.find('div', class_='col-xl-12 col-xs-12 bxr-container-catalog-element')
#         name = data.find('div', class_='bxr-cloud-all').find('h1').text.strip()
#         try:
#             price = data.find('span', class_='bxr-market-current-price bxr-market-format-price 9').text
#         except:
#             price = 'Цена по запросу'
#         description = data.find('div', class_='bxr-detail-tab-content').text.strip()
#         src = 'https://mesopharm-shop.ru/' + data.find('a').get('href')
#
#         print(name, price, description, src )
#         # yield name, price, description, src