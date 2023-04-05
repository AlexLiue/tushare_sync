"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 08:18
# @Author  : PcLiu
# @FileName: money_flow.py
===========================

接口：money_flow，可以通过数据工具调试和查看数据。
描述：获取沪深A股票资金流向数据，分析大单小单成交情况，用于判别资金动向
限量：单次最大提取5000行记录，总量不限制
积分：用户需要至少2000积分才可以调取，基础积分有流量控制，积分越多权限越大，请自行提高积分，具体请参阅积分获取办法
tushare 接口说明：https://tushare.pro/document/2?doc_id=170
"""

import os
import datetime
from utils.utils import exec_create_table_script, exec_sync_with_spec_date_column


# 全量初始化表数据
def init(drop_exist):
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, drop_exist)

    exec_sync_with_spec_date_column(
        table_name='money_flow',
        api_name='moneyflow',
        fields=[
            "ts_code",
            "trade_date",
            "buy_sm_vol",
            "buy_sm_amount",
            "sell_sm_vol",
            "sell_sm_amount",
            "buy_md_vol",
            "buy_md_amount",
            "sell_md_vol",
            "sell_md_amount",
            "buy_lg_vol",
            "buy_lg_amount",
            "sell_lg_vol",
            "sell_lg_amount",
            "buy_elg_vol",
            "buy_elg_amount",
            "sell_elg_vol",
            "sell_elg_amount",
            "net_mf_vol",
            "net_mf_amount",
            "trade_count"
        ],
        date_column='trade_date',
        start_date='19901219',
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=1,
        limit=5000,
        interval=0.3
    )


# 增量追加表数据
def append():
    exec_sync_with_spec_date_column(
        table_name='money_flow',
        api_name='moneyflow',
        fields=[
            "ts_code",
            "trade_date",
            "buy_sm_vol",
            "buy_sm_amount",
            "sell_sm_vol",
            "sell_sm_amount",
            "buy_md_vol",
            "buy_md_amount",
            "sell_md_vol",
            "sell_md_amount",
            "buy_lg_vol",
            "buy_lg_amount",
            "sell_lg_vol",
            "sell_lg_amount",
            "buy_elg_vol",
            "buy_elg_amount",
            "sell_elg_vol",
            "sell_elg_amount",
            "net_mf_vol",
            "net_mf_amount",
            "trade_count"
        ],
        date_column='trade_date',
        start_date=str((datetime.datetime.now() + datetime.timedelta(days=-10)).strftime('%Y%m%d')),
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=1,
        limit=5000,
        interval=0.3
    )


if __name__ == '__main__':
    append()
