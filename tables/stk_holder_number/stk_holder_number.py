"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/13 16:24
# @Author  : PcLiu
# @FileName: stk_holdernumber.py
===========================
接口：stk_holdernumber
描述：获取上市公司股东户数数据，数据不定期公布
限量：单次最大3000,总量不限制
积分：600积分可调取，基础积分每分钟调取100次，5000积分以上频次相对较高。具体请参阅积分获取办法
tushare 接口说明：https://tushare.pro/document/2?doc_id=166
"""

import os
import datetime
from utils.utils import exec_mysql_script, exec_sync_with_spec_date_column, exec_sync_without_ts_code


# 全量初始化表数据
def init():
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_mysql_script(dir_path)

    exec_sync_without_ts_code(
        table_name='stk_holder_number',
        api_name='stk_holdernumber',
        fields=[
            "ts_code",
            "ann_date",
            "end_date",
            "holder_num",
            "holder_nums"
        ],
        date_column='ann_date',
        start_date='20100101',
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=356,
        limit=3000,
        interval=0.5
    )


# 增量追加表数据
def append():
    exec_sync_without_ts_code(
        table_name='stk_holder_number',
        api_name='stk_holdernumber',
        fields=[
            "ts_code",
            "ann_date",
            "end_date",
            "holder_num",
            "holder_nums"
        ],
        date_column='ann_date',
        start_date=str((datetime.datetime.now() + datetime.timedelta(days=-186)).strftime('%Y%m%d')),
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=356,
        limit=3000,
        interval=0.5
    )


if __name__ == '__main__':
    append()




