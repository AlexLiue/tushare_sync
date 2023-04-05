"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 12:55
# @Author  : PcLiu
# @FileName: ggt_daily.py
===========================

沪深股票-行情数据-港股通每日成交统计
接口：ggt_daily
描述：获取港股通每日成交信息，数据从2014年开始
限量：单次最大1000，总量数据不限制
积分：用户积2000积分可调取(每分钟2次)，5000积分以上频次相对较高，请自行提高积分，具体请参阅积分获取办法
tushare 接口说明：https://tushare.pro/document/2?doc_id=196
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
        table_name='ggt_daily',
        api_name='ggt_daily',
        fields=[
            "trade_date",
            "buy_amount",
            "buy_volume",
            "sell_amount",
            "sell_volume"
        ],
        date_column='trade_date',
        start_date='20100101',
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=365,
        limit=1000,
        interval=30
    )


# 增量追加表数据
def append():
    exec_sync_without_ts_code(
        table_name='ggt_daily',
        api_name='ggt_daily',
        fields=[
            "trade_date",
            "buy_amount",
            "buy_volume",
            "sell_amount",
            "sell_volume"
        ],
        date_column='trade_date',
        start_date=str((datetime.datetime.now() + datetime.timedelta(days=-30)).strftime('%Y%m%d')),
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=365,
        limit=1000,
        interval=30
    )


if __name__ == '__main__':
    append()
