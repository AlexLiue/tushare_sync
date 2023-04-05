"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/13 17:07
# @Author  : PcLiu
# @FileName: cyq_perf.py
===========================
接口：cyq_perf
描述：获取A股每日筹码平均成本和胜率情况，每天17~18点左右更新，数据从2005年开始
来源：Tushare社区
限量：单次最大5000条，可以分页或者循环提取
积分：120积分可以试用(查看数据)，5000积分每天20000次，10000积分每天200000次，15000积分每天不限总量
您每分钟最多访问该接口5次
您每小时最多访问该接口10次
tushare 接口说明：https://tushare.pro/document/2?doc_id=293
"""

import os
import datetime
from utils.utils import exec_create_table_script, exec_sync_without_ts_code


# 全量初始化表数据
def init(drop_exist):
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, drop_exist)

    exec_sync_without_ts_code(
        table_name='cyq_perf',
        api_name='cyq_perf',
        fields=[
            "ts_code",
            "trade_date",
            "his_low",
            "his_high",
            "cost_5pct",
            "cost_15pct",
            "cost_50pct",
            "cost_85pct",
            "cost_95pct",
            "weight_avg",
            "winner_rate"
        ],
        date_column='trade_date',
        start_date='20050101',
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=10,
        limit=5000,
        interval=13
    )


# 增量追加表数据
def append():
    exec_sync_without_ts_code(
        table_name='cyq_perf',
        api_name='cyq_perf',
        fields=[
            "ts_code",
            "trade_date",
            "his_low",
            "his_high",
            "cost_5pct",
            "cost_15pct",
            "cost_50pct",
            "cost_85pct",
            "cost_95pct",
            "weight_avg",
            "winner_rate"
        ],
        date_column='trade_date',
        start_date=str((datetime.datetime.now() + datetime.timedelta(days=-3)).strftime('%Y%m%d')),
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=10,
        limit=5000,
        interval=13
    )


if __name__ == '__main__':
    append()
