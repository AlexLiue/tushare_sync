"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 07:24
# @Author  : PcLiu
# @FileName: concept_detail.py
===========================
沪深股票-市场参考数据-概念股列表 （已经停止维护）
接口：concept_detail
描述：获取概念股分类明细数据
积分：用户需要至少300积分才可以调取，具体请参阅积分获取办法
注意：本接口数据以停止更新，请转移到同花顺概念接口

已停止维护，仅进行初始化，最后维护时间2021年2月
"""

import os
import time

from utils.utils import exec_create_table_script, get_tushare_api, get_mock_connection, get_logger


# 全量初始化表数据
def init(drop_exist):
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, drop_exist)

    # 创建 API / Connection / Logger 对象
    ts_api = get_tushare_api()
    connection = get_mock_connection()
    logger = get_logger('concept_detail', 'data_syn.log')

    limit = 1000
    offset = 0
    interval = 0.2
    while True:
        logger.info(
            "Query concept_detail from tushare with api[concept_detail] from offset[%d] limit[%d]" % (offset, limit))
        data_tmp = ts_api.concept_detail(**{
            "src": "",
            "limit": "",
            "offset": ""
        }, fields=[
            "id",
            "concept_name",
            "ts_code",
            "name",
            "in_date",
            "out_date"
        ])
        data = data_tmp.rename(columns={'id': 'code'})
        time.sleep(interval)
        if data.last_valid_index() is not None:
            size = data.last_valid_index() + 1
            logger.info('Write [%d] records into table [concept_detail] with [%s]' % (size, connection.engine))
            data.to_sql('concept_detail', connection, index=False, if_exists='append', chunksize=limit)
            offset = offset + size
            if size < limit:
                break
        else:
            break


if __name__ == '__main__':
    init()
