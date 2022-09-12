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
from utils.utils import exec_mysql_script, exec_sync_without_ts_code

# 全量初始化表数据
def init():
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_mysql_script(dir_path)

    exec_sync_without_ts_code(
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
        start_date='20170101',
        end_date = str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=1,
        limit=5000,
        interval=13
    )


# 增量追加表数据
def append():
    exec_sync_without_ts_code(
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
        start_date=str((datetime.datetime.now() + datetime.timedelta(days=-7)).strftime('%Y%m%d')),
        end_date = str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=1,
        limit=5000,
        interval=13
    )


if __name__ == '__main__':
    append()

