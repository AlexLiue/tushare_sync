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
from utils.utils import exec_create_table_script, get_tushare_api, get_mock_connection, get_logger, query_last_syn_date, \
    max_date

limit = 5000  # 每次读取记录条数
interval = 31  # 读取的时间间隔, Tushare 限制每分钟 2次 API 调用
begin_date = '20160101'  # Tushare 里数据最早开始时间


def exec_syn(start_date, end_date):
    # Extern Global Var
    global limit
    global interval

    ts_api = get_tushare_api()
    connection = get_mock_connection()
    logger = get_logger('bak_basic', 'data_syn.log')
    logger.info("Sync ts_code start_date[%s] end_date[%s]" % (start_date, end_date))

    clen_sql = "delete from bak_basic where trade_date>='%s' and trade_date<='%s'" % (start_date, end_date)
    logger.info('Execute Clean SQL [%s]' % clen_sql)

    start = datetime.datetime.strptime(start_date, '%Y%m%d')
    end = datetime.datetime.strptime(end_date, '%Y%m%d')
    syn_date = start  # 同步日期
    while syn_date < end:
        offset = 0
        trade_date = str(syn_date.strftime('%Y%m%d'))
        while True:
            logger.info(
                "Query bak_basic from tushare with api[bak_basic] trade_date[%s] from offset[%d] limit[%d]"
                % (trade_date, offset, limit))
            data = ts_api.bak_basic(**{
                "trade_date": trade_date,
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
            time.sleep(interval)
            if data.last_valid_index() is not None:
                size = data.last_valid_index() + 1
                logger.info('Write [%d] records into table [bak_basic] with [%s]' % (size, connection.engine))
                data.to_sql('bak_basic', connection, index=False, if_exists='append', chunksize=limit)
                offset = offset + size
                if size < limit:
                    break
            else:
                break
        syn_date = syn_date + datetime.timedelta(days=1)


# 全量初始化表数据
# 首先从 bak_basic 接口中查询, 权限限制每30秒查询一次, 一次查询 5000 条
def init(drop_exist):
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, drop_exist)

    global begin_date
    now = datetime.datetime.now()
    end_date = str(now.strftime('%Y%m%d'))

    # 查询历史最大同步日期
    date_query_sql = "select max(cal_date) date from tushare.bak_basic"
    last_date = query_last_syn_date(date_query_sql)
    start_date = max_date(last_date, begin_date)
    exec_syn(start_date, end_date)


# 增量追加表数据
def append():
    now = datetime.datetime.now()
    end_date = str(now.strftime('%Y%m%d'))

    date_query_sql = "select max(cal_date) date from tushare.bak_basic"
    start_date = query_last_syn_date(date_query_sql)
    exec_syn(start_date, end_date)

if __name__ == '__main__':
    append()
