"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 07:24
# @Author  : PcLiu
# @FileName: repurchase.py
===========================

接口：repurchase
描述：获取上市公司回购股票数据
积分：用户需要至少600积分才可以调取，具体请参阅积分获取办法
tushare 接口说明：https://tushare.pro/document/2?doc_id=124
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
        table_name='repurchase',
        api_name='repurchase',
        fields=[
            "ts_code",
            "ann_date",
            "end_date",
            "proc",
            "exp_date",
            "vol",
            "amount",
            "high_limit",
            "low_limit",
            "repo_goal",
            "update_flag"
        ],
        date_column='ann_date',
        start_date='20100101',
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=360,
        limit=3000,
        interval=0.2
    )


# 增量追加表数据
def append():
    exec_sync_without_ts_code(
        table_name='repurchase',
        api_name='repurchase',
        fields=[
            "ts_code",
            "ann_date",
            "end_date",
            "proc",
            "exp_date",
            "vol",
            "amount",
            "high_limit",
            "low_limit",
            "repo_goal",
            "update_flag"
        ],
        date_column='ann_date',
        start_date=str((datetime.datetime.now() + datetime.timedelta(days=-62)).strftime('%Y%m%d')),
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=360,
        limit=3000,
        interval=0.2
    )


if __name__ == '__main__':
    append()
