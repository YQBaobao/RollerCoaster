#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtRollerCoaster 
@ File        : monitor_setting.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
import os

from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel
from configobj import ConfigObj
from plyer import notification

from core.message_box import MessageBox
from temp import TEMP
from uis.rc_setting.monitor_setting.monitor_setting import Ui_Monitor


class UiMonitorQWidget(QWidget, Ui_Monitor):
    def __init__(self, base_signal, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.base_signal = base_signal

        self.init_ui()
        self.message_box = MessageBox()
        self.pushButton_accepted_monitor.clicked.connect(self.on_monitor_data_check)

        self.base_signal.signal_monitor_msg.connect(self.on_message)

    def init_ui(self):
        self.user_data_path = os.path.join(TEMP, "user_data.ini")
        self.config = ConfigObj(self.user_data_path, encoding='UTF8')
        try:
            self.lineEdit.setText(self.config['monitor']['title'])
            self.lineEdit_2.setText(self.config['monitor']['msg'])
            self.spinBox.setValue(int(self.config['monitor']['timeout']))
            self.checkBox.setChecked(True if self.config['monitor']['msg_status'].lower() == 'true' else False)

            self.checkBox_6.setChecked(True if self.config['monitor']['monitor_status'].lower() == 'true' else False)
            self.lineEdit_3.setText(self.config['monitor']['symbol_1_up'])
            self.lineEdit_4.setText(self.config['monitor']['symbol_1_down'])
            self.checkBox_2.setChecked(True if self.config['monitor']['symbol_1_price'].lower() == 'true' else False)

            self.lineEdit_5.setText(self.config['monitor']['symbol_2_up'])
            self.lineEdit_6.setText(self.config['monitor']['symbol_2_down'])
            self.checkBox_3.setChecked(True if self.config['monitor']['symbol_2_price'].lower() == 'true' else False)

            self.lineEdit_7.setText(self.config['monitor']['symbol_3_up'])
            self.lineEdit_8.setText(self.config['monitor']['symbol_3_down'])
            self.checkBox_4.setChecked(True if self.config['monitor']['symbol_3_price'].lower() == 'true' else False)

            self.lineEdit_9.setText(self.config['monitor']['symbol_4_up'])
            self.lineEdit_10.setText(self.config['monitor']['symbol_4_down'])
            self.checkBox_5.setChecked(True if self.config['monitor']['symbol_4_price'].lower() == 'true' else False)
        except KeyError:
            with open(self.user_data_path, "a", encoding='utf-8') as f:
                user_data = (
                    '\n[monitor]\ntitle = 快递到咯！\nmsg = 您的快递已经送到驿站啦，快抽空签收一下哟~\n'
                    'timeout = 3\nmsg_status = True\nmonitor_status = True\n'
                    'symbol_1_up = \nsymbol_1_down = \nsymbol_1_price = True\n'
                    'symbol_2_up = \nsymbol_2_down = \nsymbol_2_price = True\n'
                    'symbol_3_up = \nsymbol_3_down = \nsymbol_3_price = True\n'
                    'symbol_4_up = \nsymbol_4_down = \nsymbol_4_price = True')
                f.write(user_data)
            self.config = ConfigObj(self.user_data_path, encoding='UTF8')

    def on_monitor_data_check(self):
        """监控数据处理"""
        self.monitor_data = []
        if not self.checkBox_6.isChecked():  # 不启用直接返回
            return
        symbol_1 = {"up": None, "down": None, "price": True, "trigger": False}
        symbol_2 = {"up": None, "down": None, "price": True, "trigger": False}
        symbol_3 = {"up": None, "down": None, "price": True, "trigger": False}
        symbol_4 = {"up": None, "down": None, "price": True, "trigger": False}
        symbol_1["up"], symbol_1["down"] = self.__data_check(self.lineEdit_3, self.lineEdit_4, self.label_3)
        symbol_1['price'] = self.checkBox_2.isChecked()
        self.monitor_data.append(symbol_1)
        symbol_2["up"], symbol_2["down"] = self.__data_check(self.lineEdit_5, self.lineEdit_6, self.label_4)
        symbol_2['price'] = self.checkBox_3.isChecked()
        self.monitor_data.append(symbol_2)
        symbol_3["up"], symbol_3["down"] = self.__data_check(self.lineEdit_7, self.lineEdit_8, self.label_5)
        symbol_3['price'] = self.checkBox_4.isChecked()
        self.monitor_data.append(symbol_3)
        symbol_4["up"], symbol_4["down"] = self.__data_check(self.lineEdit_9, self.lineEdit_10, self.label_6)
        symbol_4['price'] = self.checkBox_5.isChecked()
        self.monitor_data.append(symbol_4)

        self.user_data_save()
        self.base_signal.signal_monitor_data.emit(self.monitor_data)

    def __data_check(self, up_obj: QLineEdit, down_obj: QLineEdit, label_obj: QLabel):
        """数据规范检查"""
        up = up_obj.text().rstrip()
        down = down_obj.text().rstrip()
        try:
            up = float(up) if up else None
            down = float(down) if down else None
        except ValueError:
            self.message_box.info_message(f'请在“{label_obj.text()}”中输入正确的参数。', self)
        return up, down

    def on_message(self, status: list):
        """消息提醒"""
        if not self.checkBox.isChecked():  # 不启用直接返回
            return
        self.trigger_clear(status)

        title = self.lineEdit.text().rstrip()
        msg = self.lineEdit_2.text().rstrip()
        timeout = self.spinBox.value()
        notification.notify(
            app_name='RollerCoaster',
            app_icon=f"{TEMP}/../static/images/microscope.ico",
            title=title,
            message=msg,
            timeout=timeout
        )

    def trigger_clear(self, status):
        """触发清理"""
        if status[0] == 0:  # 清空数据
            self.config['monitor']['symbol_1_up'] = ''
            self.config['monitor']['symbol_1_down'] = ''
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()
        elif status[0] == 1:
            self.config['monitor']['symbol_2_up'] = ''
            self.config['monitor']['symbol_2_down'] = ''
            self.lineEdit_5.clear()
            self.lineEdit_6.clear()
        elif status[0] == 2:
            self.config['monitor']['symbol_3_up'] = ''
            self.config['monitor']['symbol_3_down'] = ''
            self.lineEdit_7.clear()
            self.lineEdit_8.clear()
        else:
            self.config['monitor']['symbol_4_up'] = ''
            self.config['monitor']['symbol_4_down'] = ''
            self.lineEdit_9.clear()
            self.lineEdit_10.clear()
        self.config.write()

    def user_data_save(self):
        """保存在用户数据"""
        self.config['monitor']['title'] = self.lineEdit.text()
        self.config['monitor']['msg'] = self.lineEdit_2.text()
        self.config['monitor']['timeout'] = str(self.spinBox.value())
        self.config['monitor']['msg_status'] = self.checkBox.isChecked()

        self.config['monitor']['monitor_status'] = self.checkBox_6.isChecked()
        self.config['monitor']['symbol_1_up'] = self.lineEdit_3.text()
        self.config['monitor']['symbol_1_down'] = self.lineEdit_4.text()
        self.config['monitor']['symbol_1_price'] = self.checkBox_2.isChecked()

        self.config['monitor']['symbol_2_up'] = self.lineEdit_5.text()
        self.config['monitor']['symbol_2_down'] = self.lineEdit_6.text()
        self.config['monitor']['symbol_2_price'] = self.checkBox_3.isChecked()

        self.config['monitor']['symbol_3_up'] = self.lineEdit_7.text()
        self.config['monitor']['symbol_3_down'] = self.lineEdit_8.text()
        self.config['monitor']['symbol_3_price'] = self.checkBox_4.isChecked()

        self.config['monitor']['symbol_4_up'] = self.lineEdit_9.text()
        self.config['monitor']['symbol_4_down'] = self.lineEdit_10.text()
        self.config['monitor']['symbol_4_price'] = self.checkBox_5.isChecked()
        self.config.write()
