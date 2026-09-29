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
import re
import time

import requests


class Snowball(object):
    realtime_quote = "https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol="
    headers = {
        'Accept': 'application/json, text/plain, */*',
        # 'User-Agent': 'Xueqiu iPhone 11.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Connection': 'keep-alive',
        'origin': 'https://www.xueqiu.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.xueqiu.com',
        'sec-ch-ua': '"Google Chrome";v="153", "Not_A Brand";v="8", "Chromium";v="153"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36',
    }

    def fetch(self, token, url, host="stock.xueqiu.com"):
        """带token"""
        self.headers['Host'] = host
        self.headers['Cookie'] = token
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(response.content)
        return json.loads(response.content)

    def quote(self, token, symbol, timestamp):
        url = self.realtime_quote + symbol + f'&_={timestamp}'
        return self.fetch(token, url)


class GuShiTong(object):
    quotation = 'https://finance.pae.baidu.com/vapi/v1/getquotation?group=quotation_minute_ab&code={}'
    headers = {
        'Accept': 'application/json; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Connection': 'keep-alive'
    }

    def fetch(self, url, host="finance.pae.baidu.com"):
        """不带token"""
        self.headers['Host'] = host
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(response.content)
        return json.loads(response.content)

    def get_trade_status(self, symbol):
        """获取贸易状态"""
        code = re.findall("\d+", symbol)[-1]
        url = self.quotation.format(code)
        try:
            quotation = self.fetch(url)
            return quotation['Result']['basicinfos']['tradeStatus']
        except Exception:
            return


if __name__ == '__main__':
    s = Snowball()
    t = int(time.time() * 1000)
    print(s.quote('xq_a_token=7024a6bc72f8463c74a9ea9e33051f71286293a2;', 'sh600418,sz002436,sz001696', t))

    g = GuShiTong()
    print(g.get_trade_status('SZ002594'))
