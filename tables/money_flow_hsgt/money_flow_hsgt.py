"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 11:05
# @Author  : PcLiu
# @FileName: money_flow_hsgt.py
===========================

沪深股票-行情数据-沪深港通资金流向
接口：moneyflow_hsgt，可以通过数据工具调试和查看数据。
描述：获取沪股通、深股通、港股通每日资金流向数据，每次最多返回300条记录，总量不限制。每天18~20点之间完成当日更新
积分要求：2000积分起，5000积分每分钟可提取500次
tushare 接口说明： https://tushare.pro/document/2?doc_id=47
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
    exec_syn(trade_date='', start_date=start_date, end_date=end_date, limit=300, interval=0)


# 增量追加表数据
def append():
    now = datetime.datetime.now()
    date = now.strftime('%Y%m%d')
    exec_syn(trade_date=date, start_date=date, end_date=date, limit=300, interval=0)


# trade_date: 交易日期, 空值时匹配所有日期 (增量单日增加参数)
# start_date: 数据开始日期（全量历史初始化参数）
# end_date: 数据结束日期（全量历史初始化参数）
# interval: 每次拉取的时间间隔
def exec_syn(trade_date, start_date, end_date, limit, interval):
    ts_api = get_tushare_api()
    connection = get_mock_connection()
    logger = get_logger('money_flow_hsgt', 'data_syn.log')

    offset = 0
    while True:
        logger.info("Query monthly from tushare with api[moneyflow_hsgt] trade_date[%s] start_date[%s] end_date[%s] "
                    "from offset[%d] limit[%d]" % (trade_date, start_date, end_date, offset, limit))
        data = ts_api.moneyflow_hsgt(**{
            "trade_date": trade_date,
            "start_date": start_date,
            "end_date": end_date,
            "limit": limit,
            "offset": offset
        }, fields=[
            "trade_date",
            "ggt_ss",
            "ggt_sz",
            "hgt",
            "sgt",
            "north_money",
            "south_money"
        ])
        logger.info('Write [%d] records into table [money_flow_hsgt] with [%s]' % (data.last_valid_index()+1, connection.engine))
        data.to_sql('money_flow_hsgt', connection, index=False, if_exists='append', chunksize=5000)

        size = data.last_valid_index()+1
        offset = offset + size
        if size < limit:
            break
        else:
            time.sleep(interval)


if __name__ == '__main__':
    init()


