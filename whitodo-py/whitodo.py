# -*- coding:utf-8 -*-
# environment: python 2.7, PIL, pypiwin32
# @Ekira, 2017/7/10
#
# Update
# @Ekira, 2017/7/27
# Fix "out of range" bug.
# Add function: cycling showing images from a directory.
# Add function: get/set wallpaper from bing's index image everyday.
# TODO: modebingindex.py, unsupport loopping everyday now.

import sys, os

from cfg import gen_config, load_config
from modesingle import single
from modecycle import cycle
from modebingindex import bingindex


if __name__ == '__main__':
    CONFIG_PATH = "./whitodo.cfg"
    if not os.path.exists(CONFIG_PATH):
        gen_config(CONFIG_PATH)        
        sys.exit()
    imgcfg = load_config(CONFIG_PATH)
    print imgcfg
    if imgcfg["mode"] == "mode-single":
        single(imgcfg)
    elif imgcfg["mode"] == "mode-cycle":
        cycle(imgcfg)
    elif imgcfg["mode"] == "mode-bingindex":
        bingindex(imgcfg)
    else:
        sys.exit()

