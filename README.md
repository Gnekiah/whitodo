# whitodo

![whitodo](whitodo.ico)

## Overview

WhiToDo, the to-do list panel for working management.

**This repo. have stopped maintenance**, please goto [WhiToDo-Csharp](https://github.com/Gnekiah/whitodo-csharp)

## Usage

1. For the first use, make settings file `whitodo.cfg`
2. Writing to-do item into `whitodo.txt` file, there are 6 level:
   - [S] The most important and the most urgent task
   - [A] Important and urgent task
   - [B] Important task
   - [C] General task
   - [D] Low priority task [DEFAULT]
   - [X] Hidden task
3. Run `python whitodo.py` or double click `whitodo.vbs` to active.

## New Features

#### mode-single

Without loopping, only set desktop wallpaper using this image.

#### mode-cycle

Loopping images from a specificated dir. You can set random mode or use sequential mode direct

#### mode-bingindex

Download from bing everyday and set as desktop wallpaper.

## Tips

Step:

- Load settings from whitodo.cfg
- Load todo item from whitodo.txt
- Load source image and draw todo text into source image
- Set drawed-image as desktop-wallpaper