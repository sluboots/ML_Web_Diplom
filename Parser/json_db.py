import requests
import json
import time
import os
import pandas as pd
from sqlalchemy import engine as sql
from IPython import display


def getPage(page = 0):
    """
    Создаем метод для получения страницы со списком вакансий.
    Аргументы:
        page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
    """

    # Справочник для параметров GET-запроса
    params = {
        'text': 'NAME:FrontEnd',  # Текст фильтра. В имени должно быть слово "Аналитик"
        'area': 1,  # Поиск ощуществляется по вакансиям города Москва
        'page': page,  # Индекс страницы поиска на HH
        'per_page': 100  # Кол-во вакансий на 1 странице
    }

    req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
    data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    return data


# Считываем первые 2000 вакансий
def getJson():

    for page in range(0, 20):

        # Преобразуем текст ответа запроса в справочник Python
        jsObj = json.loads(getPage(page))

        # Сохраняем файлы в папку {путь до текущего документа со скриптом}\docs\pagination
        # Определяем количество файлов в папке для сохранения документа с ответом запроса
        # Полученное значение используем для формирования имени документа
        nextFileName = './docs/pagination/{}.json'.format(len(os.listdir('./docs/pagination')))

        # Создаем новый документ, записываем в него ответ запроса, после закрываем
        f = open(nextFileName, mode='w', encoding='utf8')
        f.write(json.dumps(jsObj, ensure_ascii=False))
        f.close()

        # Проверка на последнюю страницу, если вакансий меньше 2000
        if (jsObj['pages'] - page) <= 1:
            break

        # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать
        time.sleep(0.25)

    print('Старницы поиска собраны')
    for fl in os.listdir('./docs/pagination'):

        # Открываем файл, читаем его содержимое, закрываем файл
        f = open('./docs/pagination/{}'.format(fl), encoding='utf8')
        jsonText = f.read()
        f.close()

        # Преобразуем полученный текст в объект справочника
        jsonObj = json.loads(jsonText)

        # Получаем и проходимся по непосредственно списку вакансий
        for v in jsonObj['items']:
            # Обращаемся к API и получаем детальную информацию по конкретной вакансии
            req = requests.get(v['url'])
            data = req.content.decode()
            req.close()

            # Создаем файл в формате json с идентификатором вакансии в качестве названия
            # Записываем в него ответ запроса и закрываем файл
            fileName = './docs/vacancies/{}.json'.format(v['id'])
            f = open(fileName, mode='w', encoding='utf8')
            f.write(data)
            f.close()

            time.sleep(0.25)

    print('Вакансии собраны')

def AddDB():
    IDs = []  # Список идентификаторов вакансий
    names = []  # Список наименований вакансий
    descriptions = []  # Список описаний вакансий
    url = []
    snippet_requirement = []
    snippet_responsibility = []

    # Создаем списки для столбцов таблицы skills
    skills_vac = []  # Список идентификаторов вакансий
    skills_name = []  # Список названий навыков

    # В выводе будем отображать прогресс
    # Для этого узнаем общее количество файлов, которые надо обработать
    # Счетчик обработанных файлов установим в ноль
    cnt_docs = len(os.listdir('./docs/vacancies'))
    i = 0

    # Проходимся по всем файлам в папке vacancies
    for fl in os.listdir('./docs/vacancies'):

        # Открываем, читаем и закрываем файл
        f = open('./docs/vacancies/{}'.format(fl), encoding='utf8')
        jsonText = f.read()
        f.close()

        # Текст файла переводим в справочник
        jsonObj = json.loads(jsonText)

        # Заполняем списки для таблиц
        IDs.append(jsonObj['id'])
        names.append(jsonObj['name'])
        descriptions.append(jsonObj['description'])
        url.append(jsonObj['alternate_url'])

        # Т.к. навыки хранятся в виде массива, то проходимся по нему циклом
        for skl in jsonObj['key_skills']:
            skills_vac.append(jsonObj['id'])
            skills_name.append(skl['name'])

        for snippet in jsonObj['snippet']:
            snippet_requirement.append(snippet['requirement'])
            snippet_responsibility.append(snippet['responsibility'])
        # Увеличиваем счетчик обработанных файлов на 1, очищаем вывод ячейки и выводим прогресс
        i += 1
        display.clear_output(wait=True)
        display.display('Готово {} из {}'.format(i, cnt_docs))
    # Создадим соединение с БД
    eng = sql.create_engine('postgresql://postgres:12345@localhost:5432/sql_for_study')
    conn = eng.connect()
    # Создаем пандосовский датафрейм, который затем сохраняем в БД в таблицу vacancies
    df = pd.DataFrame({'id': IDs, 'name': names, 'description': descriptions, 'requirement': snippet_requirement, 'responsibility': snippet_responsibility, 'url': url})
    df.to_sql('vacancies', conn, schema='public', if_exists='append', index=False)
    # Тоже самое, но для таблицы skills
    df = pd.DataFrame({'vacancy': skills_vac, 'skill': skills_name})
    df.to_sql('skills', conn, schema='public', if_exists='append', index=False)
    # Закрываем соединение с БД
    conn.close()
    # Выводим сообщение об окончании программы
    display.clear_output(wait=True)
    display.display('Вакансии загружены в БД')

def main():
  AddDB()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
