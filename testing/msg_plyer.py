#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtRollerCoaster 
@ File        : msg_plyer.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""

from plyer import notification

notification.notify(
    app_name='Python 3.9',
    app_icon="../static/images/microscope.ico",
    title="标题标题",
    message="这里是消息提醒的内容",
    timeout=10
)
