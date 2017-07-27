# -*- coding:utf-8 -*-
# @Ekira, 2017/7/27

import win32api, win32con, win32gui


# set register and update wallpaper
def update_wallpaper(wallpaper, style="2", tile="0"):
    regkey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, 
            "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(regkey,"WallpaperStyle",0,win32con.REG_SZ,style)
    win32api.RegSetValueEx(regkey,"TileWallpaper",0,win32con.REG_SZ,tile)
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, wallpaper, 
            win32con.SPIF_SENDWININICHANGE)  
