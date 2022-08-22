import requests
from bs4 import BeautifulSoup
from time import sleep
import xlsxwriter
from time import time
import asyncio
import aiohttp
import csv

headers = {'User-Agent':
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

stat_time = time()
async def get_first_url():
    url = 'https://mesopharm-shop.ru/catalog/'
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await response.text(), 'lxml')
        data = soup.find_all('div', class_='t_ col-xl-6 col-lg-6 col-md-12 col-sm-12 col-xs-12')

        tasks = []

        for page in range(1, 10):
            task = asyncio.create_task(get_next_url(session))
            tasks.append(task)

        await get_first_url(*tasks)



    # response = requests.get(url=url, headers=headers)


    for i in data:
        url_cat = i.find('a').get('href')
        # print(url_cat)
        yield url_cat

def get_next_url():
    sleep(1)
    for url_cat in get_first_url():
        url = 'https://mesopharm-shop.ru' + url_cat
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find_all('li', class_='bxr-children-color-hover')
        for i in data:
            url_lib = i.find('a').get('href')
            if url_lib == 'https://mesopharm.ru/kontakty/offices/':
                print()
            else:
                yield url_lib

def get_cat_url():
    sleep(1)
    for url_lib in get_next_url():
        url = 'https://mesopharm-shop.ru' + url_lib
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find_all('table', class_='bxr-element-container')
        for i in data:
            html = i.find('a').get('href')
            yield html

def array():
    sleep(1)
    for html in get_cat_url():
        url = 'https://mesopharm-shop.ru/' + html
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find('div', class_='col-xl-12 col-xs-12 bxr-container-catalog-element')
        name = data.find('div', class_='bxr-cloud-all').find('h1').text
        try:
            price = data.find('span', class_='bxr-market-current-price bxr-market-format-price 9').text
        except:
            price = 'Цена по запросу'
        description = data.find('div', class_='bxr-detail-tab-content').text
        src = 'https://mesopharm-shop.ru/' + data.find('a').get('href')
        print(name)
        yield name, price, description, src

def writer(array):
    book = xlsxwriter.Workbook('/Users/santa/Desktop/Cosmetics compain/Mesofarm/Mesofarm.xlsx')
    page_1 = book.add_worksheet('Mesofarm')

    headers = ['Наименование', 'Цена', "Описание", "Ссылка на фото товара", "Цена", "Примечание"]
    for col, h in enumerate(headers):
        page_1.write_string(0, col, h)

    page_1.set_column('A:A', 15)
    page_1.set_column('B:B', 22)
    page_1.set_column('C:C', 50)
    page_1.set_column('D:D', 25)
    page_1.set_column('E:E', 10)
    page_1.set_column('F:F', 30)

    row = 1
    column = 0

    for item in array():
        page_1.write(row, column, item[0])
        page_1.write(row, column + 1, item[1])
        page_1.write(row, column + 2, item[2])
        page_1.write(row, column + 3, item[3])
        # page_1.write(row, column + 4, item[4])
        row += 1

    book.close()

writer(array)



def main():
    get_first_url()
    get_next_url()
    get_cat_url()
    array()
    writer()
finish_time = time() - stat_time
print(f'Затраченное время на работу скрипта: {finish_time}')

if __name__ == '__main__':
    main()


