import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time
from datetime import datetime
import json_db as jdb
import pandas as pd
from sqlalchemy import engine as sql
from io import StringIO

import asyncio  # Даст нам async/await
import aiohttp  # Для асинхронного выполнения HTTP запросов
import aiofiles  # Дла асинхронного выполнения операций с файлами
import concurrent.futures  # Позволяет создать новый процесс
from multiprocessing import cpu_count  # Вернет количество ядер процессора
from math import floor  # Поможет разделить запросы между ядрами CPU
import aiohttp
import asyncio
import async_timeout

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
async def get_html(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x935')
    browser = webdriver.Chrome("C:/Users/slubo/Desktop/chromedriver.exe", chrome_options=options)
    browser.get(url)
    page_source = browser.page_source
    #user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    #session = requests.Session()
    #r = session.get(url, timeout=(3.05, 15), headers={
    #    'User-Agent': user_agent_val
    #})
    return page_source
    #print(r.status_code)
async def write_csv(data, file_name):
    async with aiofiles.open(file_name, 'a+', encoding = 'utf-8') as f:
        writer = csv.writer(f)
        await writer.writerow([data['url_resume']])

async def prepare_to_csv(url_resume):
    return {'url_resume': url_resume,}

async def get_page_url(html, step, file_name):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', class_ = 'resume-search-item')
    for i in range(step, len(items)-1, 4):
        url = items[i].find('div', class_='resume-search-item__header').find('a').get('href')
        prepare_csv = await prepare_to_csv(url)
        await write_csv(prepare_csv, file_name)
        #print(item.find('span', class_ = 'g-user-content').text)
        #print(item)
        pass


def psql_insert_copy(table, conn, keys, data_iter):
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ', '.join('"{}"'.format(k) for k in keys)
        if table.schema:
            table_name = '{}.{}'.format(table.schema, table.name)
        else:
            table_name = table.name

        sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(
            table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)
def AddDB():
    con = sql.create_engine('postgresql://postgres:12345@localhost:5432/vacancies')
    df = pd.read_csv('vacancy1.csv', encoding='utf-8')
    df.to_sql('Vacancy', con, index=False, schema='public', if_exists='append')


def start_scraping(url: str, step: int, file_name : str):
    html = asyncio.run(get_html(url))
    asyncio.run(get_page_url(html, step, file_name))


async def main():
    pattern = 'https://hh.ru/search/vacancy?fromSearchLine=true&text=frontend&area=1&search_field=name&page={}'
    new_pattern = 'https://hh.ru/search/vacancy?clusters=true&ored_clusters=true&search_field=name&enable_snippets=true&salary=&text=Frontend+%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%87%D0%B8%D0%BA&from=suggest_post&page={}&hhtmFrom=vacancy_search_list'
    NUM_PAGES = 50  # Суммарное количество страниц для скрапинга
    NUM_CORES = cpu_count()  # Количество ядер CPU (влкючая логические)
    PAGE_LINKS = [
        'https://hh.ru/search/resume?relocation=living_or_relocation&gender=unknown&text=Data+scientist&from=suggest_post&clusters=true&no_magic=true&ored_clusters=true&order_by=relevance&items_on_page=100&logic=normal&pos=full_text&exp_period=all_time&search_period=0&page={}&hhtmFrom=resume_search_result',
        'https://hh.ru/search/resume?professional_role=96&relocation=living_or_relocation&gender=unknown&text=Data+engineer&from=suggest_post&isDefaultArea=true&clusters=true&no_magic=true&ored_clusters=true&order_by=relevance&items_on_page=100&logic=normal&pos=full_text&exp_period=all_time&search_period=0&page={}&hhtmFrom=resume_search_result',
        'https://hh.ru/search/resume?professional_role=107&professional_role=73&relocation=living_or_relocation&gender=unknown&text=Product+Manager&from=suggest_post&isDefaultArea=true&clusters=true&no_magic=true&ored_clusters=true&order_by=relevance&items_on_page=100&logic=normal&pos=full_text&exp_period=all_time&search_period=0&page={}&hhtmFrom=resume_search_result',
        'https://hh.ru/search/resume?professional_role=3&relocation=living_or_relocation&gender=unknown&text=SMM+Manager&from=suggest_post&clusters=true&no_magic=true&ored_clusters=true&order_by=relevance&items_on_page=100&logic=normal&pos=full_text&exp_period=all_time&search_period=0&page={}&hhtmFrom=resume_search_result',
        'https://hh.ru/search/resume?area=1&professional_role=68&relocation=living_or_relocation&gender=unknown&text=Marketing+manager&from=suggest_post&isDefaultArea=true&clusters=true&no_magic=true&ored_clusters=true&order_by=relevance&items_on_page=100&logic=normal&pos=full_text&exp_period=all_time&search_period=0&page={}&hhtmFrom=resume_search_result',
        'https://hh.ru/search/resume?area=1&clusters=true&exp_period=all_time&logic=normal&no_magic=true&order_by=relevance&ored_clusters=true&pos=full_text&text=frontend&items_on_page=100&page={}&hhtmFrom=resume_search_result',
        'https://hh.ru/search/resume?text=Backend&from=suggest_post&clusters=true&area=1&professional_role=96&no_magic=true&ored_clusters=true&order_by=relevance&items_on_page=100&logic=normal&pos=full_text&exp_period=all_time&page={}&hhtmFrom=resume_search_result',
        'https://hh.ru/search/resume?area=1&professional_role=104&professional_role=113&professional_role=96&relocation=living_or_relocation&gender=unknown&text=DevOps&from=suggest_post&clusters=true&no_magic=true&ored_clusters=true&order_by=relevance&items_on_page=100&logic=normal&pos=full_text&exp_period=all_time&search_period=0&page={}&hhtmFrom=resume_search_result',
        'https://hh.ru/search/vacancy?search_field=name&text=Java+developer&clusters=true&ored_clusters=true&enable_snippets=true&from=suggest_post&page={}&hhtmFrom=vacancy_search_list',
        'https://hh.ru/search/vacancy?search_field=name&text=Android+developer&clusters=true&ored_clusters=true&enable_snippets=true&from=suggest_post&page={}&hhtmFrom=vacancy_search_list',
        'https://hh.ru/search/vacancy?search_field=name&text=.Net&clusters=true&ored_clusters=true&enable_snippets=true&page={}&hhtmFrom=vacancy_search_list',
    ]
    NUM_LINKS = [10, 10, 10, 10, 10, 10, 10, 8]
    NAME_FILES = [
        'Data_Science_resume.csv',
        'Data_Engineer_resume.csv',
        'Product_Manager_resume.csv',
        'SMM_Manager_resume.csv',
        'Marketing_Manager_resume.csv',
        'Frontend_Developer_resume.csv',
        'BackEnd_Developer_resume.csv',
        'DevOps_resume.csv',
    ]
    OUTPUT_FILE = "wiki_titles.csv"  # Файл для добавления заголовков

    for file_name in NAME_FILES:
        prepare_csv = await prepare_to_csv(
            'url_resume')
        await write_csv(prepare_csv, file_name)
    pages = [0, 1, 2, 3]
    PAGES_PER_CORE = floor(NUM_PAGES / NUM_CORES)
    # Для нашего последнего ядра
    futures = []  # To store our futures
    all_time_program = datetime.now()
    print(time.ctime(time.time()))
    for i in range(0, len(PAGE_LINKS)):
        all_time_per_file = datetime.now()
        print('Название области: ', NAME_FILES[i][0:-4], '\n')
        for j in range(0, NUM_LINKS[i]):
            now = datetime.now()
            url = PAGE_LINKS[i].format((str(j)))
            with concurrent.futures.ProcessPoolExecutor(NUM_CORES) as executor:
                for g in range(NUM_CORES):
                    new_future = executor.submit(
                        start_scraping,  # Function to perform
                        # v Arguments v
                        url=url,
                        step = pages[g],
                        file_name = NAME_FILES[i]
                    )
            now_2 = datetime.now() - now
            print('Cтраниц пройдено: ', j+1 , 'Время прохождения: ', now_2, ' (мин.)', '\n')
        all_time_per_file_2 = datetime.now() - all_time_per_file
        print('Время для всей области: ', all_time_per_file_2,' (мин.)', '\n')
        print('-------------------------------', '\n')
    print('\n')
    all_time_program_2 = datetime.now() - all_time_program
    print('Общее время работы: (мин.)',all_time_program_2, '\n')
        #get_page_url(get_html(url))
        #get_page_data(get_html(url), url)

    #url = 'https://hh.ru/vacancy/48752041?from=vacancy_search_list&query=frontend'
    #url = 'https://hh.ru/vacancy/48091208?from=vacancy_search_list&query=frontend'
    #get_page_data(get_html(url), url)
    # Use a breakpoint in the code line below to debug your script.
    # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   asyncio.run(main())
