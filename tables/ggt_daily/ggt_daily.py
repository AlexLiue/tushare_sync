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
    exec_syn(trade_date='', start_date=start_date, end_date=end_date, limit=1000, interval=30)


# 增量追加表数据
def append():
    now = datetime.datetime.now()
    date = now.strftime('%Y%m%d')
    exec_syn(trade_date=date, start_date=date, end_date=date, limit=1000, interval=30)


# trade_date: 交易日期, 空值时匹配所有日期 (增量单日增加参数)
# start_date: 数据开始日期（全量历史初始化参数）
# end_date: 数据结束日期（全量历史初始化参数）
# limit: 每次拉取的记录数
# interval: 每次拉取的时间间隔
def exec_syn(trade_date, start_date, end_date, limit, interval):
    ts_api = get_tushare_api()
    connection = get_mock_connection()
    logger = get_logger('ggt_daily', 'data_syn.log')

    offset = 0
    while True:
        logger.info("Query monthly from tushare with api[ggt_daily] trade_date[%s] start_date[%s] end_date[%s] "
                    "from offset[%d] limit[%d]" % (trade_date, start_date, end_date, offset, limit))
        data = ts_api.ggt_daily(**{
            "trade_date": trade_date,
            "start_date": start_date,
            "end_date": end_date,
            "limit": limit,
            "offset": offset
        }, fields=[
            "trade_date",
            "buy_amount",
            "buy_volume",
            "sell_amount",
            "sell_volume"
        ])
        logger.info('Write [%d] records into table [ggt_daily] with [%s]' % (data.iloc[:, 0].size, connection.engine))
        data.to_sql('ggt_daily', connection, index=False, if_exists='append', chunksize=5000)

        size = data.iloc[:, 0].size
        offset = offset + size
        if size < limit:
            break
        else:
            time.sleep(interval)


if __name__ == '__main__':
    append()

