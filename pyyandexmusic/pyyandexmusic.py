# -*- coding: utf-8 -*-
"""
Модуль для работы с Yandex.Music при помощи неофициального API
Автор: Дмитрий Буряков (unixwz.github.io)
"""

import httplib2
import json
import math
import hashlib


class YandexMusic(object):
    def __init__(self):
        self.base_url = "https://music.yandex.ru/handlers/"
        self.api_url = "https://music.yandex.ru/api/v2.0/handlers/"
        self.headers = {
            "Host": "music.yandex.ru",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Cookie": open("cookie.txt").read(),  # файл с куками
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0"}

        self.storage_headers = {
            "Host": "storage.mds.yandex.net",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Cookie": open("cookie.txt").read(),
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0"}

        self.key = "XGRlBW9FXlekgbPrRHuSiA"
        self.http = httplib2.Http(".cache")

    def search(self, keyword, search_type="tracks", offset=0):
        keyword = keyword.replace(" ", "+")
        (resp, content) = self.http.request(
            self.base_url + "music-search.jsx?text=" + keyword + "&type=" + search_type + "&page=" + str(offset) + "",
            headers=self.headers)

        return json.loads(content)

    def get_page_count(self, keyword, search_type="tracks"):
        keyword = keyword.replace(" ", "+")
        (resp, content) = self.http.request(
            self.base_url + "music-search.jsx?text=" + keyword + "&type=" + search_type + "", headers=self.headers)
        content = json.loads(content)
        page_count = int(math.ceil(float(content["pager"]["total"]) / 100))
        # определяем кол-во страниц на которые разбит найденный контент
        return page_count

    def get_track(self, track_id):
        (resp, content) = self.http.request(self.base_url + "track.jsx?track=" + str(track_id) + "&lang=ru",
                                            headers=self.headers)
        return json.loads(content)

    def get_artist(self, artist_id):
        (resp, content) = self.http.request(self.base_url + "artist.jsx?artist=" + str(artist_id) + "&lang=ru",
                                            headers=self.headers)
        return json.loads(content)

    def get_artist_tracks(self, artist_id):
        # получение всех треков исполнителя
        (resp, content) = self.http.request(
            self.base_url + "artist.jsx?artist=" + str(artist_id) + "&lang=ru&what=tracks",
            headers=self.headers)
        return json.loads(content)

    def get_album(self, album_id):
        (resp, content) = self.http.request(self.base_url + "album.jsx?album=" + str(album_id) + "&lang=ru",
                                            headers=self.headers)
        return json.loads(content)

    def get_download_link(self, track_id):
        storage_info = self.__get_storage_info__(track_id)
        h = hashlib.md5()
        h.update(self.key + storage_info["path"][1:100] + storage_info["s"])
        hash = h.hexdigest()  # hash для обращения к хранилищу

        src_url = "https://" + storage_info["host"] + "/get-mp3/" + hash + "/" + storage_info["ts"] + \
                  storage_info["path"] + "?track-id=" + str(track_id)

        return src_url

    def get_lyrics(self):
        pass

    def __get_storage_info__(self, track_id):
        track = self.get_track(track_id)
        (track_info_resp, track_info_content) = self.http.request(
            self.api_url + "track/" + str(track_id) + ":" + str(track["track"]["albums"][0]["id"]) +
            "/download/m?hq=0&external-domain=music.yandex.ru""&format=json", headers=self.headers)

        (storage_info_resp, storage_info_content) = self.http.request(
            json.loads(track_info_content)["src"] + "&format=json", headers=self.storage_headers)

        return json.loads(storage_info_content)
