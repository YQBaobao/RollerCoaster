#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : test_keyboard.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
import tkinter as tk
import keyboard


def output(event):
    # print("From global keystroke")
    print(event)


root = tk.Tk()
root.withdraw()

keyboard.add_hotkey('ctrl+k', output, args=('From global keystroke',))
# keyboard.add_hotkey('ctrl+a', output)
root.mainloop()
