# -*- coding:utf-8 -*-
# @Ekira, 2017/7/27

import re, time
from os import path
from urllib2 import urlopen
from urllib import urlretrieve
from imgcheck import imgcheck
from drawwatermark import draw_watermark
from updatewallpaper import update_wallpaper


def __get_img(imgcfg):
    apiurl = "http://cn.bing.com/HPImageArchive.aspx?idx=0&n=1"
    content = str(urlopen(apiurl).read())
    url = re.search(r'<url>[^\s]*</url>', content).group(0)
    url = 'http://cn.bing.com' + url[5:-6]
    print "[IMAGE URL]:", url
    wallpaper = time.strftime("%Y.%m.%d-%H.%M.%S") + url[-4:]
    imgcfg["wppath"] = path.abspath(path.join(imgcfg["downloaddir"], wallpaper))
    urlretrieve(url, imgcfg["wppath"])
    print "[IMAGE GOT]:", imgcfg["wppath"]


def bingindex(imgcfg):
    if not path.isdir(imgcfg["downloaddir"]):
        os.makedirs(imgcfg["downloaddir"])
    __get_img(imgcfg)
    if not imgcheck(imgcfg):
        prerr("Can not parse this images")
    draw_watermark(imgcfg)
    update_wallpaper(imgcfg["wppath"])
