"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 10:31
# @Author  : PcLiu
# @FileName: stk_limit.py
===========================

沪深股票-行情数据-每日涨跌停价格
接口：stk_limit
描述：获取全市场（包含A/B股和基金）每日涨跌停价格，包括涨停价格，跌停价格等，每个交易日8点40左右更新当日股票涨跌停价格。
限量：单次最多提取5800条记录，可循环调取，总量不限制
积分：用户积600积分可调取，单位分钟有流控，积分越高流量越大，请自行提高积分，具体请参阅积分获取办法
tushare 接口说明： https://tushare.pro/document/2?doc_id=183
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
        table_name='stk_limit',
        api_name='stk_limit',
        fields=[
            "trade_date",
            "ts_code",
            "up_limit",
            "down_limit",
            "pre_close"
        ],
        start_date='20070101',
        end_date = str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=1,
        limit=5000,
        interval=0.2
    )


# 增量追加表数据
def append():
    exec_sync_without_ts_code(
        table_name='stk_limit',
        api_name='stk_limit',
        fields=[
            "trade_date",
            "ts_code",
            "up_limit",
            "down_limit",
            "pre_close"
        ],
        start_date=str((datetime.datetime.now() + datetime.timedelta(days=-10)).strftime('%Y%m%d')),
        end_date = str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=1,
        limit=5000,
        interval=0.2
    )


if __name__ == '__main__':
    append()

