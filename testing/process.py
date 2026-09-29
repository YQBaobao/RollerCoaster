#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : process.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
import os

# try:
#     x = os.system('tasklist | findstr RoCoaster.exe')
#     if x != 1:
#         os.system('taskkill /f /t /im  RoCoaster.exe')  # 结束进程
# except OSError as e:
#     print("Error ending existing process:", e)
#

import psutil

pids = psutil.process_iter()
print("[ RoCoaster.exe ]'s pid is:")
for pid in pids:
    if (pid.name() == 'RoCoaster.exe'):
        print(pid.pid)
