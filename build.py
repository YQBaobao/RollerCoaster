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
        '--noupx',
        '--upx-exclude=api-ms-win-core*.dll',  # 忽略压缩 NotCompressibleException
        '--upx-exclude=api-ms-win-crt*.dll',
        '--upx-exclude=python3.dll',
        '--upx-exclude=_uuid.pyd',
        '--upx-exclude=md.cp39-win32.pyd',
        '--upx-exclude=WinDivert32.sys',
        '--upx-exclude=WinDivert64.sys',
        '--add-data=static/images;static/images',
        '--hidden-import=plyer.platforms.win.notification',
        '--contents-directory=.'
    ]

    run(opts)
