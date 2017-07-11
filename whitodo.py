# -*- coding:utf-8 -*-
# environment: python 2.7, PIL, pypiwin32
# @Ekira, 2017/7/10

from os import path
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageEnhance
import ConfigParser
import sys, os
import win32api, win32con, win32gui, time


# print error and exit
def prerr(err):
    print "[ERROR]", err
    sys.exit()

# print warning
def prwarn(warn):
    print "[WARNING]", warn

# print message
def prmsg(msg):
    print "[MESSAGE]", msg


# set register and update wallpaper
def update_wallpaper(wallpaper, style="2", tile="0"):
    regkey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, 
            "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(regkey,"WallpaperStyle",0,win32con.REG_SZ,style)
    win32api.RegSetValueEx(regkey,"TileWallpaper",0,win32con.REG_SZ,tile)
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, wallpaper, 
            win32con.SPIF_SENDWININICHANGE)


# if the image is jpg, convert to bmp and return bmp path
# and the bmp file locates on the same as jpg file
def convert2bmp(img_path):
    wallpaper = time.strftime("%Y.%m.%d-%H.%M.%S") + ".bmp"
    bmp_path = path.abspath(path.join(path.dirname(img_path), wallpaper))
    image = Image.open(img_path).save(bmp_path, "BMP")
    return bmp_path


# draw watermark
def draw_watermark(imgcfg):
    img = Image.open(imgcfg["path"]).convert("RGB")
    # calculate mask RGBA for using white mask or black mask
    imgray = img.convert("1").load()
    cntgray = 0
    maskrgba = [None, None]
    for i in range(img.width): 
        for j in range(img.height):
            if imgray[i,j] == 0: cntgray += 1
    if cntgray < (img.width * img.height / 2):
        maskrgba[0] = (0, 0, 0, 35)
        maskrgba[1] = (0, 0, 0, 95)
    else:
        maskrgba[0] = (255, 255, 255, 35)
        maskrgba[1] = (255, 255, 255, 95)

    # draw watermark
    wmback = Image.new("RGBA", img.size, (0,0,0,0))
    wmdraw = ImageDraw.Draw(wmback, "RGBA")
    sfont = ImageFont.truetype(imgcfg["sfont"], int(imgcfg["sfontsize"]))
    scolor = ImageColor.getrgb(imgcfg["sfontcolor"])
    afont = ImageFont.truetype(imgcfg["afont"], int(imgcfg["afontsize"]))
    acolor = ImageColor.getrgb(imgcfg["afontcolor"])
    bfont = ImageFont.truetype(imgcfg["bfont"], int(imgcfg["bfontsize"]))
    bcolor = ImageColor.getrgb(imgcfg["bfontcolor"])
    cfont = ImageFont.truetype(imgcfg["cfont"], int(imgcfg["cfontsize"]))
    ccolor = ImageColor.getrgb(imgcfg["cfontcolor"])
    dfont = ImageFont.truetype(imgcfg["dfont"], int(imgcfg["dfontsize"]))
    dcolor = ImageColor.getrgb(imgcfg["dfontcolor"])
    texts = []
    for i in imgcfg["content"]:
        i = unicode(i,"utf-8")
        if len(i) < 3:
            texts.append((i, dfont, dcolor))
            continue
        if i[:3] == "[S]" or i[:3] == "[s]":
            texts.append((i[3:], sfont, scolor))
        elif i[:3] == "[A]" or i[:3] == "[a]":
            texts.append((i[3:], afont, acolor))
        elif i[:3] == "[B]" or i[:3] == "[b]":
            texts.append((i[3:], bfont, bcolor))
        elif i[:3] == "[C]" or i[:3] == "[c]":
            texts.append((i[3:], cfont, ccolor))
        elif i[:3] == "[D]" or i[:3] == "[d]":
            texts.append((i[3:], dfont, dcolor))
        else:
             texts.append((i, dfont, dcolor))
             
    # calculate mask size
    maskwidth = 0
    maskheight = 0
    for i in texts:
        tmp_size = i[1].getsize(i[0])
        maskwidth = max(maskwidth,tmp_size[0])
        maskheight += tmp_size[1]
    # calculate pos and do draw
    if imgcfg["endmargin"] == "0,0":
        textpos = imgcfg["startpos"].split(",")
        textpos = [int(textpos[0]), int(textpos[1])]
    else:
        textpos = imgcfg["endmargin"].split(",")
        textpos = [img.width-int(textpos[0]), img.height-int(textpos[1])]
        textpos = [textpos[0]-maskwidth, textpos[1]-maskheight]
        print textpos
    maskAX1 = textpos[0] - 50
    maskAY1 = textpos[1] - 50
    maskAX2 = maskAX1 + maskwidth + 100
    maskAY2 = maskAY1 + maskheight + 100
    maskBX1 = maskAX1 + 20
    maskBY1 = maskAY1 + 20
    maskBX2 = maskAX2 - 20
    maskBY2 = maskAY2 - 20
    wmdraw.rectangle((maskAX1,maskAY1,maskAX2,maskAY2), fill=maskrgba[0])
    wmdraw.rectangle((maskBX1,maskBY1,maskBX2,maskBY2), fill=maskrgba[1]) 

    # draw text
    for i in texts:
        wmdraw.text((textpos[0], textpos[1]), i[0], i[2], font=i[1])
        textpos[1] += i[1].getsize(i[0])[1]
    img.paste(wmback, mask=wmback)
    img.save(imgcfg["path"])
    

# check format of wallpaper image
# if format is not .bmp, convert it to .bmp
# then, set register and wallpaper
def set_wallpaper(imgcfg):
    if len(imgcfg["path"]) < 5:
        prerr("path is too short")
    del_flag = False
    # jpg, png to bmp
    if imgcfg["path"][-3:] == "jpg" or imgcfg["path"][-4:] == "jpeg"\
    or imgcfg["path"][-3:] == "JPG" or imgcfg["path"][-3:] == "JPEG"\
    or imgcfg["path"][-3:] == "png" or imgcfg["path"][-3:] == "PNG":
        imgcfg["path"] = convert2bmp(imgcfg["path"])
        if imgcfg["delbmp"] == "no" or imgcfg["delbmp"] == "NO":
            prmsg("save .bmp in %s" % imgcfg["path"])
        elif imgcfg["delbmp"] == "yes" or imgcfg["delbmp"] == "YES":
            del_flag = True
        else:
            prwarn("value of option <delbmp> is illegal") 
    # do update
    if imgcfg["path"][-3:] == "bmp" or imgcfg["path"][-3:] == "BMP":
        # draw watermark
        draw_watermark(imgcfg)
        update_wallpaper(imgcfg["path"])
    else:
        prerr("image format can not support")
    if del_flag:
        time.sleep(1)
        prmsg("delete tmp .bmp file")
        os.remove(imgcfg["path"])


# load configuration from CONFIG_PATH
# return dict "imgcfg"
def load_config(CONFIG_PATH):
    imgcfg = {"path":"", "style":"2", "tile":"0", "delbmp":"no",
            "sfont":"", "sfontsize":"30", "sfontcolor":"(255,255,255)",
            "afont":"", "afontsize":"30", "afontcolor":"(255,255,255)",
            "bfont":"", "bfontsize":"30", "bfontcolor":"(255,255,255)",
            "cfont":"", "cfontsize":"30", "cfontcolor":"(255,255,255)",
            "dfont":"", "dfontsize":"30", "dfontcolor":"(255,255,255)",
            "startpos":"0,0", "endmargin":"0,0", "content":[]}
    imgcfg_opts = ["path","style","tile","delbmp","startpos","endmargin",
            "sfont", "sfontsize", "sfontcolor", 
            "afont", "afontsize", "afontcolor",
            "bfont", "bfontsize", "bfontcolor",
            "cfont", "cfontsize", "cfontcolor",
            "dfont", "dfontsize", "dfontcolor",] 
    cfg = ConfigParser.ConfigParser()
    cfg.read(CONFIG_PATH)
    for opt in imgcfg_opts:
        imgcfg[opt] = cfg.get("imgcfg", opt)
    with open(cfg.get("imgcfg", "content"), "rt") as f:
        for i in f: imgcfg["content"].append(i.strip('\n').strip('\r'))
    return imgcfg


# generate a configuration file
def gen_config(CONFIG_PATH):
    config_opts = """[imgcfg]
path = /path/to/image.jpg
style = 2
tile = 0
delbmp = no
startpos = 1200, 400
endmargin = 300, 300
content = ./whitodo.txt

sfont = msyhbd.ttc
sfontsize = 50
sfontcolor = RGB(255, 0, 0)

afont = msyhbd.ttc
afontsize = 30
afontcolor = RGB(255, 0, 0)

bfont = msyhbd.ttc
bfontsize = 30
bfontcolor = RGB(255, 255, 0)

cfont = msyhbd.ttc
cfontsize = 30
cfontcolor = RGB(255, 255, 255)

dfont = msyh.ttc
dfontsize = 30
dfontcolor = RGB(255, 255, 255)"""
    texts = """[S]The most important and the most urgent task
[A]Important and urgent task
[B]Important task
[C]General task
[D]Low priority task[DEFAULT]"""
    with open(CONFIG_PATH, "wt") as f:
        f.write(config_opts)
    if path.exists("whitodo.txt"):
        return
    with open("whitodo.txt", "wt") as f:
        f.write(texts)


if __name__ == '__main__':
    CONFIG_PATH = "./whitodo.cfg"
    if not path.exists(CONFIG_PATH):
        gen_config(CONFIG_PATH)
        prmsg("Configuration generated on <whitodo.cfg>")
        prmsg("Update <whitodo.txt> for using [whitodo]!")
        sys.exit()
    imgcfg = load_config(CONFIG_PATH)
    print imgcfg
    set_wallpaper(imgcfg)

