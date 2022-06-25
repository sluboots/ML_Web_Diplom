import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time
import json_db as jdb
import pandas as pd
from sqlalchemy import engine as sql
from io import StringIO
import aiohttp
import asyncio
import async_timeout

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def get_html(url):
    #options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    #options.add_argument('window-size=1920x935')
    browser = webdriver.Chrome("C:/Users/slubo/Desktop/chromedriver.exe")
    browser.get(url)
    time.sleep(0.25)
    #user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    #session = requests.Session()
    #r = session.get(url, timeout=(3.05, 15), headers={
    #    'User-Agent': user_agent_val
    #})

    return browser.page_source
    #print(r.status_code)
def write_csv(data):
    with open('vacancy1.csv', 'a', encoding = 'utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([data['name_vacancy'],
                         data['salary'],
                         data['name_company'],
                         data['location_company'],
                         data['location_company_link'],
                         data['required_experience'],
                         data['busyness'],
                         data['description'],
                         data['key_skills'],
                         data['vacancy_url']])

def prepare_to_csv(vacancy_url, name_vacancy, salary, name_company, location_company, location_company_link, required_experience, busyness, description, key_skills):
    return {'name_vacancy': name_vacancy,
            'salary': salary,
            'name_company': name_company,
            'location_company': location_company,
            'location_company_link': location_company_link,
            'required_experience': required_experience,
            'busyness':  busyness,
            'description': description,
            'key_skills': key_skills,
            'vacancy_url': vacancy_url}

def get_page_data(html, url):
    soup = BeautifulSoup(html, 'lxml')
    vacancy_url = url
    try:
        name_vacancy = soup.find('h1').text
    except:
        name_vacancy = ''
    try:
        salary = soup.find('div', class_='vacancy-salary').text
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
        find_key_skills = soup.find('div', class_='bloko-tag-list').find('div').find_all('div', class_='bloko-tag_inline')
        #print(find_key_skills)
        for key_skill in find_key_skills:
            #print(key_skill.text)
            key_skills += key_skill.text + ' '
        key_skills = key_skills[0:len(key_skills)-2]
        #print(key_skills)
    except:
        key_skills = ''
    write_csv(prepare_to_csv(vacancy_url, name_vacancy, salary, name_company, location_company, location_company_link, required_experience, busyness, description, key_skills))

def get_page_url(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', class_ = 'vacancy-serp-item')
    print(len(items))
    for item in items:
        url = item.find('div', class_='vacancy-serp-item__row_header').find('a').get('href')
        get_page_data(get_html(url), url)
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



def main():
    pattern = 'https://hh.ru/search/vacancy?fromSearchLine=true&text=frontend&area=1&search_field=name&page={}'
    write_csv(prepare_to_csv(
        'vacancy_url',
        'name_vacancy',
        'salary',
        'name_company',
        'location_company',
        'location_company_link',
        'required_experience',
        'busyness',
        'description',
        'key_skills'))
    for i in range(0, 30):
        url = pattern.format((str(i)))
        get_page_url(get_html(url))
        #get_page_data(get_html(url), url)

    #url = 'https://hh.ru/vacancy/48752041?from=vacancy_search_list&query=frontend'
    #url = 'https://hh.ru/vacancy/48091208?from=vacancy_search_list&query=frontend'
    #get_page_data(get_html(url), url)
    # Use a breakpoint in the code line below to debug your script.
    # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    AddDB()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
