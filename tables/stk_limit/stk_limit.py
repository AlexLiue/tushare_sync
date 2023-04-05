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

import datetime
import os

from utils.utils import exec_create_table_script, exec_sync_with_spec_date_column, get_cfg, query_last_sync_date, \
    max_date


def exec_sync(start_date, end_date):
    exec_sync_with_spec_date_column(
        table_name='stk_limit',
        api_name='stk_limit',
        fields=[
            "trade_date",
            "ts_code",
            "up_limit",
            "down_limit",
            "pre_close"
        ],
        date_column='trade_date',
        start_date=start_date,
        end_date=end_date,
        limit=5000,
        interval=0.2)


# 全量初始化表数据
def sync(drop_exist):
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, drop_exist)

    # 查询历史最大同步日期
    begin_date = '20070101'
    cfg = get_cfg()
    date_query_sql = "select max(trade_date) date from %s.stk_limit" % cfg['mysql']['database']
    last_date = query_last_sync_date(date_query_sql)
    start_date = max_date(last_date, begin_date)
    end_date = str(datetime.datetime.now().strftime('%Y%m%d'))

    exec_sync(start_date, end_date)


if __name__ == '__main__':
    sync(True)
