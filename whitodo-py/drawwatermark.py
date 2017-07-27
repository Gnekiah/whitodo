# -*- coding:utf-8 -*-
# @Ekira, 2017/7/27

import time
from os import path
from PIL import Image, ImageDraw, ImageFont, ImageColor


# draw watermark
def draw_watermark(imgcfg):
    img = Image.open(imgcfg["wppath"]).convert("RGB")
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
        elif i[:3] == "[X]" or i[:3] == "[x]":
            pass
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
    wallpaper = time.strftime("%Y.%m.%d-%H.%M.%S") + ".bmp"
    imgcfg["wppath"] = path.abspath(path.join(imgcfg["tgtdir"], wallpaper))
    img.save(imgcfg["wppath"])
