"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 06:40
# @Author  : PcLiu
# @FileName: daily.py
===========================

沪深股票-行情数据-A股日线行情
接口：daily，可以通过数据工具调试和查看数据
数据说明：交易日每天15点～16点之间入库。本接口是未复权行情，停牌期间不提供数据
调取说明：120积分每分钟内最多调取500次，每次5000条数据，相当于单次提取23年历史
描述：获取股票行情数据，或通过通用行情接口获取数据，包含了前后复权数据
tushare 接口说明：https://tushare.pro/document/2?doc_id=27
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


# trade_date: 交易日期, 空值时匹配所有日期 (增量单日增加参数)
# start_date: 数据开始日期（全量历史初始化参数）
# end_date: 数据结束日期（全量历史初始化参数）
# limit: 单次拉起记录数限制
# interval: 每次拉取的时间间隔
def exec_syn(trade_date, start_date, end_date, limit, interval):
    ts_api = get_tushare_api()
    connection = get_mock_connection()
    logger = get_logger('daily', 'data_syn.log')
    offset = 0
    while True:
        logger.info("Query daily from tushare with api[daily] trade_date[%s] start_date[%s] end_date[%s] "
                    "from offset[%d] limit[%d]" % (trade_date, start_date, end_date, offset, limit))

        data = ts_api.daily(**{
            "ts_code": "",
            "trade_date": trade_date,
            "start_date": start_date,
            "end_date": end_date,
            "offset": offset,
            "limit": limit
        }, fields=[
            "ts_code",
            "trade_date",
            "open",
            "high",
            "low",
            "close",
            "pre_close",
            "change",
            "pct_chg",
            "vol",
            "amount"
        ])
        logger.info('Write [%d] records into table [daily] with [%s]' % (data.iloc[:, 0].size, connection.engine))
        data.to_sql('daily', connection, index=False, if_exists='append', chunksize=5000)

        size = data.iloc[:, 0].size
        offset = offset + size
        if size < limit:
            break
        else:
            time.sleep(interval)


# 增量追加表数据
def append():
    now = datetime.datetime.now()
    date = now.strftime('%Y%m%d')
    exec_syn(trade_date=date, start_date='', end_date='', limit=5000, interval=0)


if __name__ == '__main__':
    append()
