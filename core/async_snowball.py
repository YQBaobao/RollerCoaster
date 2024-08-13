#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : RollerCoaster 
@ File        : async_snowball.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 雪球数据
"""
import json
import re
import time

import aiohttp
import asyncio


class Snowball(object):
    realtime_quote = "https://stock.xueqiu.com/v5/stock/realtime/quotec.json?symbol="
    realtime_quote_detail = "https://stock.xueqiu.com/v5/stock/quote.json?extend=detail&symbol="
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Xueqiu iPhone 11.8',
        'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
        'Accept-Encoding': 'br, gzip, deflate',
        'Connection': 'keep-alive'

    }

    async def async_fetch_token(self, url, host="stock.xueqiu.com"):
        self.headers['Host'] = host
        self.headers['Cookie'] = self.token
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as resp:
                if resp.status != 200:
                    raise Exception(await resp.text())
                return json.loads(await resp.text())

    async def async_fetch(self, url, host="stock.xueqiu.com"):
        self.headers['Host'] = host
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as resp:
                if resp.status != 200:
                    raise Exception(await resp.text())
                return json.loads(await resp.text())

    async def async_quote(self, symbol, timestamp):
        url = self.realtime_quote + symbol + f'&_={timestamp}'
        return await self.async_fetch(url)

    async def async_quote_detail(self, token, symbol, timestamp):
        self.token = token
        url = self.realtime_quote_detail + symbol + f'&_={timestamp}'
        return await self.async_fetch_token(url)


class GuShiTong(object):
    quotation = 'https://finance.pae.baidu.com/vapi/v1/getquotation?group=quotation_minute_ab&code={}'
    headers = {
        'Accept': 'application/json; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Connection': 'keep-alive'
    }

    async def async_fetch(self, url, host="finance.pae.baidu.com"):
        """不带token"""
        self.headers['Host'] = host
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as resp:
                if resp.status != 200:
                    raise Exception(await resp.text())
                return json.loads(await resp.text())

    async def async_get_trade_status(self, symbol):
        """获取贸易状态"""
        code = re.findall("\d+", symbol)[-1]
        url = self.quotation.format(code)
        try:
            quotation = await self.async_fetch(url)
            return quotation['Result']['basicinfos']['tradeStatus']
        except Exception:
            return


if __name__ == '__main__':
    s = Snowball()
    t = int(time.time() * 1000)
    loop = asyncio.get_event_loop()
    x = loop.run_until_complete(s.async_quote('SH601127', t))
    print(type(x), x)

    g = GuShiTong()
    print(loop.run_until_complete(g.async_get_trade_status('SZ002594')))
