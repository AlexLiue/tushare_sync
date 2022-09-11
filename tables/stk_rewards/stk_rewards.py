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
from utils.utils import exec_mysql_script, get_tushare_api, get_mock_connection, get_logger


# 全量初始化表数据
# 首先从 stock_basic 接口中查询 ts_code , 每次查询 1000 条
# 然后从 stk_rewards 接口中查询管理层薪酬和持股, 每次查询 4000 条
def init():
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_mysql_script(dir_path)

    ts_api = get_tushare_api()
    connection = get_mock_connection()
    logger = get_logger('stk_rewards', 'data_syn.log')

    limit1 = 1000  # 每次读取 1000 行
    offset1 = 0  # 读取偏移量
    while True:
        logger.info("Query ts_code from tushare with api[stock_basic] from offset1[%d] limit1[%d]" % (offset1, limit1))
        df_ts_code = ts_api.stock_basic(**{
            "limit": limit1,
            "offset": offset1
        }, fields=[
            "ts_code"
        ])

        ts_code = df_ts_code['ts_code'].str.cat(sep=',')
        limit2 = 4000
        offset2 = 0
        while True:
            logger.info("Query stk_rewards from tushare with api[stk_rewards] from offset1[%d] limit1[%d] offset2[%d] "
                        "limit2[%d]" % (offset1, limit1, offset2, limit2))
            data = ts_api.stk_rewards(**{
                "ts_code": ts_code,
                "limit": limit2,
                "offset": offset2
            }, fields=[
                "ts_code",
                "ann_date",
                "end_date",
                "name",
                "title",
                "reward",
                "hold_vol"
            ])
            logger.info('Write [%d] records into table [stk_rewards] with [%s]' %
                         (data.last_valid_index()+1, connection.engine))
            data.to_sql('stk_rewards', connection, index=False, if_exists='append', chunksize=5000)
            size2 = data.last_valid_index()+1
            offset2 = offset2 + size2
            if size2 < limit2:
                break
        size = df_ts_code.last_valid_index()+1
        offset1 = offset1 + size
        if size < limit1:
            break


# 增量追加表数据, 股票列表不具备增量条件, 全量覆盖
def append():
    init()


if __name__ == '__main__':
    init()
