# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtRollerCoaster
@ File        : window_rect.py
@ Author      : yqbao
@ version     : V1.0.0
@ Description :
"""
import ctypes
from ctypes import wintypes


def get_taskbar_sections_width():
    """获取 Windows 任务栏托盘 + 时间区域宽度"""
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()  # 支持高DPI缩放，拿到真实像素

    # 获取屏幕尺寸
    screen_width = user32.GetSystemMetrics(0)

    def get_window_rect(hwnd):
        rect = wintypes.RECT()
        if user32.GetWindowRect(hwnd, ctypes.byref(rect)):
            return rect.left, rect.top, rect.right, rect.bottom
        return None

    # 找到托盘区域窗口 win10/win11
    hwnd_taskbar = user32.FindWindowW("Shell_TrayWnd", None)
    hwnd_tray = user32.FindWindowExW(hwnd_taskbar, None, "TrayNotifyWnd", None)

    if not hwnd_taskbar or not hwnd_tray:
        return None
    taskbar_rect = get_window_rect(hwnd_taskbar)
    if not taskbar_rect:
        return None
    tray_rect = get_window_rect(hwnd_tray)
    if not tray_rect:
        return None
    _, top, _, bottom = taskbar_rect
    tray_left, _, _, _ = tray_rect
    # 托盘 + 时间区域宽度,任务栏高度
    return screen_width - tray_left, bottom - top


if __name__ == '__main__':
    print(get_taskbar_sections_width())
