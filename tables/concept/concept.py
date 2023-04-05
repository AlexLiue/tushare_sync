"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 07:24
# @Author  : PcLiu
# @FileName: concept.py
===========================

接口：concept
描述：获取概念股分类，目前只有ts一个来源，未来将逐步增加来源
积分：用户需要至少300积分才可以调取，具体请参阅积分获取办法
注意：本接口数据以停止更新，请转移到同花顺概念接口
tushare 接口说明：https://tushare.pro/document/2?doc_id=125
已停止维护，仅进行初始化，最后维护时间2021年2月
"""

import os
from utils.utils import exec_create_table_script, get_tushare_api, get_mock_connection, get_logger


# 全量初始化表数据
def sync(drop_exist=True):
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, True)

    # 创建 API / Connection / Logger 对象
    ts_api = get_tushare_api()
    connection = get_mock_connection()
    logger = get_logger('concept', 'data_syn.log')

    # 拉取数据
    data = ts_api.concept(**{
        "src": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "code",
        "name",
        "src"
    ])
    size = data.last_valid_index() + 1
    logger.info('Write [%d] records into table [%s] with [%s]' % (size, 'concept', connection.engine))
    data.to_sql('concept', connection, index=False, if_exists='append', chunksize=5000)


if __name__ == '__main__':
    sync(False)
