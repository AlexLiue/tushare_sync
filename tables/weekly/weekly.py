"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 07:13
# @Author  : PcLiu
# @FileName: weekly.py
===========================

沪深股票-行情数据-A股周线行情
接口：weekly
描述：获取A股周线行情
限量：单次最大4500行，总量不限制
tushare 接口说明：https://tushare.pro/document/2?doc_id=144
"""

import os
import time
import datetime
from utils.utils import exec_mysql_script, get_tushare_api, get_mock_connection, get_logger


# 全量初始化表数据
def init():
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_mysql_script(dir_path)

    start_date = '19700101'
    now = datetime.datetime.now()
    end_date = now.strftime('%Y%m%d')

    exec_syn(trade_date='', start_date=start_date, end_date=end_date, limit=4500, interval=2)


# 增量追加表数据
def append():
    now = datetime.datetime.now()
    date = now.strftime('%Y%m%d')
    exec_syn(trade_date=date, start_date='', end_date='', limit=5000, interval=2)


# trade_date: 交易日期, 空值时匹配所有日期 (增量单日增加参数)
# start_date: 数据开始日期（全量历史初始化参数）
# end_date: 数据结束日期（全量历史初始化参数）
# limit: 单次拉起记录数限制
# interval: 每次拉取的时间间隔
def exec_syn(trade_date, start_date, end_date, limit, interval):
    ts_api = get_tushare_api()
    connection = get_mock_connection()
    logger = get_logger('weekly', 'data_syn.log')
    offset = 0
    while True:
        logger.info("Query weekly from tushare with api[weekly] trade_date[%s] start_date[%s] end_date[%s] "
                    "from offset[%d] limit[%d]" % (trade_date, start_date, end_date, offset, limit))

        data = ts_api.weekly(**{
            "ts_code": "",
            "trade_date": trade_date,
            "start_date": start_date,
            "end_date": end_date,
            "offset": offset,
            "limit": limit
        }, fields=[
            "ts_code",
            "trade_date",
            "close",
            "open",
            "high",
            "low",
            "pre_close",
            "change",
            "pct_chg",
            "vol",
            "amount"
        ])
        logger.info('Write [%d] records into table [weekly] with [%s]' % (data.last_valid_index()+1, connection.engine))
        data.to_sql('weekly', connection, index=False, if_exists='append', chunksize=5000)

        size = data.last_valid_index()+1
        offset = offset + size
        if size < limit:
            break
        else:
            time.sleep(interval)


if __name__ == '__main__':
    init()
