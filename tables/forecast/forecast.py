"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 06:40
# @Author  : PcLiu
# @FileName: forecast.py
===========================

沪深股票-财务数据-业绩预告
接口：forecast，可以通过数据工具调试和查看数据。 每次 3500 条
描述：获取业绩预告数据
权限：用户需要至少800积分才可以调取，具体请参阅积分获取办法

提示：当前接口只能按单只股票获取其历史数据，如果需要获取某一季度全部上市公司数据，请使用forecast_vip接口（参数一致），需积攒5000积分。
tushare 接口说明：https://tushare.pro/document/2?doc_id=45
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
        table_name='forecast',
        api_name='forecast',
        fields=[
            "ts_code",
            "ann_date",
            "end_date",
            "type",
            "p_change_min",
            "p_change_max",
            "net_profit_min",
            "net_profit_max",
            "last_parent_net",
            "first_ann_date",
            "summary",
            "change_reason",
            "notice_times"
        ],
        date_column='ann_date',
        start_date='19980101',
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=365,
        limit=3500,
        interval=2
    )


# 增量追加表数据
def append():
    exec_sync_without_ts_code(
        table_name='forecast',
        api_name='forecast',
        fields=[
            "ts_code",
            "ann_date",
            "end_date",
            "type",
            "p_change_min",
            "p_change_max",
            "net_profit_min",
            "net_profit_max",
            "last_parent_net",
            "first_ann_date",
            "summary",
            "change_reason",
            "notice_times"
        ],
        date_column='ann_date',
        start_date=str((datetime.datetime.now() + datetime.timedelta(days=-180)).strftime('%Y%m%d')),
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=365,
        limit=3500,
        interval=2
    )


if __name__ == '__main__':
    append()
