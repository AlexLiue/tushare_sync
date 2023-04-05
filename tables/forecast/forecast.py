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
from utils.utils import exec_create_table_script, exec_sync_with_spec_date_column, get_cfg, query_last_sync_date, \
    max_date


def exec_sync(start_date, end_date):
    exec_sync_with_spec_date_column(
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
        start_date=start_date,
        end_date=end_date,
        limit=3500,
        interval=2)


# 全量初始化表数据
def sync(drop_exist):
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, drop_exist)

    # 查询历史最大同步日期
    begin_date = '19980405'
    cfg = get_cfg()
    date_query_sql = "select max(ann_date) date from %s.forecast" % cfg['mysql']['database']
    last_date = query_last_sync_date(date_query_sql)
    start_date = max_date(last_date, begin_date)
    end_date = str(datetime.datetime.now().strftime('%Y%m%d'))

    exec_sync(start_date, end_date)


if __name__ == '__main__':
    sync(True)
