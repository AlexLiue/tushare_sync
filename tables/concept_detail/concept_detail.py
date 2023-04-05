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
import datetime
import os
from utils.utils import exec_create_table_script, exec_sync_with_ts_code



# 全量初始化表数据
def sync(drop_exist=True):
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, True)

    limit = 1000
    interval = 1
    exec_sync_with_ts_code(
        table_name='stk_rewards',
        api_name='stk_rewards',
        fields=[
            "id",
            "concept_name",
            "ts_code",
            "name",
            "in_date",
            "out_date"
        ],
        date_column='end_date',
        start_date=19970101,
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=36000,
        limit=limit,
        interval=interval,
        ts_code_limit=1)


if __name__ == '__main__':
    sync()
