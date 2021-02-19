
# (c) Denis Ksolapov 2018
# License GPLv2 
import re
import time
import urllib

import httplib2
from requests import request
from bs4 import BeautifulSoup
import urllib.parse as urlparse

from Database import Database


class Parser:
    global image_count, extension

    quantity_image = 30
    print("количество запрашиваемых картинок: " + str(quantity_image))

    start_url = 'https://yandex.ru/images/search?text='
    text_search = "картинки для свободного скачивания"
    search = urllib.parse.quote(text_search)
    query = (start_url + search)
    print("Выдача картинок по запросу: " + text_search + "\n" + query)

    t = request('GET', query).text
    with open('index.xml', 'w', encoding='utf-8') as f:
        f.write(t)

    with open("index.xml", "r", encoding='utf-8') as f:
        contents = f.read()

        soup = BeautifulSoup(contents, 'lxml')

        title = soup.title
        for i in title:
            print(i)

    # получаем массив с ссылками на картинки
    mass_links = soup.find_all(href=re.compile(r'/images/search\?pos='))

    # чистим ссылки на картинки
    links = []
    for x in mass_links:
        x = str(x)
        x = urllib.parse.unquote(x)
        x = x.split('&')[1]
        x = x.split('?_cvc=')[0]
        x = x.split('amp;img_url=')[1]
        x = urllib.parse.unquote(x)
        links.append(x)

    # пробуем извлечь формат картинки!
    for i in links:
        result = re.findall(r'[.]\w{3}', i)

        # создаем словарь с расширениями
        extensions = {
            '.png': "png",
            '.jpe': "jpeg",
            '.jpg': "jpg"
        }

        # проверили на наличие в сорваре
        for x in result:
            if x in extensions:
                extension = extensions.get(x)
        # получили расширение из словаря

    # если количество картинок равно нулю, пишем что картинки не найдены
    if len(links) == 0:
        print("image not found")
    else:
        # иначе выводим количество картинок
        image_count = int(len(links))

    # если количество запрашиваемых картинок больше чем найдено, выводим сообщение
    if image_count < quantity_image:
        print("Нет столько картинок")
    else:
        # иначе сохраняем картинку
        if quantity_image > 1:

            mass_png = []
            mass_jpg = []
            mass_jpeg = []

            for i in links:
                result = re.findall(r'[.]\w{3}', i)
                # # создаем словарь с форматами
                extensions = {
                    '.png': ".png",
                    '.jpe': ".jpeg",
                    '.jpg': ".jpg"
                }
                # # проверили на наличие в сорваре
                for x in result:
                    if x in extensions:
                        # получили расширение из словаря
                        extension = extensions.get(x)

                if extension == ".png":
                    mass_png.append(i)

                if extension == ".jpg":
                    mass_jpg.append(i)

                if extension == ".jpeg":
                    mass_jpeg.append(i)

            try:
                num = -1
                for i in mass_jpg:
                    time.sleep(3)
                    num += 1
                    h = httplib2.Http('images/jpg/.cache')
                    response, content = h.request(links[num])
                    out = open('images/jpg/' + 'name_' + str(num + 1) + '.jpg', 'wb')
                    out.write(content)
                    out.close()
            except:
                print(IOError.filename)

            try:
                num = -1
                for i in mass_png:
                    time.sleep(3)
                    num += 1
                    h = httplib2.Http('images/png/.cache')
                    response, content = h.request(links[num])
                    out = open('images/png/' + 'name_' + str(num + 1) + '.png', 'wb')
                    out.write(content)
                    out.close()
            except:
                print(IOError.filename)

            try:
                num = -1
                for i in mass_jpeg:
                    time.sleep(3)
                    num += 1
                    h = httplib2.Http('images/jpeg/.cache')
                    response, content = h.request(links[num])
                    out = open('images/jpeg/' + 'name_' + str(num + 1) + '.jpeg', 'wb')
                    out.write(content)
                    out.close()
            except:
                print(IOError.filename)

    print("всего найдено картинок: " + str(image_count))
