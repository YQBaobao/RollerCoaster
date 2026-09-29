#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : tool_tip.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
import sys

import win32gui
from PyQt5.QtWidgets import QWidget, QApplication


class UiWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # self.setToolTip('Background Color')
        m_h_taskbar = win32gui.FindWindow("Shell_TrayWnd", None)  # 任务栏“Shell_TaryWnd”的窗口句柄
        m_h_bar = win32gui.FindWindowEx(m_h_taskbar, 0, "ReBarWindow32", None)  # 子窗口“ReBarWindow32”的窗口句柄
        m_h_min = win32gui.FindWindowEx(m_h_bar, 0, "MSTaskSwWClass", None)  # 子窗口“MSTaskSwWClass”的窗口句柄
        print(m_h_min)
        b = win32gui.GetWindowRect(m_h_bar)  # 获取m_hBar窗口尺寸b为[左，上，右，下]的数组
        print(b)
        win32gui.MoveWindow(m_h_min, 0, 0, b[2] - b[0] - 100, b[3] - b[1], True)  # 调整m_hMin的窗口大小，为我们的程序预留出位置
        print(0, 0, b[2] - b[0] - 75, b[3] - b[1])
        self.setGeometry(b[2] - b[0] - 75, -5, 60, b[3] - b[1])  # 调整我们自己的窗口到预留位置的大小
        print(b[2] - b[0] - 75, -5, 75, b[3] - b[1])
        win32gui.SetParent(int(self.winId()), m_h_bar)  # 将我们自己的窗口设置为m_hBar的子窗口


if __name__ == '__main__':
    app = QApplication(sys.argv)
    rc = UiWidget()
    rc.show()
    exit(app.exec_())
