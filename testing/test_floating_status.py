# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtRollerCoaster
@ File        : test_floating_status.py
@ Author      : yqbao
@ version     : V1.0.0
@ Description :
"""
import sys
import ctypes
from ctypes import wintypes
import win32gui
import win32con
import win32api
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer, QObject, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush
from pynput import mouse

from lib.window_rect import get_taskbar_sections_width

user32 = ctypes.windll.user32


class MouseWatcher(QObject):
    """鼠标监控 任务栏点击 + 任务栏移入移出"""
    taskbar_clicked = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()

        self._was_inside = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_mouse)
        self.timer.start(100)  # 100ms 轮询

    @staticmethod
    def get_taskbar_rect():
        hwnd = win32gui.FindWindow("Shell_TrayWnd", None)
        if hwnd:
            return win32gui.GetWindowRect(hwnd)
        return None

    def check_mouse(self):
        pos = win32api.GetCursorPos()
        taskbar_rect = self.get_taskbar_rect()
        if not taskbar_rect:
            return

        x, y = pos
        l, t, r, b = taskbar_rect
        inside = l <= x <= r and t <= y <= b

        if inside and not self._was_inside:
            self._was_inside = True
            self.taskbar_clicked.emit(True)
        elif not inside and self._was_inside:
            self._was_inside = False
            self.taskbar_clicked.emit(False)

    def on_click(self, x, y, button, pressed):
        if not pressed:
            return
        taskbar_rect = self.get_taskbar_rect()
        if taskbar_rect:
            left, top, right, bottom = taskbar_rect
            if left <= x <= right and top <= y <= bottom:
                self.taskbar_clicked.emit(True)


class FloatingStatus(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_action()

    def init_ui(self):
        # 设置窗口无边框、置顶、工具窗口
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.Tool |
            Qt.WindowStaysOnTopHint
        )

        # 设置透明背景
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        # 大小和显示内容
        self.setFixedSize(100, 40)
        self.label = QLabel("同步中...\n文件 3 个", self)
        self.label.setFont(QFont("微软雅黑", 8))
        self.label.setStyleSheet("color: red;")
        self.label.setGeometry(0, 0, 100, 40)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    def init_action(self):
        # 浮动在任务栏上方
        self.move_to_bottom_right()

        # 设置点击穿透 & 不抢焦点
        self.set_click_through()

        # 定时更新显示内容（可选）
        self.counter = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(2000)

        # 定时维持窗口置顶
        self.timer_set_topmost(500)

        # 全局鼠标监听器
        # self.mouse_watcher = MouseWatcher()
        # self.mouse_watcher.taskbar_clicked.connect(self.on_taskbar_clicked)

    def move_to_bottom_right(self):
        # 获取任务栏位置
        hwnd = win32gui.FindWindow("Shell_TrayWnd", None)
        re_bar = win32gui.FindWindowEx(hwnd, 0, "ReBarWindow32", None)
        # rect = win32gui.GetWindowRect(re_bar)  # win10
        # rect = win32gui.GetWindowRect(hwnd)  # win10/win11
        # screen_height = QApplication.desktop().screenGeometry().height()
        screen = self.screen()  # 当前所在屏幕
        screen_rect = screen.availableGeometry()
        screen_height = screen_rect.height()
        screen_width = screen_rect.width()

        sections_width, taskbar_height = get_taskbar_sections_width()

        # 完全重叠在任务上方
        # x = right - self.width()
        x = screen_width - sections_width - self.width()
        y = screen_height - self.height() + taskbar_height
        print(x, y)
        self.move(x, y)

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

    @staticmethod
    def is_obscured(hwnd):
        """判断当前窗口是否被遮挡"""
        foreground = win32gui.GetForegroundWindow()
        if foreground == hwnd:
            return False  # 自己是前台窗口，无需置顶

        # 获取窗口矩形
        rect_self = wintypes.RECT()
        rect_fore = wintypes.RECT()

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

    @staticmethod
    def is_already_topmost(hwnd):
        """窗口是否已是 TOPMOST"""
        ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        return bool(ex_style & win32con.WS_EX_TOPMOST)

    def set_topmost(self):
        hwnd = int(self.winId())

        def is_obscured():
            """判断当前窗口是否被遮挡"""
            foreground = win32gui.GetForegroundWindow()
            if foreground == hwnd:
                return False  # 自己是前台窗口，无需置顶

            # 获取窗口矩形
            rect_self = wintypes.RECT()
            rect_fore = wintypes.RECT()

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


    def on_taskbar_clicked(self, value):
        if value:
            print("👋 任务栏被点击")
            self.set_topmost()
        else:
            print("鼠标移出了任务栏")

    def paintEvent(self, event):
        # 绘制背景圆角矩形
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(40, 40, 40, 250)))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 0, 0)

    def update_status(self):
        self.counter += 1
        self.label.setText(f"同步中...\n文件 {self.counter} 个")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FloatingStatus()
    window.show()
    sys.exit(app.exec_())
