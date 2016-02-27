# -*- coding: utf-8 -*-
"""
В данном примере, мы найдем треки по запросу Steve Roach
и получим информацию по каждому из треков
"""

import pyyandexmusic
ym = pyyandexmusic.YandexMusic()
resp = ym.search("Steve Roach")
i = 0

for track in resp["tracks"]["items"]:
    i += 1
    info = ym.get_track(track["id"])["track"]
    print(str(i) + ") " + track["artists"][0]["name"] + " - " + track["title"] + " / id = " + str(track["id"]) +
          " / " + info["albums"][0]["title"])
