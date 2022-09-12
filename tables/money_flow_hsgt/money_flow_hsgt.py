"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 11:05
# @Author  : PcLiu
# @FileName: money_flow_hsgt.py
===========================

沪深股票-行情数据-沪深港通资金流向
接口：moneyflow_hsgt，可以通过数据工具调试和查看数据。
描述：获取沪股通、深股通、港股通每日资金流向数据，每次最多返回300条记录，总量不限制。每天18~20点之间完成当日更新
积分要求：2000积分起，5000积分每分钟可提取500次
tushare 接口说明： https://tushare.pro/document/2?doc_id=47
"""


import os
import datetime
from utils.utils import exec_mysql_script, exec_sync

# 全量初始化表数据
def init():
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_mysql_script(dir_path)

    exec_sync(
        table_name='money_flow_hsgt',
        api_name='moneyflow_hsgt',
        fields=[
            "trade_date",
            "ggt_ss",
            "ggt_sz",
            "hgt",
            "sgt",
            "north_money",
            "south_money"
        ],
        start_date='20100101',
        end_date = str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=365,
        limit=300,
        interval=0.2
    )


# 增量追加表数据
def append():
    exec_sync(
        table_name='money_flow_hsgt',
        api_name='moneyflow_hsgt',
        fields=[
            "trade_date",
            "ggt_ss",
            "ggt_sz",
            "hgt",
            "sgt",
            "north_money",
            "south_money"
        ],
        start_date=str((datetime.datetime.now() + datetime.timedelta(days=-20)).strftime('%Y%m%d')),
        end_date = str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=365,
        limit=300,
        interval=0.2
    )

if __name__ == '__main__':
    init()


