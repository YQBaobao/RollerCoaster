#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : test_1.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
from infi.systray import SysTrayIcon
from PIL import Image, ImageDraw, ImageFont
import time
import psutil

image = "main.ico"
initialStart = True
systray = SysTrayIcon(image, "CPU/MEM")

while True:
    img = Image.new('RGBA', (50, 50), color=(255, 255, 255, 100))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 25, 50, 50), fill=(39, 112, 229), outline=None)

    font_type = ImageFont.truetype("arial.ttf", 25)
    a = psutil.cpu_percent(interval=1, percpu=False)
    b = psutil.virtual_memory().percent
    d.text((0, 0), f"{a}\n{b}", fill=(255, 255, 255), font=font_type)

    img.save(image)

    if initialStart:
        systray.start()
        initialStart = False
    else:
        systray.update(icon=image)
    time.sleep(0.5)
