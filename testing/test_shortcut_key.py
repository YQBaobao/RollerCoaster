#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : test_shortcut_key.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
from system_hotkey import SystemHotkey, SystemRegisterError, InvalidKeyError

try:
    hk = SystemHotkey()
    hk.register(['control', 'up'], callback=lambda x: print("Easy!"))
except SystemRegisterError as e:
    print('热键已在使用中', e)
except InvalidKeyError as e:
    print('不被理解', e)
except Exception as e:
    print(e)
