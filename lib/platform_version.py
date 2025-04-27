# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtRollerCoaster
@ File        : platform_version.py
@ Author      : yqbao
@ version     : V1.0.0
@ Description :
"""
import platform
import winreg


def get_windows_system_info():
    if platform.system() != "Windows":
        return {
            "is_windows_11": False,
            "is_windows_10": False,
            "product_name": None,
            "build_number": None,
            "display_version": None
        }
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
    product_name, _ = winreg.QueryValueEx(key, "ProductName")
    build_number_str, _ = winreg.QueryValueEx(key, "CurrentBuildNumber")
    build_number = int(build_number_str)

    try:
        # 某些老版本没有这个键
        display_version, _ = winreg.QueryValueEx(key, "DisplayVersion")
    except FileNotFoundError:
        display_version = None

    is_win11 = build_number >= 22000
    is_win10 = 10240 <= build_number < 22000

    return {
        "is_windows_11": is_win11,
        "is_windows_10": is_win10,
        "product_name": product_name,
        "build_number": build_number,
        "display_version": display_version
    }


if __name__ == "__main__":
    info = get_windows_system_info()
    print("系统类型:", "Windows 11" if info["is_windows_11"] else "Windows 10")
    print("产品名称:", info['product_name'])
    print("Build号:", info['build_number'])
    print("显示版本:", info['display_version'])
