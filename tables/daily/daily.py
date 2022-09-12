"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 06:40
# @Author  : PcLiu
# @FileName: daily.py
===========================

沪深股票-行情数据-A股日线行情
接口：daily，可以通过数据工具调试和查看数据
数据说明：交易日每天15点～16点之间入库。本接口是未复权行情，停牌期间不提供数据
调取说明：120积分每分钟内最多调取500次，每次5000条数据，相当于单次提取23年历史
描述：获取股票行情数据，或通过通用行情接口获取数据，包含了前后复权数据
tushare 接口说明：https://tushare.pro/document/2?doc_id=27
"""

import os
import datetime
from utils.utils import exec_mysql_script, exec_sync_without_ts_code

# 全量初始化表数据
def init():
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_mysql_script(dir_path)

    exec_sync_without_ts_code(
        table_name='daily',
        api_name='daily',
        fields=[
            "ts_code",
            "trade_date",
            "open",
            "high",
            "low",
            "close",
            "pre_close",
            "change",
            "pct_chg",
            "vol",
            "amount"
        ],
        start_date='19901219',
        end_date = str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=1,
        limit=5000,
        interval=0.3
    )


# 增量追加表数据
def append():
    exec_sync_without_ts_code(
        table_name='daily',
        api_name='daily',
        fields=[
            "ts_code",
            "trade_date",
            "open",
            "high",
            "low",
            "close",
            "pre_close",
            "change",
            "pct_chg",
            "vol",
            "amount"
        ],
        start_date=str((datetime.datetime.now() + datetime.timedelta(days=-7)).strftime('%Y%m%d')),
        end_date = str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=1,
        limit=5000,
        interval=0.3
    )


if __name__ == '__main__':
    append()


