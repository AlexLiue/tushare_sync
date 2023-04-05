"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 12:55
# @Author  : PcLiu
# @FileName: ggt_daily.py
===========================

沪深股票-行情数据-港股通每日成交统计
接口：ggt_daily
描述：获取港股通每日成交信息，数据从2014年开始
限量：单次最大1000，总量数据不限制
积分：用户积2000积分可调取(每分钟2次)，5000积分以上频次相对较高，请自行提高积分，具体请参阅积分获取办法
tushare 接口说明：https://tushare.pro/document/2?doc_id=196
"""

import os
import datetime
from utils.utils import exec_create_table_script, exec_sync_with_spec_date_column, get_cfg, query_last_sync_date, \
    max_date


def exec_sync(start_date, end_date):
    exec_sync_with_spec_date_column(
        table_name='ggt_daily',
        api_name='ggt_daily',
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
        date_column='trade_date',
        start_date=start_date,
        end_date=end_date,
        limit=1000,
        interval=35)


# 全量初始化表数据
def sync(drop_exist):
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, drop_exist)

    # 查询历史最大同步日期
    begin_date = '20100101'
    cfg = get_cfg()
    date_query_sql = "select max(trade_date) date from %s.ggt_daily" % cfg['mysql']['database']
    last_date = query_last_sync_date(date_query_sql)
    start_date = max_date(last_date, begin_date)
    end_date = str(datetime.datetime.now().strftime('%Y%m%d'))

    exec_sync(start_date, end_date)


if __name__ == '__main__':
    sync(True)
