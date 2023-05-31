"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 12:30
# @Author  : PcLiu
# @FileName: ggt_top10.py
===========================

沪深股票-行情数据-港股通十大成交股
接口：ggt_top10
描述：获取港股通每日成交数据，其中包括沪市、深市详细数据，每天18~20点之间完成当日更新
tushare 接口说明：https://tushare.pro/document/2?doc_id=49
"""


import os
import datetime
from utils.utils import exec_create_table_script, exec_sync_with_spec_date_column, get_cfg, query_last_sync_date, \
    max_date


def exec_sync(start_date, end_date):
    exec_sync_with_spec_date_column(
        table_name='ggt_top10',
        api_name='ggt_top10',
        fields=[
            "trade_date",
            "ts_code",
            "name",
            "close",
            "p_change",
            "rank",
            "market_type",
            "amount",
            "net_amount",
            "sh_amount",
            "sh_net_amount",
            "sh_buy",
            "sh_sell",
            "sz_amount",
            "sz_net_amount",
            "sz_buy",
            "sz_sell"
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
    begin_date = '20150107'
    cfg = get_cfg()
    date_query_sql = "select max(trade_date) date from %s.ggt_top10" % cfg['mysql']['database']
    last_date = query_last_sync_date(date_query_sql)
    start_date = max_date(last_date, begin_date)
    end_date = str(datetime.datetime.now().strftime('%Y%m%d'))

    exec_sync(start_date, end_date)


if __name__ == '__main__':
    sync(False)
