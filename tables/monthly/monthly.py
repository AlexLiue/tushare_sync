"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 07:24
# @Author  : PcLiu
# @FileName: monthly.py
===========================

沪深股票-行情数据-A股月线行情
接口：monthly
描述：获取A股月线数据
限量：单次最大4500行，总量不限制
积分：用户需要至少300积分才可以调取，具体请参阅积分获取办法
tushare 接口说明：https://tushare.pro/document/2?doc_id=144
"""

import os
import datetime
from utils.utils import exec_create_table_script, exec_sync_without_ts_code


# 全量初始化表数据
def init(drop_exist):
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, drop_exist)

    exec_sync_without_ts_code(
        table_name='monthly',
        api_name='monthly',
        fields=[
            "ts_code",
            "trade_date",
            "close",
            "open",
            "high",
            "low",
            "pre_close",
            "change",
            "pct_chg",
            "vol",
            "amount"
        ],
        date_column='trade_date',
        start_date='19901201',
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=31,
        limit=4500,
        interval=1
    )


# 增量追加表数据
def append():
    exec_sync_without_ts_code(
        table_name='monthly',
        api_name='monthly',
        fields=[
            "ts_code",
            "trade_date",
            "close",
            "open",
            "high",
            "low",
            "pre_close",
            "change",
            "pct_chg",
            "vol",
            "amount"
        ],
        date_column='trade_date',
        start_date=str((datetime.datetime.now() + datetime.timedelta(days=-62)).strftime('%Y%m%d')),
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=31,
        limit=4500,
        interval=1
    )


if __name__ == '__main__':
    append()
