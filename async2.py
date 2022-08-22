import time
import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from time import sleep
import xlsxwriter











headers = {'User-Agent':
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

# stat_time = time.time()

def get_first_url():
    url = 'https://mesopharm-shop.ru/catalog/'
    sleep(0.1)
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    data = soup.find_all('div', class_='t_ col-xl-6 col-lg-6 col-md-12 col-sm-12 col-xs-12')
    for i in data:
        url_cat = i.find('a').get('href')
        # print(url_cat)
        yield url_cat

def get_next_url():
    sleep(0.1)
    for url_cat in get_first_url():
        url = 'https://mesopharm-shop.ru' + url_cat
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find_all('li', class_='bxr-children-color-hover')
        for i in data:
            url_lib = i.find('a').get('href')
            if url_lib != 'https://mesopharm.ru/kontakty/offices/':
                yield url_lib
            else:
                print()
        break

def get_cat_url():
    sleep(0.1)
    # count = 0
    for url_lib in get_next_url():
        url = 'https://mesopharm-shop.ru' + url_lib
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find_all('table', class_='bxr-element-container')
        for i in data:
            html = i.find('a').get('href')
            # count += 1
            # print(count, html)
            yield html


def array():
    sleep(0.1)
    count = 0
    for html in get_cat_url():
        url = 'https://mesopharm-shop.ru' + html
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find('div', class_='col-xl-12 col-xs-12 bxr-container-catalog-element')
        name = data.find('div', class_='bxr-cloud-all').find('h1').text.strip()
        try:
            price = data.find('div', class_='bxr-detail-price').text
        except:
            price = 'Цена по запросу'
        description = data.find('div', class_='bxr-detail-tab-content').text.strip('\n').strip('')
        src = 'https://mesopharm-shop.ru/' + data.find('a').get('href')
        count += 1
        print(count, url)
        # yield name, price, description, src



# def writer(array):
#     book = xlsxwriter.Workbook('/Users/santa/Desktop/Cosmetics compain/Mesofarm/Mesofarm.xlsx')
#     page_1 = book.add_worksheet('Mesofarm')
#
#     headers = ['Наименование', 'Цена', "Описание", "Ссылка на фото товара", "Примечание"]
#     for col, h in enumerate(headers):
#         page_1.write_string(0, col, h)
#
#     page_1.set_column('A:A', 15)
#     page_1.set_column('B:B', 22)
#     page_1.set_column('C:C', 50)
#     page_1.set_column('D:D', 25)
#     # page_1.set_column('E:E', 10)
#     page_1.set_column('F:F', 30)
#
#     row = 1
#     column = 0
#
#     for item in array():
#         page_1.write(row, column, item[0])
#         page_1.write(row, column + 1, item[1])
#         page_1.write(row, column + 2, item[2])
#         page_1.write(row, column + 3, item[3])
#         # page_1.write(row, column + 4, item[4])
#         row += 1
#
#     book.close()
#
# writer(array)
#
#
#
# def main():
# #     # get_first_url()
# #     # get_next_url()
# #     # get_cat_url()
# #     # array()
#     writer(array)
# finish_time = round((time.time() - stat_time) % 60)
#
# print(f'Затраченное время на работу скрипта: {finish_time} минут')
#
# # if __name__ == '__main__':
# #     main()


