
"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/9 21:33
# @Author  : PcLiu
# @FileName: t.py
===========================

沪深股票-基础信息-交易日历
接口：trade_cal，可以通过数据工具调试和查看数据。
描述：获取各大交易所交易日历数据,默认提取的是上交所
tushare 接口说明： https://tushare.pro/document/2?doc_id=26
"""

import datetime
import os

from utils.utils import exec_mysql_script, get_tushare_api, get_mock_connection, get_logger


def init():
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_mysql_script(dir_path)

    start = 19700101
    now = datetime.datetime.now()
    end = now.strftime('%Y%m%d')
    sync(start, end, 'append')


def append():
    now = datetime.datetime.now()
    start = now.strftime('%Y%m%d')
    end = start
    sync(start, end, 'append')


# 数据同步,  start-数据开始日期, end-数据结束日期
def sync(start, end, if_exists):
    ts_api = get_tushare_api()
    connection = get_mock_connection()
    logger = get_logger('trade_cal', 'data_syn.log')

    api_name = 'trade_cal'
    fields = 'exchange,cal_date,is_open,pretrade_date'

    logger.info("Query data from tushare with api[%s], start[%s]- end[%s], fields[%s]" % (api_name, start, end, fields))
    data = ts_api.query(api_name, fields, start_date=start, end_date=end)

    logger.info('Write [%d] records into table [trade_cal] with [%s]' % (data.iloc[:, 0].size, connection.engine))
    data.to_sql('trade_cal', connection, index=False, if_exists=if_exists, chunksize=5000)
