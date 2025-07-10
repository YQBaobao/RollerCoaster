# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtRollerCoaster
@ File        : sina_js.py
@ Author      : yqbao
@ version     : V1.0.0
@ Description : 新浪财经
"""
import random
from decimal import Decimal

import requests


class SinaJs(object):
    qh_realtime_quote = "https://hq.sinajs.cn/rn={}/&list={}"
    gu_realtime_quote = "https://w.sinajs.cn/rn={}/&list={}"
    headers = {
        'Accept': '*/*',
        'host': "hq.sinajs.cn",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Connection': 'keep-alive',
        'Referer': "https://finance.sina.com.cn/futuremarket/"
    }

    @staticmethod
    def rn():
        return int(1234567890 * random.random() + 1) + int(9876543210 * random.random() + 1)

    @staticmethod
    def fetch(url, headers: dict):
        """不带token"""
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(response.text)
        return response.text

    def qh_quote_hq(self, symbol, timestamp):
        url = self.qh_realtime_quote.format(timestamp, symbol)
        value = self.fetch(url, self.headers)
        symbol_list = value.split("\n")[:-1]
        quote_dict = {'data': []}
        for index, value in enumerate(symbol_list):
            value_list = value.split(',')
            settlement_yesterday = float(value_list[10])
            current = float(value_list[8])
            percent = (current - settlement_yesterday) / settlement_yesterday * 100
            percent = float(Decimal(percent).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))
            quote_dict['data'].append({"symbol": symbol.split(',')[index], "current": current, "percent": percent})
        return quote_dict

    def gu_quote_hq(self, symbol, timestamp):
        url = self.qh_realtime_quote.format(timestamp, symbol)
        value = self.fetch(url, self.headers)
        symbol_list = value.split("\n")[:-1]
        quote_dict = {'data': []}
        for index, value in enumerate(symbol_list):
            value_list = value.split(',')
            settlement_yesterday = float(value_list[2])
            current = float(value_list[3])
            percent = (current - settlement_yesterday) / settlement_yesterday * 100
            percent = float(Decimal(percent).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))
            quote_dict['data'].append({"symbol": symbol.split(',')[index], "current": current, "percent": percent})
        return quote_dict

    def gu_quote_w(self, symbol, timestamp):
        url = self.gu_realtime_quote.format(timestamp, symbol)
        self.headers.update({"host": "w.sinajs.cn", "Referer": "https://gu.sina.cn/"})
        value = self.fetch(url, self.headers)
        symbol_list = value.split("\n")[:-1]
        quote_dict = {'data': []}
        for index, value in enumerate(symbol_list):
            value_list = value.split(',')
            settlement_yesterday = float(value_list[2])
            current = float(value_list[3])
            percent = (current - settlement_yesterday) / settlement_yesterday * 100
            percent = float(Decimal(percent).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))
            quote_dict['data'].append({"symbol": symbol.split(',')[index], "current": current, "percent": percent})
        return quote_dict


if __name__ == '__main__':
    import time

    s = SinaJs()
    for i in range(10):
        t = int(time.time() * 1000)
        # print(s.qh_quote_hq('nf_AU2602,nf_AU2508', t))
        print(s.gu_quote_hq('sh600418,sz002436,sz001696', t))
        # rn = s.rn()
        # print(s.gu_quote_w('sh600418,sz002436,sz001696', rn))
        time.sleep(2)
