#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtRollerCoaster 
@ File        : test_taskbar.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
import commctrl
import win32gui
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout


class TaskbarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMaximumSize(80, 30)  # 默认任务栏高是 40，于是我们设置窗口最大是 30
        self.setWindowFlags(Qt.FramelessWindowHint)  # 设置窗口为无边框

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setContentsMargins(0, -1, 0, -1)  # 内边距
        self.label = QLabel('Hello!')
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.init_set_taskbar()  # 初始化设置

        self.icon_count = 0  # 默认图标数量
        self.icon_status = True  # 获取初始数量时的状态
        self.timer_set_taskbar()  # 定时设置任务栏

    def init_set_taskbar(self):
        """设置任务栏"""
        self.m_h_taskbar = win32gui.FindWindow("Shell_TrayWnd", None)  # 任务栏“Shell_TaryWnd”的窗口句柄
        # 子窗口“ReBarWindow32”的窗口句柄
        self.m_h_bar = win32gui.FindWindowEx(self.m_h_taskbar, 0, "ReBarWindow32", None)
        self.m_h_min = win32gui.FindWindowEx(self.m_h_bar, 0, "MSTaskSwWClass", None)  # 子窗口“MSTaskSwWClass”的窗口句柄
        self.b = win32gui.GetWindowRect(self.m_h_bar)  # 获取m_hBar窗口尺寸b为[左，上，右，下]的数组

        self.move_window()

    def move_window(self):
        # 调整m_hMin的窗口大小，为我们的程序预留出位置
        win32gui.MoveWindow(self.m_h_min, 0, 0, self.b[2] - self.b[0] - 75, self.b[3] - self.b[1], True)

        self.setGeometry(self.b[2] - self.b[0] - 75, 5, 75, self.b[3] - self.b[1])  # 调整我们自己的窗口到预留位置的大小
        win32gui.SetParent(int(self.winId()), self.m_h_bar)  # 将我们自己的窗口设置为m_hBar的子窗口

    def timer_set_taskbar(self, interval: int = 200):  # 200ms
        """定时获取指定的值"""
        self.time_set_taskbar = QTimer(self)
        self.time_set_taskbar.setInterval(interval)
        # self.time_set_taskbar.timeout.connect(self.get_taskbar_size)  # 方案1
        self.time_set_taskbar.timeout.connect(self.get_tray_icon_count)  # 方案2
        self.time_set_taskbar.start()  # 启动

    def get_taskbar_size(self):
        """获取任务栏尺寸"""
        self.b_new = win32gui.GetWindowRect(self.m_h_bar)
        if self.b_new == self.b:  # 尺寸没变化，则直接返回
            return
        self.b = self.b_new
        self.move_window()

    def get_tray_icon_count(self):
        # 获取托盘区域的窗口句柄
        tray_notify_handle = win32gui.FindWindowEx(self.m_h_taskbar, 0, "TrayNotifyWnd", None)
        sys_pager_handle = win32gui.FindWindowEx(tray_notify_handle, 0, "SysPager", None)
        notification_area_handle = win32gui.FindWindowEx(sys_pager_handle, 0, "ToolbarWindow32", None)
        # 获取托盘图标的数量
        count = win32gui.SendMessage(notification_area_handle, commctrl.TB_BUTTONCOUNT, 0, 0)
        if self.icon_status:
            self.icon_count = count  # 初始化
            self.icon_status = False
        if self.icon_count != count:
            self.dynamic_set_taskbar(icon_count=count)

    def dynamic_set_taskbar(self, icon_count=0):
        """动态设置任务栏"""
        if icon_count and self.icon_count != 0:
            x = self.icon_count - icon_count
            self.b = (self.b[0], self.b[1], self.b[2] + (x * 24), self.b[3],)
            self.icon_count = icon_count
        self.move_window()

    def closeEvent(self, event):
        self.time_set_taskbar.stop()
        super(TaskbarWidget, self).closeEvent(event)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    rc = TaskbarWidget()
    rc.show()
    sys.exit(app.exec_())
