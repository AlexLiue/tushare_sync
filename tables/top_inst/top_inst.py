"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/13 13:47
# @Author  : PcLiu
# @FileName: top_inst.py
===========================

沪深股票-市场参考数据-融资融券交易明细
接口：top_inst
描述：龙虎榜机构成交明细
限量：单次最大10000
积分：用户需要至少300积分才可以调取，具体请参阅积分获取办法
tushare 接口说明：https://tushare.pro/document/2?doc_id=107
"""

import os
import datetime
from utils.utils import exec_mysql_script, exec_sync_with_spec_date_column


# 全量初始化表数据
def init():
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_mysql_script(dir_path)

    exec_sync_with_spec_date_column(
        table_name='top_inst',
        api_name='top_inst',
        fields=[
            "trade_date",
            "ts_code",
            "exalter",
            "buy",
            "buy_rate",
            "sell",
            "sell_rate",
            "net_buy",
            "side",
            "reason"
        ],
        date_column='trade_date',
        start_date='20050101',
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        limit=10000,
        interval=0.4
    )


# 增量追加表数据
def append():
    exec_sync_with_spec_date_column(
        table_name='top_inst',
        api_name='top_inst',
        fields=[
            "trade_date",
            "ts_code",
            "exalter",
            "buy",
            "buy_rate",
            "sell",
            "sell_rate",
            "net_buy",
            "side",
            "reason"
        ],
        date_column='trade_date',
        start_date=str((datetime.datetime.now() + datetime.timedelta(days=-10)).strftime('%Y%m%d')),
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        limit=3000,
        interval=0.4
    )


if __name__ == '__main__':
    append()
