"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/9 21:33
# @Author  : PcLiu
# @FileName: t.py
===========================

沪深股票-基础信息-股票列表   stock_basic 表
接口：stock_basic，可以通过数据工具调试和查看数据
描述：获取基础信息数据，包括股票代码、名称、上市日期、退市日期等
tushare 接口说明： https://tushare.pro/document/2?doc_id=25
"""

import os

from utils.utils import exec_create_table_script, get_tushare_api, get_mock_connection, get_logger


# 全量初始化表数据
def sync(drop_exist):
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, True)

    ts_api = get_tushare_api()
    connection = get_mock_connection()
    logger = get_logger('stock_basic', 'data_syn.log')

    api_name = 'stock_basic'
    fields = 'ts_code,symbol,name,area,industry,fullname,enname,' \
             'cnspell,market,exchange,curr_type,list_status,list_date,delist_date,is_hs'

    logger.info("Query data from tushare with api[%s], fields[%s]" % (api_name, fields))
    data = ts_api.query(api_name, fields, exchange='', list_status='L')

    logger.info(
        'Write [%d] records into table [stock_basic] with [%s]' % (data.last_valid_index() + 1, connection.engine))
    data.to_sql('stock_basic', connection, index=False, if_exists='append', chunksize=5000)


# 增量追加表数据, 股票列表不具备增量条件, 全量覆盖
if __name__ == '__main__':
    sync(True)
