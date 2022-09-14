"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 06:40
# @Author  : PcLiu
# @FileName: fina_mainbz.py
===========================

沪深股票-财务数据-主营业务构成  
接口：fina_mainbz，可以通过数据工具调试和查看数据。
描述：获取上市公司财务指标数据，为避免服务器压力，现阶段每次请求最多返回60条记录，可通过设置日期多次请求获取更多数据。
权限：用户需要至少800积分才可以调取，具体请参阅积分获取办法, 每分钟最多访问该接口60次
tushare 接口说明：https://tushare.pro/document/2?doc_id=79
"""

import os
import datetime
from utils.utils import exec_mysql_script, exec_sync_with_ts_code

fields=[
    "ts_code",
    "end_date",
    "bz_item",
    "bz_sales",
    "bz_profit",
    "bz_cost",
    "curr_type",
    "bz_code",
    "update_flag"
]


# 全量初始化表数据
def init():
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_mysql_script(dir_path)

    global fields
    exec_sync_with_ts_code(
        table_name='fina_mainbz',
        api_name='fina_mainbz',
        fields=fields,
        date_column='end_date',
        start_date='20040101',
        end_date = str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=3650,
        limit=1000,
        interval=1.1,
        ts_code_limit=1
    )

# 增量追加表数据
def append():
    exec_sync_with_ts_code(
        table_name='fina_mainbz',
        api_name='fina_mainbz',
        fields=fields,
        date_column='end_date',
        start_date=str((datetime.datetime.now() + datetime.timedelta(days=-62)).strftime('%Y%m%d')),
        end_date = str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=365,
        limit=1000,
        interval=1.1,
        ts_code_limit=1
    )


if __name__ == '__main__':
    init()
