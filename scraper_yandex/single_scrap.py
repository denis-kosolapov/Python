# License GPLv2 
import re
import time
import urllib
import httplib2
from requests import request
from bs4 import BeautifulSoup
import urllib.parse as urlparse
import random
from Database import Database

massive = Database()
data = massive.myresult()
for stroke in data:
    sec = random.randint(15, 20)
    time.sleep(sec)
    for text_search in stroke:
        # это глобальные переменные
        global image_count, extension
        quantity_image = 1
        print("количество запрашиваемых картинок: " + str(quantity_image))
        # здесь создается ссылка для адресной строки
        # по которой будет происходить переход на страницу с результатами поиска
        # Это начало ссылки, оно не меняется
        start_url = 'https://yandex.ru/images/search?text='
        # это текст запроса, он меняется
        # text_search = "Валвир табл плен.об 500мг N10 ИСЛАНДИЯ"
        # это шифрование ссылки, чтобы яндекс ее скушал как свою
        search = urllib.parse.quote(text_search)
        # складываем полученый результат )
        query = (start_url + search)
        print("Выдача картинок по запросу: " + text_search + "\n" + query)
        # записываем полученый xml в файл
        t = request('GET', query).text
        with open('index.xml', 'w', encoding='utf-8') as f:
            f.write(t)
        # читаем полученый xml файл
        with open('index.xml', "r", encoding='utf-8') as f:
            contents = f.read()
            urllib.parse.unquote(contents)
        # подключаем BS4
        soup = BeautifulSoup(contents, 'lxml')
        # Выводим заголовок страницы (Яндекс.Картинки)
        title = soup.title
        for i in title:
            print(i)
            # if i == "":
            #     exit()
        # получаем массив с ссылками на картинки, регулярное выражение для поиска
        # mass_links = soup.find_all(href=re.compile(r'/images/search\?pos='))
        mass = soup.find_all(href=re.compile("[.]jpg"))
        # чистим ссылки на картинки, из xml файла
        links = []
        for text in mass:
            text = str(text)
            text2 = (text.split('=')[4])
            text3 = text2.split('&')[0]
            text4 = (urllib.parse.unquote(text3))
            links.append(text4)
        num = -1
        if quantity_image == 1:
            time.sleep(3)
            for i in range(quantity_image):
                num += 1
                try:
                    # сначала сохраняем кэш картинки, с указанием расширения и пути у кэшу
                    h = httplib2.Http('image/' + text_search + '/.cache')
                    # записываем в скобки переменную со ссылкой на картинку
                    response, content = h.request(links[num])
                    # скачиваем картинку с расширением картинки и текстом поиска
                    # стоит заметить, что если скачивается больше одной картинки,
                    # то имя картинки нужно тоже менять, иначе она просто перезапишется n-раз
                    out = open('image/' + text_search + '.jpg', 'wb')
                    out.write(content)
                    out.close()
                except IOError:
                    print(IOError.filename)

                # THE END :)

