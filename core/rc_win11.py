# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtRollerCoaster
@ File        : rc_win11.py
@ Author      : yqbao
@ version     : V1.0.0
@ Description :
"""
import ctypes
from ctypes import wintypes

import win32con
import win32gui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtWidgets import QApplication
from configobj import ConfigObj

from core.rc import RollerCoasterApp
from lib.window_rect import get_taskbar_sections_width


class Win11FloatingRollerCoasterApp(RollerCoasterApp):
    """Win11 浮动显示（有瑕疵），也支持Win10，但是不建议。因为嵌入方案在Win10上显示效果更好"""

    def __init__(self):
        super().__init__()
        # 设置透明背景
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.timer_set_topmost(500)  # 定时维持窗口置顶

    def init_ui(self):
        self.set_click_through()  # 设置点击穿透 & 不抢焦点
        font = QFont()
        font.setPointSize(10)
        self.label_value.setFont(font)
        self.label_rate.setFont(font)

        # 初始化
        self.sections_width, _ = get_taskbar_sections_width()
        self.screen_rect = QApplication.desktop().screenGeometry(0)  # 固定用主屏幕坐标基准

        self.config = ConfigObj(self.user_data_path, encoding='UTF8')
        color = QColor(self.config['background_color']['color'])
        palette = self.palette()
        palette.setColor(QPalette.Background, color)
        self.setPalette(palette)
        self.label_value.setStyleSheet(self.light)
        self.label_rate.setStyleSheet(self.light)

    def move_window(self):
        screen_height = self.screen_rect.height()
        screen_width = self.screen_rect.width()

        # 完全重叠在任务栏上方
        x = screen_width - self.sections_width - self.width()
        y = screen_height - self.height() + 3
        self.move(x, y)

    def timer_set_taskbar(self, interval: int = 200):  # 500ms
        """定时设置任务栏"""
        self.time_set_taskbar = QTimer(self)
        self.time_set_taskbar.setInterval(interval)
        self.time_set_taskbar.timeout.connect(self.get_taskbar_size)  # 兼容 win11
        self.time_set_taskbar.start()  # 启动

    def get_taskbar_size(self):
        """获取任务栏尺寸"""
        sections_width, _ = get_taskbar_sections_width()
        if sections_width == self.sections_width:
            return
        self.sections_width = sections_width
        self.move_window()

    def init_action(self):
        super(Win11FloatingRollerCoasterApp, self).init_action()
        # 监听屏幕插拔，自动调整位置
        QApplication.instance().screenAdded.connect(self.on_screen_changed)
        QApplication.instance().screenRemoved.connect(self.on_screen_changed)

    def on_screen_changed(self, *args):
        """当屏幕插拔变化时，重新定位"""
        QTimer.singleShot(500, self.move_window)  # 延迟，等待系统完成更新

    def set_click_through(self):
        hwnd = int(self.winId())
        # 获取当前扩展样式
        ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        ex_style |= win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)

    def timer_set_topmost(self, interval=100):
        self.timer_topmost = QTimer()
        self.timer_topmost.timeout.connect(self.set_topmost)
        self.timer_topmost.start(interval)

    def set_topmost(self):
        """设置到最顶层。任务栏一旦处于活动状态，系统会将其提到最顶层"""
        hwnd = int(self.winId())

        def is_obscured():
            """判断当前窗口是否被遮挡"""
            foreground = win32gui.GetForegroundWindow()
            if foreground == hwnd:
                return False  # 自己是前台窗口，无需置顶

            # 获取窗口矩形
            rect_self = wintypes.RECT()
            rect_fore = wintypes.RECT()

            user32 = ctypes.windll.user32
            user32.GetWindowRect(hwnd, ctypes.byref(rect_self))
            user32.GetWindowRect(foreground, ctypes.byref(rect_fore))

            # 判断是否有交集
            intersect = wintypes.RECT()
            has_intersection = user32.IntersectRect(
                ctypes.byref(intersect),
                ctypes.byref(rect_self),
                ctypes.byref(rect_fore)
            )
            return bool(has_intersection)

        def is_already_topmost():
            """窗口是否已是 TOPMOST"""
            ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            return bool(ex_style & win32con.WS_EX_TOPMOST)

        if not is_already_topmost() or is_obscured():
            win32gui.SetWindowPos(
                hwnd, win32con.HWND_TOPMOST,
                self.x(), self.y(), self.width(), self.height(),
                win32con.SWP_NOACTIVATE | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
            )

    def set_futures(self, data):
        super().set_futures(data)
        QTimer.singleShot(1000, self.move_window)  # 单次定时

    def closeEvent(self, event) -> None:
        self.timer_topmost.stop()
        super(Win11FloatingRollerCoasterApp, self).closeEvent(event)
