"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 10:31
# @Author  : PcLiu
# @FileName: stk_limit.py
===========================

沪深股票-行情数据-每日涨跌停价格
接口：stk_limit
描述：获取全市场（包含A/B股和基金）每日涨跌停价格，包括涨停价格，跌停价格等，每个交易日8点40左右更新当日股票涨跌停价格。
限量：单次最多提取5800条记录，可循环调取，总量不限制
积分：用户积600积分可调取，单位分钟有流控，积分越高流量越大，请自行提高积分，具体请参阅积分获取办法
tushare 接口说明： https://tushare.pro/document/2?doc_id=183
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
# interval: 每次拉取的时间间隔
def exec_syn(trade_date, start_date, end_date, limit, interval):
    ts_api = get_tushare_api()
    connection = get_mock_connection()
    logger = get_logger('stk_limit', 'data_syn.log')

    offset = 0
    while True:
        logger.info("Query monthly from tushare with api[stk_limit] trade_date[%s] start_date[%s] end_date[%s] "
                    "from offset[%d] limit[%d]" % (trade_date, start_date, end_date, offset, limit))
        data = ts_api.stk_limit(**{
            "ts_code": "",
            "trade_date": trade_date,
            "start_date": start_date,
            "end_date": end_date,
            "offset": offset,
            "limit": limit
        }, fields=[
            "trade_date",
            "ts_code",
            "up_limit",
            "down_limit",
            "pre_close"
        ])
        logger.info('Write [%d] records into table [stk_limit] with [%s]' % (data.last_valid_index()+1, connection.engine))
        data.to_sql('stk_limit', connection, index=False, if_exists='append', chunksize=5000)

        size = data.last_valid_index()+1
        offset = offset + size
        if size < limit:
            break
        else:
            time.sleep(interval)


if __name__ == '__main__':
    append()

