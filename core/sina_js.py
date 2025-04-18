# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtRollerCoaster
@ File        : sina_js.py
@ Author      : yqbao
@ version     : V1.0.0
@ Description : 新浪财经
"""
from decimal import Decimal

import requests


class SinaJs(object):
    realtime_quote = "https://hq.sinajs.cn/rn={}/&list={}"
    headers = {
        'Accept': '*/*',
        'host': "hq.sinajs.cn",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Connection': 'keep-alive',
        'Referer': "https://finance.sina.com.cn/futuremarket/"
    }

    def fetch(self, url):
        """不带token"""
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(response.text)
        return response.text

    def quote(self, symbol, timestamp):
        url = self.realtime_quote.format(timestamp, symbol)
        value = self.fetch(url)
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


if __name__ == '__main__':
    import time

    s = SinaJs()
    t = int(time.time() * 1000)
    for i in range(10):
        print(s.quote('nf_AU2602,nf_AU2508', t))
        time.sleep(2)
