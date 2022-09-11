"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 14:14
# @Author  : PcLiu
# @FileName: bak_daily.py
===========================

沪深股票-行情数据-备用行情
接口：bak_daily
描述：获取备用行情，包括特定的行情指标
限量：单次最大5000行数据，可以根据日期参数循环获取，正式权限需要5000积分。 2000积分（每分钟最多访问该接口5次）
tushare 接口说明：https://tushare.pro/document/2?doc_id=255
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
    exec_syn(trade_date='', start_date=start_date, end_date=end_date, limit=5000, interval=12)


# 增量追加表数据
def append():
    now = datetime.datetime.now()
    date = now.strftime('%Y%m%d')
    exec_syn(trade_date=date, start_date=date, end_date=date, limit=5000, interval=12)


# trade_date: 交易日期, 空值时匹配所有日期 (增量单日增加参数)
# start_date: 数据开始日期（全量历史初始化参数）
# end_date: 数据结束日期（全量历史初始化参数）
# limit: 每次拉取的记录数
# interval: 每次拉取的时间间隔
def exec_syn(trade_date, start_date, end_date, limit, interval):
    ts_api = get_tushare_api()
    connection = get_mock_connection()
    logger = get_logger('bak_daily', 'data_syn.log')

    offset = 0
    while True:
        logger.info("Query monthly from tushare with api[bak_daily] trade_date[%s] start_date[%s] end_date[%s] "
                    "from offset[%d] limit[%d]" % (trade_date, start_date, end_date, offset, limit))
        data = ts_api.bak_daily(**{
            "ts_code": "",
            "trade_date": trade_date,
            "start_date": start_date,
            "end_date": end_date,
            "offset": interval,
            "limit": limit
        }, fields=[
            "ts_code",
            "trade_date",
            "name",
            "pct_change",
            "close",
            "change",
            "open",
            "high",
            "low",
            "pre_close",
            "vol_ratio",
            "turn_over",
            "swing",
            "vol",
            "amount",
            "selling",
            "buying",
            "total_share",
            "float_share",
            "pe",
            "industry",
            "area",
            "float_mv",
            "total_mv",
            "avg_price",
            "strength",
            "activity",
            "avg_turnover",
            "attack",
            "interval_3",
            "interval_6"
        ])
        logger.info('Write [%d] records into table [bak_daily] with [%s]' % (data.last_valid_index()+1, connection.engine))
        data.to_sql('bak_daily', connection, index=False, if_exists='append', chunksize=5000)

        size = data.last_valid_index()+1
        offset = offset + size
        if size < limit:
            break
        else:
            time.sleep(interval)


if __name__ == '__main__':
    append()

