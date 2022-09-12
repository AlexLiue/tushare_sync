"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 12:04
# @Author  : PcLiu
# @FileName: hsgt_top10.py
===========================

沪深股票-行情数据-沪深股通十大成交股
接口：hsgt_top10
描述：获取沪股通、深股通每日前十大成交详细数据，每天18~20点之间完成当日更新
tushare 接口说明：https://tushare.pro/document/2?doc_id=48
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
        table_name='hsgt_top10',
        api_name='hsgt_top10',
        fields=[
            "trade_date",
            "ts_code",
            "name",
            "close",
            "change",
            "rank",
            "market_type",
            "amount",
            "net_amount",
            "buy",
            "sell"
        ],
        date_column='trade_date',
        start_date='20100101',
        end_date = str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=365,
        limit=5000,
        interval=0.2
    )


# 增量追加表数据
def append():
    exec_sync_without_ts_code(
        table_name='hsgt_top10',
        api_name='hsgt_top10',
        fields=[
            "trade_date",
            "ts_code",
            "name",
            "close",
            "change",
            "rank",
            "market_type",
            "amount",
            "net_amount",
            "buy",
            "sell"
        ],
        date_column='trade_date',
        start_date=str((datetime.datetime.now() + datetime.timedelta(days=-30)).strftime('%Y%m%d')),
        end_date = str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=365,
        limit=5000,
        interval=0.2
    )


if __name__ == '__main__':
    append()

