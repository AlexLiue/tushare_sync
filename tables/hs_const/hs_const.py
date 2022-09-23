"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/9 22:23
# @Author  : PcLiu
# @FileName: hs_const.py
===========================

沪深股票-基础信息-沪深股通成份股
接口：hs_const
描述：获取沪股通、深股通成分数据
tushare 接口说明： https://tushare.pro/document/2?doc_id=104
"""

import os
from utils.utils import exec_mysql_script, get_tushare_api, get_mock_connection, get_logger


# 全量初始化表数据
def init():
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_mysql_script(dir_path)

    ts_api = get_tushare_api()
    connection = get_mock_connection()
    logger = get_logger('hs_const', 'data_syn.log')

    fields = 'ts_code,hs_type,in_date,out_date,is_new'
    logger.info("Query data from tushare with api[hs_const], fields[%s]" % fields)

    data = ts_api.hs_const(hs_type='SZ', is_new='0', fields=fields)
    logger.info('Write [%d] records into table [stock_basic] with [%s], where condition[hs_type=SZ, is_new=0]'
                % (data.last_valid_index() + 1, connection.engine))
    data.to_sql('hs_const', connection, index=False, if_exists='append', chunksize=5000)

    data = ts_api.hs_const(hs_type='SZ', is_new='1', fields=fields)
    logger.info('Write [%d] records into table [stock_basic] with [%s], where condition[hs_type=SZ, is_new=1]'
                % (data.last_valid_index() + 1, connection.engine))
    data.to_sql('hs_const', connection, index=False, if_exists='append', chunksize=5000)

    data = ts_api.hs_const(hs_type='SH', is_new='0', fields=fields)
    logger.info('Write [%d] records into table [stock_basic] with [%s], where condition[hs_type=SH, is_new=0]'
                % (data.last_valid_index() + 1, connection.engine))
    data.to_sql('hs_const', connection, index=False, if_exists='append', chunksize=5000)

    data = ts_api.hs_const(hs_type='SH', is_new='1', fields=fields)
    logger.info('Write [%d] records into table [stock_basic] with [%s], where condition[hs_type=SH, is_new=1]'
                % (data.last_valid_index() + 1, connection.engine))
    data.to_sql('hs_const', connection, index=False, if_exists='append', chunksize=5000)


# 增量追加表数据, 股票列表不具备增量条件, 全量覆盖
def append():
    init()


if __name__ == '__main__':
    init()
