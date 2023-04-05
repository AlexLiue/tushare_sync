"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 12:55
# @Author  : PcLiu
# @FileName: disclosure_date.py
===========================

沪深股票-财务数据-财报披露计划
接口：disclosure_date
描述：获取财报披露计划日期
限量：单次最大3000，总量不限制
积分：用户需要至少500积分才可以调取，积分越多权限越大，具体请参阅积分获取办法
tushare 接口说明：https://tushare.pro/document/2?doc_id=162
"""

import os
import datetime
from utils.utils import exec_create_table_script, exec_sync_with_spec_date_column, query_last_sync_date, max_date, \
    get_cfg

begin_date = "20100331"
limit = 1000
interval = 0.4
date_step = 1


def exec_sync(start_date, end_date):
    global limit
    global interval
    global date_step
    exec_sync_with_spec_date_column(
        table_name='disclosure_date',
        api_name='disclosure_date',
        fields=[
            "ts_code",
            "ann_date",
            "end_date",
            "pre_date",
            "actual_date",
            "modify_date"
        ],
        date_column='ann_date',
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        interval=interval)


# 全量初始化表数据
def sync(drop_exist):
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, drop_exist)

    # 查询历史最大同步日期
    global begin_date
    cfg = get_cfg()
    date_query_sql = "select max(ann_date) date from %s.disclosure_date" % cfg['mysql']['database']
    last_date = query_last_sync_date(date_query_sql)
    start_date = max_date(last_date, begin_date)
    end_date = str(datetime.datetime.now().strftime('%Y%m%d'))

    exec_sync(start_date, end_date)


if __name__ == '__main__':
    sync(False)
