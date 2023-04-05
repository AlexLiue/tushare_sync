"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/9 21:33
# @Author  : PcLiu
# @FileName: t.py
===========================

沪深股票-基础信息-股票曾用名
接口：name_change
描述：历史名称变更记录
tushare 接口说明： https://tushare.pro/document/2?doc_id=100
"""

import os

from utils.utils import exec_create_table_script, get_tushare_api, get_mock_connection, get_logger


# 全量初始化表数据
def sync(drop_exist):
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, drop_exist)

    ts_api = get_tushare_api()
    connection = get_mock_connection()
    logger = get_logger('name_change', 'data_syn.log')

    fields = 'ts_code,name,start_date,end_date,ann_date,change_reason'
    logger.info("Query data from tushare with api[namechange], fields[%s]" % fields)

    data = ts_api.namechange(ts_code='', fields=fields)

    logger.info(
        'Write [%d] records into table [stock_basic] with [%s]' % (data.last_valid_index() + 1, connection.engine))
    data.to_sql('name_change', connection, index=False, if_exists='append', chunksize=5000)


if __name__ == '__main__':
    sync(True)
