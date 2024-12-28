#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : MQSendUi
@ File        : installers.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description :
"""
import os
from PyInstaller.__main__ import run

dir_path = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    opts = [
        'main.py',
        '--name=RoCoaster',
        '-D',
        '-w',
        '--icon={}/static/images/microscope.ico'.format(dir_path),
        '-y',
        '-p .',
        '--clean',
        '--add-data=static/images;static/images',
        '--contents-directory=.'
    ]

    run(opts)
