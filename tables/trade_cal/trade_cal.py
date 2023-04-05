"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/9 21:33
# @Author  : PcLiu
# @FileName: t.py
===========================

沪深股票-基础信息-交易日历
接口：trade_cal，可以通过数据工具调试和查看数据。
描述：获取各大交易所交易日历数据,默认提取的是上交所
tushare 接口说明： https://tushare.pro/document/2?doc_id=26
"""

import datetime
import os

from utils.utils import exec_create_table_script, exec_sync_with_spec_date_column_v2, get_cfg, query_last_sync_date, \
    max_date


def exec_sync(start_date, end_date):
    exec_sync_with_spec_date_column_v2(
        table_name='trade_cal',
        api_name='trade_cal',
        fields=[
            "exchange",
            "cal_date",
            "is_open",
            "pretrade_date"
        ],
        date_column='cal_date',
        start_date=start_date,
        end_date=end_date,
        limit=10000,
        interval=0.4,
        date_step=3600)


# 全量初始化表数据
def sync(drop_exist):
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, drop_exist)

    # 查询历史最大同步日期
    begin_date = '19901221'
    cfg = get_cfg()
    date_query_sql = "select max(cal_date) date from %s.trade_cal" % cfg['mysql']['database']
    last_date = query_last_sync_date(date_query_sql)
    start_date = max_date(last_date, begin_date)
    end_date = str(datetime.datetime.now().strftime('%Y%m%d'))

    exec_sync(start_date, end_date)


if __name__ == '__main__':
    sync(False)
