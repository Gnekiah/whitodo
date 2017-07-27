# -*- coding:utf-8 -*-
# @Ekira, 2017/7/27

from imgcheck import imgcheck
from drawwatermark import draw_watermark
from updatewallpaper import update_wallpaper


def single(imgcfg):
    imgcfg["wppath"] = imgcfg["srcpath"]
    if not imgcheck(imgcfg):
        prerr("Can not parse this images")
    draw_watermark(imgcfg)
    update_wallpaper(imgcfg["wppath"])
