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
    home = "https://www.xueqiu.com/hq"
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

    def __init__(self):
        self.token = None

    def get_token(self):
        """自动获取 token（访问首页，从 cookie 中解析）"""
        headers = {key: value for key, value in self.headers.items() if key not in ('Host', 'Cookie')}
        response = requests.get(self.home, headers=headers)
        if response.status_code != 200:
            raise Exception(response.content)
        self.token = response.cookies.get('xq_a_token')
        if not self.token:
            raise Exception('获取 token 失败')
        return self.token

    def fetch(self, url, token=None, host="stock.xueqiu.com"):
        """带token"""
        self.headers['Host'] = host
        self.headers['Cookie'] = token if token else f'xq_a_token={self.token or self.get_token()};'
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(response.content)
        response_body = json.loads(response.content)
        if response_body.get('error_code', 0) != 0:  # token 过期或失效，例如 400016
            raise Exception(response_body.get('error_description'))
        return response_body

    @staticmethod
    def format_quote(response):
        """格式化行情数据"""
        quote_dict = {'data': []}
        for item in response['data']['items']:
            quote = item['quote']
            quote_dict['data'].append({"symbol": quote['symbol'].lower(),
                                       "current": quote['current'],
                                       "percent": quote['percent']})
        return quote_dict

    def quote(self, symbol, timestamp, token=None):
        """行情数据（token 过期时自动重新获取并重试一次）"""
        url = self.realtime_quote + symbol + f'&_={timestamp}'
        try:
            return self.format_quote(self.fetch(url, token))
        except Exception:
            if token:  # 手动指定的 token 失效时不重试
                raise
            self.token = None  # 丢弃失效 token，重新获取后再试一次
            return self.format_quote(self.fetch(url))


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
    print(s.quote('SH603327,SH600203,SZ000823', t))

    # g = GuShiTong()
    # print(g.get_trade_status('SZ002594'))
