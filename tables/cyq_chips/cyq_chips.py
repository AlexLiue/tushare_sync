"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/13 17:07
# @Author  : PcLiu
# @FileName: cyq_chips.py
===========================

接口：cyq_chips
描述：获取A股每日的筹码分布情况，提供各价位占比，数据从2010年开始，每天17~18点之间更新当日数据
来源：Tushare社区
限量：单次最大2000条，可以按股票代码和日期循环提取
积分：120积分可以试用查看数据，5000积分每天20000次，10000积分每天200000次，15000积分每天不限总量

您每分钟最多访问该接口5次
您每小时最多访问该接口10次
tushare 接口说明：https://tushare.pro/document/2?doc_id=294
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
        table_name='cyq_chips',
        api_name='cyq_chips',
        fields=[
            "ts_code",
            "trade_date",
            "price",
            "percent"
        ],
        date_column='trade_date',
        start_date='20050101',
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=2,
        limit=2000,
        interval=13
    )


# 增量追加表数据
def append():
    exec_sync_without_ts_code(
        table_name='cyq_chips',
        api_name='cyq_chips',
        fields=[
            "ts_code",
            "trade_date",
            "price",
            "percent"
        ],
        date_column='trade_date',
        start_date=str((datetime.datetime.now() + datetime.timedelta(days=0)).strftime('%Y%m%d')),
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=1,
        limit=2000,
        interval=13
    )


if __name__ == '__main__':
    append()


