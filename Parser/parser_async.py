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
        await writer.writerow([data['name_vacancy'],
                         data['salary'],
                         data['name_company'],
                         data['location_company'],
                         data['location_company_link'],
                         data['required_experience'],
                         data['busyness'],
                         data['description'],
                         data['key_skills'],
                         data['vacancy_url']])

async def prepare_to_csv(vacancy_url, name_vacancy, salary, name_company, location_company, location_company_link, required_experience, busyness, description, key_skills):
    return  {'name_vacancy': name_vacancy,
            'salary': salary,
            'name_company': name_company,
            'location_company': location_company,
            'location_company_link': location_company_link,
            'required_experience': required_experience,
            'busyness':  busyness,
            'description': description,
            'key_skills': key_skills,
            'vacancy_url': vacancy_url}

async def get_page_data(html, url, file_name):
    soup = BeautifulSoup(html, 'lxml')
    vacancy_url = url
    try:
        name_vacancy = soup.find('h1').text
    except:
        name_vacancy = ''
    try:
        salary = soup.find('span', class_='bloko-header-2 bloko-header-2_lite').text
    except:
        salary = ''
    try:
        name_company = soup.find('a', class_='vacancy-company-name').text
    except:
        name_company = ''
    try:
        location_company = soup.find('div', class_='vacancy-company').find('a', attrs={'target': '_blank', 'data-qa': 'vacancy-view-link-location'}).text
        #print(location_company)
    except:
        location_company = soup.find('div', class_='vacancy-company').find('p', attrs={'data-qa': 'vacancy-view-location'}).text
        #print(location_company)
    try:
        location_company_link = soup.find('div', class_='vacancy-company').find('a', attrs={'target': '_blank', 'data-qa': 'vacancy-view-link-location'}).get('href')
        location_company_link = 'https://hh.ru' + location_company_link
        #print(location_company_link)
    except:
        location_company_link = ''
        #print(location_company_link)
    try:
        required_experience = soup.find('div', class_='vacancy-description').find('p').text
            #find_parent('span', attrs={'data-qa': 'vacancy-experience'}).text
        #print(required_experience)
    except:
        required_experience = ''
        #print(1)

    try:
        busyness = soup.find('div', class_='vacancy-description').find('p', attrs={'data-qa': 'vacancy-view-employment-mode'}).text
        #print(busyness)
    except:
        busyness = ''
    try:
        description = soup.find('div', class_='g-user-content').text
    except:
        description = '0'
    try:
        key_skills = ''
        find_key_skills = soup.find('div', class_='bloko-tag-list').find_all('div', attrs={'data-qa': 'bloko-tag bloko-tag_inline skills-element'})
        #print(find_key_skills)
        for key_skill in find_key_skills:
            #print(key_skill.text)
            key_skills += key_skill.text + ' '
        key_skills = key_skills[0:len(key_skills)-2]
        #print(key_skills)
    except:
        key_skills = ''
    prepare_csv = await prepare_to_csv(vacancy_url, name_vacancy, salary, name_company, location_company, location_company_link, required_experience, busyness, description, key_skills)
    await write_csv(prepare_csv, file_name)

async def get_page_url(html, step, file_name):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', class_ = 'vacancy-serp-item')
    for i in range(step, len(items)-1, 4):
        url = items[i].find('div', class_='vacancy-serp-item-body').find('a').get('href')
        new_html = await get_html(url)
        await get_page_data(new_html, url, file_name)
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
    NUM_PAGES = 50  # Суммарное количество страниц для скрапинга
    NUM_CORES = cpu_count()  # Количество ядер CPU (влкючая логические)
    PAGE_LINKS = [
        'https://hh.ru/search/vacancy?search_field=name&search_field=company_name&text=machine+learning&clusters=true&enable_snippets=true&ored_clusters=true&from=SIMILAR_QUERY&hhtmFromLabel=SIMILAR_QUERY&page={}&hhtmFrom=vacancy_search_list',
        'https://hh.ru/search/vacancy?search_field=name&text=data+scientist&page={}&hhtmFrom=vacancy_search_catalog',
        'https://hh.ru/search/vacancy?search_field=name&text=Data+analyst&clusters=true&ored_clusters=true&enable_snippets=true&from=suggest_post&page={}&hhtmFrom=vacancy_search_list',
        'https://hh.ru/search/vacancy?search_field=name&text=Data+engineer&clusters=true&ored_clusters=true&enable_snippets=true&from=suggest_post&page={}&hhtmFrom=vacancy_search_list',
        'https://hh.ru/search/vacancy?search_field=name&text=Product+manager&clusters=true&ored_clusters=true&enable_snippets=true&from=suggest_post&page={}&hhtmFrom=vacancy_search_list',
        'https://hh.ru/search/vacancy?search_field=name&text=Smm+manager&clusters=true&ored_clusters=true&enable_snippets=true&from=suggest_post&page={}&hhtmFrom=vacancy_search_list',
        'https://hh.ru/search/vacancy?search_field=name&text=Marketing+manager&clusters=true&ored_clusters=true&enable_snippets=true&page={}&hhtmFrom=vacancy_search_list',
        'https://hh.ru/search/vacancy?search_field=name&text=Frontend&from=suggest_post&page={}&hhtmFrom=vacancy_search_list',
        'https://hh.ru/search/vacancy?search_field=name&text=Backend&clusters=true&ored_clusters=true&enable_snippets=true&page={}&hhtmFrom=vacancy_search_list',
        'https://hh.ru/search/vacancy?search_field=name&text=DevOps&clusters=true&ored_clusters=true&enable_snippets=true&page={}&hhtmFrom=vacancy_search_list',
        'https://hh.ru/search/vacancy?search_field=name&text=Java+developer&clusters=true&ored_clusters=true&enable_snippets=true&from=suggest_post&page={}&hhtmFrom=vacancy_search_list',
        'https://hh.ru/search/vacancy?search_field=name&text=Android+developer&clusters=true&ored_clusters=true&enable_snippets=true&from=suggest_post&page={}&hhtmFrom=vacancy_search_list',
        'https://hh.ru/search/vacancy?search_field=name&text=.Net&clusters=true&ored_clusters=true&enable_snippets=true&page={}&hhtmFrom=vacancy_search_list',
    ]
    NUM_LINKS = [2, 6, 6, 7, 24, 19, 40, 40, 35, 30, 40, 19, 17]
    NAME_FILES = [
        'Data_Science.csv',
        'Data_Science.csv',
        'Data_Science.csv',
        'Data_Engineer.csv',
        'Product_Manager.csv',
        'SMM_Manager.csv',
        'Marketing_Manager.csv',
        'Frontend_Developer.csv',
        'BackEnd_Developer.csv',
        'DevOps.csv',
        'Java_Developers.csv',
        'Android_Developer.csv',
        'dotNet.csv',
    ]
    '''
    for file_name in NAME_FILES:
        prepare_csv = await prepare_to_csv(
            'vacancy_url',
            'name_vacancy',
            'salary',
            'name_company',
            'location_company',
            'location_company_link',
            'required_experience',
            'busyness',
            'description',
            'key_skills')
        await write_csv(prepare_csv, file_name)
        '''
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

