# -*- coding:utf-8 -*-
# @Ekira, 2017/7/27

import time
from os import path
from PIL import Image


# if the image is jpg, convert to bmp and return bmp path
# and the bmp file locates on the same as jpg file
def __conv2bmp(img_path, cachedir):
    wallpaper = time.strftime("%Y.%m.%d-%H.%M.%S") + ".bmp"
    bmp_path = path.abspath(path.join(cachedir, wallpaper))
    image = Image.open(img_path).save(bmp_path, "BMP")
    return bmp_path


def imgcheck(imgcfg):
    if len(imgcfg["wppath"]) < 5:
        return False
    if imgcfg["wppath"][-3:] == "jpg" or imgcfg["wppath"][-4:] == "jpeg"\
    or imgcfg["wppath"][-3:] == "JPG" or imgcfg["wppath"][-4:] == "JPEG"\
    or imgcfg["wppath"][-3:] == "png" or imgcfg["wppath"][-3:] == "PNG":
        imgcfg["wppath"] = __conv2bmp(imgcfg["wppath"], imgcfg["cachedir"])
    if imgcfg["wppath"][-3:] == "bmp" or imgcfg["wppath"][-3:] == "BMP":
        return True
    return False
