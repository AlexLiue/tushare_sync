"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 05:51
# @Author  : PcLiu
# @FileName: bak_basic.py
===========================

沪深股票-基础信息-备用列表 (数据量较大, 2000积分每分钟只能调用2次,独立处理)
接口：hs_const
描述：获取沪股通、深股通成分数据
tushare 接口说明： https://tushare.pro/document/2?doc_id=262
"""

import os
import time
import datetime
from utils.utils import exec_mysql_script, get_tushare_api, get_mock_connection, get_logger


# 全量初始化表数据
# 首先从 bak_basic 接口中查询, 权限限制每30秒查询一次, 一次查询 5000 条
def init():
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_mysql_script(dir_path)
    exec_syn(trade_date='', limit=5000, interval=35)


# trade_date: 交易日期, 空值时匹配所有日期
# limit: 单次拉起记录数限制
# interval: 每次拉取的时间间隔
def exec_syn(trade_date, limit, interval):
    ts_api = get_tushare_api()
    connection = get_mock_connection()
    logger = get_logger('bak_basic', 'data_syn.log')
    offset = 0
    while True:
        logger.info("Query bak_basic from tushare with api[bak_basic] trade_date[%s] from offset[%d] limit[%d]" %
                    (trade_date, offset, limit))
        data = ts_api.bak_basic(**{
            "trade_date": trade_date,
            "ts_code": "",
            "limit": limit,
            "offset": offset
        }, fields=[
            "trade_date",
            "ts_code",
            "name",
            "industry",
            "area",
            "pe",
            "float_share",
            "total_share",
            "total_assets",
            "liquid_assets",
            "fixed_assets",
            "reserved",
            "reserved_pershare",
            "eps",
            "bvps",
            "pb",
            "list_date",
            "undp",
            "per_undp",
            "rev_yoy",
            "profit_yoy",
            "gpr",
            "npr",
            "holder_num"
        ])

        data.loc[data['list_date'] == '0'] = '19700101'  # 数据预处理 日期 0 值替换为 19700101
        logger.info('Write [%d] records into table [bak_basic] with [%s]' %
                    (data.last_valid_index()+1, connection.engine))
        data.to_sql('bak_basic', connection, index=False, if_exists='append', chunksize=5000)

        size = data.last_valid_index()+1
        offset = offset + size
        if size < limit:
            break
        else:
            time.sleep(interval)


# 增量追加表数据
def append():
    now = datetime.datetime.now()
    date = now.strftime('%Y%m%d')
    exec_syn(date, limit=5000, interval=35)


if __name__ == '__main__':
    append()
