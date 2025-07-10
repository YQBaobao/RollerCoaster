# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtRollerCoaster
@ File        : config.py
@ Author      : yqbao
@ version     : V1.0.0
@ Description :
"""
import os
from configobj import ConfigObj


class ConfigManager(object):
    def __init__(self, config_path, new_config=None):
        self.user_data_path = config_path
        self.new_config = new_config  # 新配置
        self.config = self.load_or_update_config()

    def load_or_update_config(self):
        config = ConfigObj(encoding='UTF8')
        # 如果配置文件存在，则读取
        if os.path.exists(self.user_data_path):
            try:
                config = ConfigObj(self.user_data_path, encoding='UTF8')
                print(f"成功读取配置文件: {self.user_data_path}")
            except Exception as e:
                print(f"读取配置文件失败: {e}")
                config = ConfigObj(encoding='UTF8')
        else:
            print(f"配置文件 {self.user_data_path} 不存在，创建新配置文件")
        if self.new_config is not None:
            config = self.merge_config(config, self.new_config)
        try:
            config.filename = self.user_data_path
            config.write()
            print(f"已更新并保存配置文件到 {self.user_data_path}")
        except IOError as e:
            print(f"无法保存配置文件: {e}")
        return config

    def merge_config(self, config, new_config):
        """合并新配置到现有配置"""
        for section, settings in new_config.items():
            if section not in config:
                config[section] = {}
            if isinstance(settings, dict):
                config[section] = self.merge_config(config[section], settings)
            else:
                if section not in config:
                    config[section] = settings
        return config

    def save_config(self):
        """保存当前配置到文件"""
        try:
            self.config.write()
            print("配置已保存")
        except IOError as e:
            print(f"无法保存配置文件: {e}")
