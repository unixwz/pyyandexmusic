# -*- coding: utf-8 -*-
"""
Модуль для работы с Yandex.Music при помощи неофициального API
Автор: Дмитрий Буряков (unixwz.github.io)

Возможности модуля:
1) Search(keyword, search_type, offset)
    Поиск по ключевому слову с заданным типом и смещением страниц.
    - keyword - ключевое слово
    - search_type - тип поиска
        - tracks - треки
        - albums - альбомы
        - artists - исполнитель
    - offset - смещение (в страницах)
        к примеру offset=1 вернёт результаты расположенные на 1 странице,
        offset=2 вернёт результаты расположенные на 2 странице,
        при этом следует учитывать, что нумерация начинается с нуля.
        Для того, что бы определить присутствует ли разбиение на страницы -
        достаточно проверить общее кол-во результатов полученных в результате
        вызова метода search (кол-во хранится в перменной YandexMusic.page_count).
        Если YandexMusic.page_count > 100, то разбиение на страницы присутвует.


TODO:
- получение прямой ссылки на аудио
"""

import httplib2
import json


class YandexMusic(object):

    def __init__(self):
        self.base_url = "https://music.yandex.ru/handlers/"
        self.api_url = "https://music.yandex.ru/api/v2.0/"
        self.headers = {"Host": "music.yandex.ru",
                        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Cookie": open("cookie.txt").read(),  # файл с куками
                        "Connection": "keep-alive",
                        "Cache-Control": "max-age=0"}

        self.key = "XGRlBW9FXlekgbPrRHuSiA"
        self.http = httplib2.Http(".cache")

    def search(self, keyword, search_type="tracks", offset=0):
        keyword = keyword.replace(" ", "+")
        # заменяем пробел "+", для HTTP запроса

        (resp, content) = self.http.request(
            self.base_url + "music-search.jsx?text=" + keyword + "&type=" + search_type + "&page=" + str(offset) + "",
            headers=self.headers)

        return json.loads(content)

    def get_track(self, track_id):
        (resp, content) = self.http.request(self.base_url + "track.jsx?track=" + str(track_id) + "&lang=ru",
                                            headers=self.headers)
        return json.loads(content)

    def get_author(self, artist_id):
        (resp, content) = self.http.request(self.base_url + "artist.jsx?artist=" + str(artist_id) + "&lang=ru",
                                            headers=self.headers)
        return json.loads(content)

    def get_album(self):
        pass

    def get_link(self):
        pass

    def get_lyrics(self):
        pass
