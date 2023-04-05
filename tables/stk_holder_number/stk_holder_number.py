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
import datetime
import os

from utils.utils import exec_create_table_script, exec_sync_with_spec_date_column, get_cfg, query_last_sync_date, \
    max_date


def exec_sync(start_date, end_date):
    exec_sync_with_spec_date_column(
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
        start_date=start_date,
        end_date=end_date,
        limit=3000,
        interval=0.5)


# 全量初始化表数据
def sync(drop_exist):
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, drop_exist)

    # 查询历史最大同步日期
    begin_date = '20070101'
    cfg = get_cfg()
    date_query_sql = "select max(ann_date) date from %s.stk_holder_number" % cfg['mysql']['database']
    last_date = query_last_sync_date(date_query_sql)
    start_date = max_date(last_date, begin_date)
    end_date = str(datetime.datetime.now().strftime('%Y%m%d'))

    exec_sync(start_date, end_date)


if __name__ == '__main__':
    sync(True)
