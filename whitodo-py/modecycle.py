# -*- coding:utf-8 -*-
# @Ekira, 2017/7/27

import os, time, random
from os import path
from imgcheck import imgcheck
from drawwatermark import draw_watermark
from updatewallpaper import update_wallpaper


def __get_next(tgtimgs, israndom, cnt):
    if israndom == "no" or israndom == "NO":
        return tgtimgs[cnt % len(tgtimgs)]
    return random.sample(tgtimgs, 1)[0]


def cycle(imgcfg):
    srcimgs = os.listdir(imgcfg["srcdir"])
    tgtimgs = []
    for i in srcimgs:
        i = path.abspath(path.join(imgcfg["srcdir"], i))
        imgcfg["wppath"] = i
        if imgcheck(imgcfg):
            draw_watermark(imgcfg)
            tgtimgs.append(imgcfg["wppath"])
        time.sleep(1)
    cnt = 0
    while True:
        update_wallpaper(__get_next(tgtimgs, imgcfg["random"], cnt))
        cnt += 1
        time.sleep(int(imgcfg["switchtime"]) * 60)

