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
from utils.utils import exec_mysql_script, exec_sync_without_ts_code

# 全量初始化表数据
def init():
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_mysql_script(dir_path)

    exec_sync_without_ts_code(
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
        date_column='end_date',
        start_date='20100331',
        end_date = str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=1,
        limit=3000,
        interval=0.2
    )


# 增量追加表数据
def append():
    exec_sync_without_ts_code(
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
        date_column='end_date',
        start_date=str((datetime.datetime.now() + datetime.timedelta(days=-30)).strftime('%Y%m%d')),
        end_date = str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=1,
        limit=3000,
        interval=0.2
    )


if __name__ == '__main__':
    append()

