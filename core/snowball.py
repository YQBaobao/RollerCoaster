#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : snowball.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 雪球数据
"""
import json

import requests


class Snowball(object):
    host = 'https://stock.xueqiu.com'
    realtime_quote = f"{host}/v5/stock/realtime/quotec.json?symbol="
    realtime_quote_detail = f"{host}/v5/stock/quote.json?extend=detail&symbol="
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Xueqiu iPhone 11.8',
        'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
        'Accept-Encoding': 'br, gzip, deflate',
        'Connection': 'keep-alive'

    }

    def set_token(self, token):
        self.token = token

    def fetch_token(self, url, host="stock.xueqiu.com"):
        """带token"""
        self.headers['Host'] = host
        self.headers['Cookie'] = self.token
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(response.content)
        return json.loads(response.content)

    def fetch(self, url, host="stock.xueqiu.com"):
        """不带token"""
        self.headers['Host'] = host
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(response.content)
        return json.loads(response.content)

    def quote(self, symbol):
        url = self.realtime_quote + symbol
        return self.fetch(url)

    def quote_detail(self, symbol):
        url = self.realtime_quote_detail + symbol
        return self.fetch_token(url)


if __name__ == '__main__':
    s = Snowball()
    s.set_token('xq_a_token=a7dacb9398d5c3c8bf5d92115b281556f5f7eb52;')
    print(s.quote('SH601127'))
    print(s.quote_detail('SH601127'))
