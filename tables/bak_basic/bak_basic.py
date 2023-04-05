"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 05:51
# @Author  : PcLiu
# @FileName: bak_basic.py
===========================

沪深股票-基础信息-备用列表 (数据量较大, 2000积分每分钟只能调用2次,独立处理)
接口：hs_const
描述：获取沪股通、深股通成分数据
tushare 接口说明： https://tushare.pro/document/2?doc_id=262
"""

import os
import datetime
from utils.utils import exec_create_table_script, query_last_sync_date, \
    max_date, exec_sync_with_spec_date_column, get_cfg

limit = 5000  # 每次读取记录条数
interval = 31  # 读取的时间间隔, Tushare 限制每分钟 2次 API 调用
begin_date = '20160101'  # Tushare 里数据最早开始时间


def exec_sync(start_date, end_date):
    # Extern Global Var
    global limit
    global interval
    exec_sync_with_spec_date_column(
        table_name='bak_basic',
        api_name='bak_basic',
        fields=[
            "trade_date",
            "ts_code",
            "name",
            "industry",
            "area",
            "pe",
            "float_share",
            "total_share",
            "total_assets",
            "liquid_assets",
            "fixed_assets",
            "reserved",
            "reserved_pershare",
            "eps",
            "bvps",
            "pb",
            "list_date",
            "undp",
            "per_undp",
            "rev_yoy",
            "profit_yoy",
            "gpr",
            "npr",
            "holder_num"
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
    date_query_sql = "select max(trade_date) date from %s.bak_basic" % cfg['mysql']['database']
    last_date = query_last_sync_date(date_query_sql)
    start_date = max_date(last_date, begin_date)
    exec_sync(start_date, end_date)


if __name__ == '__main__':
    sync(False)
