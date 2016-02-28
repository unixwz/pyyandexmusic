# -*- coding: utf-8 -*-
"""
В данном примеры мы получим прямую ссылку на трек
и сохраним его на нашем ПК
"""

import pyyandexmusic

ym = pyyandexmusic.YandexMusic()
ym.get_download_link(3699871)