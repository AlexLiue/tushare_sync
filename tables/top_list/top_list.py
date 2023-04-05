"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 07:24
# @Author  : PcLiu
# @FileName: top_list.py
===========================

沪深股票-市场参考数据-融资融券交易明细
接口：top_list
描述：获取沪深两市每日融资融券明细
tushare 接口说明：https://tushare.pro/document/2?doc_id=106

接口：top_list
描述：龙虎榜每日交易明细
数据历史： 2005年至今
限量：单次最大10000
积分：用户需要至少300积分才可以调取，具体请参阅积分获取办法
"""


import datetime
import os

from utils.utils import exec_create_table_script, exec_sync_with_spec_date_column, get_cfg, query_last_sync_date, \
    max_date


def exec_sync(start_date, end_date):
    exec_sync_with_spec_date_column(
        table_name='top_list',
        api_name='top_list',
        fields=[
            "trade_date",
            "ts_code",
            "name",
            "close",
            "pct_change",
            "turnover_rate",
            "amount",
            "l_sell",
            "l_buy",
            "l_amount",
            "net_amount",
            "net_rate",
            "amount_rate",
            "float_values",
            "reason"
        ],
        date_column='trade_date',
        start_date=start_date,
        end_date=end_date,
        limit=10000,
        interval=0.4)


# 全量初始化表数据
def sync(drop_exist):
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, drop_exist)

    # 查询历史最大同步日期
    begin_date = '20050101'
    cfg = get_cfg()
    date_query_sql = "select max(trade_date) date from %s.top_list" % cfg['mysql']['database']
    last_date = query_last_sync_date(date_query_sql)
    start_date = max_date(last_date, begin_date)
    end_date = str(datetime.datetime.now().strftime('%Y%m%d'))

    exec_sync(start_date, end_date)


if __name__ == '__main__':
    sync(True)
