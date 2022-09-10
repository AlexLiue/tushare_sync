"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 12:04
# @Author  : PcLiu
# @FileName: hsgt_top10.py
===========================

沪深股票-行情数据-沪深股通十大成交股
接口：hsgt_top10
描述：获取沪股通、深股通每日前十大成交详细数据，每天18~20点之间完成当日更新
tushare 接口说明：https://tushare.pro/document/2?doc_id=48
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
    exec_syn(trade_date='', start_date=start_date, end_date=end_date, limit=5000, interval=0)


# 增量追加表数据
def append():
    now = datetime.datetime.now()
    date = now.strftime('%Y%m%d')
    exec_syn(trade_date=date, start_date=date, end_date=date, limit=5000, interval=0)


# trade_date: 交易日期, 空值时匹配所有日期 (增量单日增加参数)
# start_date: 数据开始日期（全量历史初始化参数）
# end_date: 数据结束日期（全量历史初始化参数）
# limit: 每次拉取的记录数
# interval: 每次拉取的时间间隔
def exec_syn(trade_date, start_date, end_date, limit, interval):
    ts_api = get_tushare_api()
    connection = get_mock_connection()
    logger = get_logger('hsgt_top10', 'data_syn.log')

    offset = 0
    while True:
        logger.info("Query monthly from tushare with api[hsgt_top10] trade_date[%s] start_date[%s] end_date[%s] "
                    "from offset[%d] limit[%d]" % (trade_date, start_date, end_date, offset, limit))
        data = ts_api.hsgt_top10(**{
            "ts_code": "",
            "trade_date": trade_date,
            "start_date": start_date,
            "end_date": end_date,
            "market_type": "",
            "limit": limit,
            "offset": offset
        }, fields=[
            "trade_date",
            "ts_code",
            "name",
            "close",
            "change",
            "rank",
            "market_type",
            "amount",
            "net_amount",
            "buy",
            "sell"
        ])
        logger.info('Write [%d] records into table [hsgt_top10] with [%s]' % (data.iloc[:, 0].size, connection.engine))
        data.to_sql('hsgt_top10', connection, index=False, if_exists='append', chunksize=5000)

        size = data.iloc[:, 0].size
        offset = offset + size
        if size < limit:
            break
        else:
            time.sleep(interval)


if __name__ == '__main__':
    append()

