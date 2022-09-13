"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 07:24
# @Author  : PcLiu
# @FileName: share_float.py
===========================

接口：share_float
描述：获取限售股解禁
限量：单次最大5000条，总量不限制
积分：120分可调取，每分钟内限制次数，超过5000积分频次相对较高，具体请参阅积分获取办法
tushare 接口说明：https://tushare.pro/document/2?doc_id=160
"""

import os
import datetime
from utils.utils import exec_mysql_script, exec_sync_with_spec_date_column


# 全量初始化表数据
def init():
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_mysql_script(dir_path)

    exec_sync_with_spec_date_column(
        table_name='share_float',
        api_name='share_float',
        fields=[
            "ts_code",
            "ann_date",
            "float_date",
            "float_share",
            "float_ratio",
            "holder_name",
            "share_type"
        ],
        date_column='ann_date',
        start_date='20100101',
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        limit=3000,
        interval=2
    )


# 增量追加表数据
def append():
    exec_sync_with_spec_date_column(
        table_name='share_float',
        api_name='share_float',
        fields=[
            "ts_code",
            "ann_date",
            "float_date",
            "float_share",
            "float_ratio",
            "holder_name",
            "share_type"
        ],
        date_column='ann_date',
        start_date=str((datetime.datetime.now() + datetime.timedelta(days=-7)).strftime('%Y%m%d')),
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        limit=3000,
        interval=2
    )


if __name__ == '__main__':
    append()




