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
from utils.utils import exec_create_table_script, exec_sync_with_spec_date_column, query_last_sync_date, max_date, \
    get_cfg


def exec_sync(start_date, end_date):
    exec_sync_with_spec_date_column(
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
        date_column='trade_date',
        start_date=start_date,
        end_date=end_date,
        limit=5000,
        interval=0.3)


# 全量初始化表数据
def sync(drop_exist):
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, drop_exist)

    # 查询历史最大同步日期
    begin_date = '19901219'
    cfg = get_cfg()
    date_query_sql = "select max(trade_date) date from %s.daily" % cfg['mysql']['database']
    last_date = query_last_sync_date(date_query_sql)
    start_date = max_date(last_date, begin_date)
    end_date = str(datetime.datetime.now().strftime('%Y%m%d'))

    exec_sync(start_date, end_date)


if __name__ == '__main__':
    sync(False)
