import time
# import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup
# from time import sleep
# import xlsxwriter



start_time = time.time()
cosmet_url = []




async def get_page_data(session, category: str, page_id: int) -> str:
    # headers = {'User-Agent':
    #                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

    url = f'https://mesopharm-shop.ru/catalog/{category}'
    # if page_id:
    #     url = f'https://mesopharm-shop.ru/catalog/{category}/?page={page_id}'
    # else:
    #     url = f'https://mesopharm-shop.ru/catalog/{category}/'
    async with session.get(url) as resp:
        # assert resp.status == 200
        # print(f'get url: {url}')

        resp_text = resp.text()
        soup = BeautifulSoup(await resp_text, "lxml")
        data = soup.find_all('table', class_='bxr-element-container')
        for i in data:
            html = i.find('a').get('href')
            cosmet_url.append(html)
            print(cosmet_url)


    # async with session.get('https://mesopharm-shop.ru' + str(cosmet_url)) as response:
    #
    #     soup = BeautifulSoup(await response.text(), "lxml")
    #     data = soup.find('div', class_='col-xl-12 col-xs-12 bxr-container-catalog-element')
    #     name = data.find('div', class_='bxr-cloud-all').find('h1').text.strip()
    #     try:
    #         price = data.find('div', class_='bxr-detail-price').text
    #     except:
    #         price = 'Цена по запросу'
    #     description = data.find('div', class_='bxr-detail-tab-content').text.strip('\n').strip('')
    #     src = 'https://mesopharm-shop.ru/' + data.find('a').get('href')
    #
    #     print(name, src)
    #     # yield name, price, description, src
    #
    #
    #     # cosmetics_data.append(await resp_text)


async def load_site_data():

    categories_list = ['_mesopeptide/', '_nucleospire/', 'inektsionnye_preparaty_i_aktivnye_kontsentraty_dlya_mezoterapii/', '_mesopharm_professional/',
                       '_hinoki_clinical/', '_mesopharm_simple_care/', 'konturnaya_plastika/', '_mesopharm_gentest/', 'khimicheskie_pilingi/',
                       'maski_dlya_professionalnogo_ukhoda/', 'catalog/raskhodnye_materialy/', 'polidioksanonovye_sterilnye_mezoniti/'
                       ]
    async with aiohttp.ClientSession(trust_env=True) as session:
        tasks = []
        for cat in categories_list:
            for page_id in range(100):
                task = asyncio.create_task(get_page_data(session, cat, page_id))
                tasks.append(task)
                # process text and do whatever we need...
        await asyncio.gather(*tasks)


asyncio.run(load_site_data())

end_time = time.time() - start_time
# print(all_data)
print(f"\nExecution time: {end_time} seconds")