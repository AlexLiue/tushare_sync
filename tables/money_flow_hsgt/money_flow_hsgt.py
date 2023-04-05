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


import datetime
import os

from utils.utils import exec_create_table_script, exec_sync_with_spec_date_column, get_cfg, query_last_sync_date, \
    max_date


def exec_sync(start_date, end_date):
    exec_sync_with_spec_date_column(
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
        date_column='trade_date',
        start_date=start_date,
        end_date=end_date,
        limit=300,
        interval=0.2)


# 全量初始化表数据
def sync(drop_exist):
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, drop_exist)

    # 查询历史最大同步日期
    begin_date = '20100101'
    cfg = get_cfg()
    date_query_sql = "select max(trade_date) date from %s.money_flow_hsgt" % cfg['mysql']['database']
    last_date = query_last_sync_date(date_query_sql)
    start_date = max_date(last_date, begin_date)
    end_date = str(datetime.datetime.now().strftime('%Y%m%d'))

    exec_sync(start_date, end_date)


if __name__ == '__main__':
    sync(True)
