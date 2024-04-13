#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : reptile.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 获取价格
"""

import requests


class ReptileValue(object):
    api = 'https://19.push2.eastmoney.com/api/qt/ulist/sse?invt=3&pi=0&pz=1&mpi=2000&secids=1.601127&ut=6d2ffaa6a585d612eda28417681d58fb&fields=f12,f13,f19,f14,f139,f148,f2,f4,f1,f125,f18,f3,f152,f5,f30,f31,f32,f6,f8,f7,f10,f22,f9,f112,f100&po='

    headers = {
        'Accept': 'text/event-stream',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': '41.push2.eastmoney.com',
        'Origin': 'https://quote.eastmoney.com',
        'Referer': 'https://quote.eastmoney.com/zixuan/?from=quotecenter',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    def __init__(self):
        pass

    def value(self):
        response = requests.get(url=self.api, headers=self.headers)
        print(response.status_code)
        print(response)
