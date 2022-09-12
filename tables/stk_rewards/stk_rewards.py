"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/9 22:50
# @Author  : PcLiu
# @FileName: stk_rewards.py
===========================

沪深股票-基础信息-管理层薪酬和持股（数据量较大,不存在日更新逻辑, 选择性同步）
接口：stk_rewards
描述：获取上市公司管理层薪酬和持股
tushare 接口说明： https://tushare.pro/document/2?doc_id=194
"""

import os
import time
import datetime
from utils.utils import exec_mysql_script, get_tushare_api, get_mock_connection, get_logger, min_date, exec_mysql_sql, \
    exec_sync

ts_code_limit = 1000 # 每次查询多少家股票代码
limit = 5000 # 每次读取记录条数
interval = 0.3 # 读取的时间间隔, Tushare 限制每分钟 200次 API 调用
begin_date = '19940416' # Tushare 里数据最早开始时间
init_date_step = 30 # 微批时间段长度

# 首先从 stock_basic 接口中查询 ts_code , 每次查询 ts_code_limit 条
# 然后从 stk_rewards 接口中查询管理层薪酬和持股, 每次查询 limit 条
def exec_syn(start_date, end_date):
    # Extern Global Var
    global ts_code_limit
    global limit
    global interval

    ts_api = get_tushare_api()
    connection = get_mock_connection()
    logger = get_logger('stk_rewards', 'data_syn.log')
    logger.info("Sync ts_code start_date[%s] end_date[%s]" % (start_date, end_date))

    ts_code_offset = 0  # 读取偏移量
    while True:
        logger.info("Query ts_code from tushare with api[stock_basic] from ts_code_offset[%d] ts_code_limit[%d]"
                    % (ts_code_offset, ts_code_offset))
        df_ts_code = ts_api.stock_basic(**{
            "limit": ts_code_limit,
            "offset": ts_code_offset
        }, fields=[
            "ts_code"
        ])
        time.sleep(interval)
        if df_ts_code.last_valid_index() is not None:
            ts_code = df_ts_code['ts_code'].str.cat(sep=',')
            start = datetime.datetime.strptime(start_date, '%Y%m%d')
            end = datetime.datetime.strptime(end_date, '%Y%m%d')
            syn_date = start  # 微批开始时间
            while syn_date < end:
                offset = 0
                syn_end_date = str(syn_date.strftime('%Y%m%d'))
                while True:
                    logger.info(
                        "Query stk_rewards from tushare with api[stk_rewards] syn_date[%s] from ts_code_offset[%d] ts_code_limit[%d]"
                        " offset[%d] limit[%d]" % (syn_end_date, ts_code_offset, ts_code_limit, offset, limit))
                    data = ts_api.stk_rewards(**{
                        "end_date": syn_end_date,
                        "ts_code": ts_code,
                        "limit": limit,
                        "offset": offset
                    }, fields=[
                        "ts_code",
                        "ann_date",
                        "end_date",
                        "name",
                        "title",
                        "reward",
                        "hold_vol"
                    ])
                    time.sleep(interval)
                    if data.last_valid_index() is not None:
                        size = data.last_valid_index() + 1
                        logger.info('Write [%d] records into table [stk_rewards] with [%s]' % (size, connection.engine))
                        data.to_sql('stk_rewards', connection, index=False, if_exists='append', chunksize=limit)
                        offset = offset + size
                        if size < limit:
                            break
                    else:
                        break
                syn_date = syn_date + datetime.timedelta(days=1)
            ts_code_size = df_ts_code.last_valid_index() + 1
            ts_code_offset = ts_code_offset + ts_code_size
            if ts_code_size < ts_code_limit:
                break
        else:
            break

def init():
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_mysql_script(dir_path)

    global begin_date
    now = datetime.datetime.now()
    end_date = str(now.strftime('%Y%m%d'))

    exec_syn(begin_date, end_date)



# 增量追加表数据, 股票列表不具备增量条件, 先选择无条件覆盖（20天的数据)
def append():
    now = datetime.datetime.now()
    end_date = str(datetime.datetime.now().strftime('%Y%m%d'))
    start_date = str((now + datetime.timedelta(days=-10)).strftime('%Y%m%d'))

    logger = get_logger('stk_rewards', 'data_syn.log')
    clen_sql = "delete from stk_rewards where end_date>='%s' and end_date<='%s'" % (end_date, start_date)
    logger.info('Execute Clean SQL [%s]' % clen_sql)

    exec_mysql_sql(clen_sql)

    exec_syn(start_date, end_date)

if __name__ == '__main__':
    append()
