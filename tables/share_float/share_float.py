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
import datetime
import os

from utils.utils import exec_create_table_script, exec_sync_with_spec_date_column, get_cfg, query_last_sync_date, \
    max_date


def exec_sync(start_date, end_date):
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
        start_date=start_date,
        end_date=end_date,
        limit=300,
        interval=2)


# 全量初始化表数据
def sync(drop_exist):
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, drop_exist)

    # 查询历史最大同步日期
    begin_date = '20070101'
    cfg = get_cfg()
    date_query_sql = "select max(ann_date) date from %s.share_float" % cfg['mysql']['database']
    last_date = query_last_sync_date(date_query_sql)
    start_date = max_date(last_date, begin_date)
    end_date = str(datetime.datetime.now().strftime('%Y%m%d'))

    exec_sync(start_date, end_date)


if __name__ == '__main__':
    sync(False)
