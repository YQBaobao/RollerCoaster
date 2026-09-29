#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtRollerCoaster 
@ File        : data.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
# 假设 quotes 和 symbols 已经定义
quotes = {
    'data': [
        {'symbol': 'SZ002594', 'current': 286.28, 'percent': 0.5, 'chg': 1.42, 'timestamp': 1735283082000,
         'volume': 7868319, 'amount': 2249658028.46, 'market_capital': 832864628969.0,
         'float_market_capital': 332788337680.0, 'turnover_rate': 0.68, 'amplitude': 1.6, 'open': 286.8,
         'last_close': 284.86, 'high': 287.55, 'low': 283.0, 'avg_price': 285.913, 'trade_volume': None, 'side': 0,
         'is_trade': False, 'level': 1, 'trade_session': None, 'trade_type': None, 'current_year_percent': 46.36,
         'trade_unique_id': None, 'type': 11, 'bid_appl_seq_num': None, 'offer_appl_seq_num': None, 'volume_ext': None,
         'traded_amount_ext': None, 'trade_type_v2': None, 'yield_to_maturity': None},
        {'symbol': 'SH601127', 'current': 135.08, 'percent': -0.68, 'chg': -0.92, 'timestamp': 1735282800000,
         'volume': 28771020, 'amount': 3873235835.0, 'market_capital': 203941378630.0,
         'float_market_capital': 203941378630.0, 'turnover_rate': 1.91, 'amplitude': 1.91, 'open': 134.88,
         'last_close': 136.0, 'high': 136.0, 'low': 133.4, 'avg_price': 134.623, 'trade_volume': None, 'side': None,
         'is_trade': False, 'level': 2, 'trade_session': None, 'trade_type': None, 'current_year_percent': 77.7,
         'trade_unique_id': None, 'type': 11, 'bid_appl_seq_num': None, 'offer_appl_seq_num': None, 'volume_ext': None,
         'traded_amount_ext': None, 'trade_type_v2': None, 'yield_to_maturity': None},
        {'symbol': 'SH600418', 'current': 39.46, 'percent': 1.26, 'chg': 0.49, 'timestamp': 1735282800000,
         'volume': 76842303, 'amount': 3038599595.0, 'market_capital': 86181026353.0,
         'float_market_capital': 86181026353.0, 'turnover_rate': 3.52, 'amplitude': 3.62, 'open': 38.95,
         'last_close': 38.97, 'high': 39.97, 'low': 38.56, 'avg_price': 39.543, 'trade_volume': None, 'side': None,
         'is_trade': False, 'level': 2, 'trade_session': None, 'trade_type': None, 'current_year_percent': 144.58,
         'trade_unique_id': None, 'type': 11, 'bid_appl_seq_num': None, 'offer_appl_seq_num': None, 'volume_ext': None,
         'traded_amount_ext': None, 'trade_type_v2': None, 'yield_to_maturity': None},
        {'symbol': 'SH600519', 'current': 1528.97, 'percent': 0.08, 'chg': 1.18, 'timestamp': 1735282800000,
         'volume': 2075932, 'amount': 3170191445.0, 'market_capital': 1920688750266.0,
         'float_market_capital': 1920688750266.0, 'turnover_rate': 0.17, 'amplitude': 1.08, 'open': 1528.9,
         'last_close': 1527.79, 'high': 1536.0, 'low': 1519.5, 'avg_price': 1527.117, 'trade_volume': None,
         'side': None, 'is_trade': False, 'level': 2, 'trade_session': None, 'trade_type': None,
         'current_year_percent': -8.17, 'trade_unique_id': None, 'type': 11, 'bid_appl_seq_num': None,
         'offer_appl_seq_num': None, 'volume_ext': None, 'traded_amount_ext': None, 'trade_type_v2': None,
         'yield_to_maturity': None}
    ],
    'error_code': 0,
    'error_description': None
}

symbols = ['SZ002594', 'SH600519', 'SH601127', 'SH600418']

# 创建一个字典用于查找 quotes 中的数据
quotes_dict = {item['symbol']: item for item in quotes['data']}
current = []
percent = []

for symbol in symbols:
    current.append(quotes_dict[symbol]['current'])
    percent.append(quotes_dict[symbol]['percent'])

print(current, percent)

import sys


def get_windows_version():
    version_info = sys.getwindowsversion()
    build = version_info.build
    return True if build >= 22000 else False


print(get_windows_version())
