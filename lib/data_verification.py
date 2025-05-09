# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtRollerCoaster
@ File        : data_verification.py
@ Author      : yqbao
@ version     : V1.0.0
@ Description :
"""
import typing

from core.message_box import MessageBox

message_box = MessageBox()


def data_verification(symbol_1, symbol_2, symbol_3, symbol_4, parent) -> typing.Union[bool, list]:
    """数据校验"""
    if not symbol_1:
        message_box.info_message('“代码(1)”必须有值。', parent)
        return False
    symbol_list = [symbol_1]
    if symbol_2:
        symbol_list.append(symbol_2)
    if symbol_3:
        symbol_list.append(symbol_3)
    if symbol_4:
        symbol_list.append(symbol_4)
    symbol_set = set(symbol_list)
    if len(symbol_set) != len(symbol_list):
        message_box.info_message('请确保已经输入的“代码”互不相同。', parent)
        return False
    return symbol_list
