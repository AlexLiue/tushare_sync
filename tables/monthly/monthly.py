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

import datetime
import os

from utils.utils import exec_create_table_script, exec_sync_with_spec_date_column, get_cfg, query_last_sync_date, \
    max_date


def exec_sync(start_date, end_date):
    exec_sync_with_spec_date_column(
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
        start_date=start_date,
        end_date=end_date,
        limit=4500,
        interval=1)


# 全量初始化表数据
def sync(drop_exist):
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, drop_exist)

    # 查询历史最大同步日期
    begin_date = '19901201'
    cfg = get_cfg()
    date_query_sql = "select max(trade_date) date from %s.monthly" % cfg['mysql']['database']
    last_date = query_last_sync_date(date_query_sql)
    start_date = max_date(last_date, begin_date)
    end_date = str(datetime.datetime.now().strftime('%Y%m%d'))

    exec_sync(start_date, end_date)


if __name__ == '__main__':
    sync(True)
