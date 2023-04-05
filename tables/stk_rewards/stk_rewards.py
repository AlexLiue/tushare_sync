"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/9 22:50
# @Author  : PcLiu
# @FileName: stk_rewards.py
===========================

沪深股票-基础信息-管理层薪酬和持股（数据量较大,不存在日更新逻辑, 选择性同步）
接口：stk_rewards
描述：获取上市公司管理层薪酬和持股
tushare 接口说明： https://tushare.pro/document/2?doc_id=194
"""

import os
import datetime
from utils.utils import exec_create_table_script, exec_sync_without_ts_code, exec_sync_with_ts_code

fields = [
    "ts_code",
    "ann_date",
    "end_date",
    "name",
    "title",
    "reward",
    "hold_vol"
]


# 全量初始化表数据
def init(drop_exist):
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, drop_exist)

    global fields
    exec_sync_with_ts_code(
        table_name='stk_rewards',
        api_name='stk_rewards',
        fields=fields,
        date_column='end_date',
        start_date='19940416',
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=1,
        limit=5000,
        interval=0.3,
        ts_code_limit=1000
    )


# 增量追加表数据
def append():
    exec_sync_with_ts_code(
        table_name='stk_rewards',
        api_name='stk_rewards',
        fields=fields,
        date_column='end_date',
        start_date=str((datetime.datetime.now() + datetime.timedelta(days=-62)).strftime('%Y%m%d')),
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=1,
        limit=5000,
        interval=0.3,
        ts_code_limit=1000
    )


if __name__ == '__main__':
    init()
