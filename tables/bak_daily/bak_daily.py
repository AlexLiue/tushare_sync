"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 14:14
# @Author  : PcLiu
# @FileName: bak_daily.py
===========================

沪深股票-行情数据-备用行情
接口：bak_daily
描述：获取备用行情，包括特定的行情指标
限量：单次最大5000行数据，可以根据日期参数循环获取，正式权限需要5000积分。 2000积分（每分钟最多访问该接口5次）
tushare 接口说明：https://tushare.pro/document/2?doc_id=255
"""

import os
import datetime
from utils.utils import exec_create_table_script, exec_sync_with_spec_date_column, get_cfg, query_last_sync_date, \
    max_date

limit = 5000  # 每次读取记录条数
interval = 15  # 读取的时间间隔, Tushare 限制
begin_date = '20170101'  # Tushare 里数据最早开始时间


def exec_sync(start_date, end_date):
    # Extern Global Var
    global limit
    global interval
    exec_sync_with_spec_date_column(
        table_name='bak_daily',
        api_name='bak_daily',
        fields=[
            "ts_code",
            "trade_date",
            "name",
            "pct_change",
            "close",
            "change",
            "open",
            "high",
            "low",
            "pre_close",
            "vol_ratio",
            "turn_over",
            "swing",
            "vol",
            "amount",
            "selling",
            "buying",
            "total_share",
            "float_share",
            "pe",
            "industry",
            "area",
            "float_mv",
            "total_mv",
            "avg_price",
            "strength",
            "activity",
            "avg_turnover",
            "attack",
            "interval_3",
            "interval_6"
        ],
        date_column='trade_date',
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        interval=interval)


def sync(drop_exist):
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, drop_exist)

    global begin_date
    now = datetime.datetime.now()
    end_date = str(now.strftime('%Y%m%d'))

    # 查询历史最大同步日期
    cfg = get_cfg()
    date_query_sql = "select max(trade_date) date from %s.bak_daily" % cfg['mysql']['database']
    last_date = query_last_sync_date(date_query_sql)
    start_date = max_date(last_date, begin_date)
    exec_sync(start_date, end_date)


if __name__ == '__main__':
    sync(False)
