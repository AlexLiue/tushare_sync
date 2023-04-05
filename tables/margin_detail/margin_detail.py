"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 07:24
# @Author  : PcLiu
# @FileName: margin_detail.py
===========================

 沪深股票-市场参考数据-融资融券交易明细
接口：margin_detail
描述：获取沪深两市每日融资融券明细
tushare 接口说明：https://tushare.pro/document/2?doc_id=59

本报表基于证券公司报送的融资融券余额数据汇总生成，其中：
本日融资余额(元)=前日融资余额＋本日融资买入-本日融资偿还额
本日融券余量(股)=前日融券余量＋本日融券卖出量-本日融券买入量-本日现券偿还量
本日融券余额(元)=本日融券余量×本日收盘价
本日融资融券余额(元)=本日融资余额＋本日融券余额

单位说明：股（标的证券为股票）、份（标的证券为基金）、手（标的证券为债券）。

2014年9月22日起，“融资融券交易总量”数据包含调出标的证券名单的证券的融资融券余额。

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
        table_name='margin_detail',
        api_name='margin_detail',
        fields=[
            "trade_date",
            "ts_code",
            "rzye",
            "rqye",
            "rzmre",
            "rqyl",
            "rzche",
            "rqchl",
            "rqmcl",
            "rzrqye",
            "name"
        ],
        date_column='trade_date',
        start_date='20100101',
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=31,
        limit=3000,
        interval=0.2
    )


# 增量追加表数据
def append():
    exec_sync_with_spec_date_column(
        table_name='margin_detail',
        api_name='margin_detail',
        fields=[
            "trade_date",
            "ts_code",
            "rzye",
            "rqye",
            "rzmre",
            "rqyl",
            "rzche",
            "rqchl",
            "rqmcl",
            "rzrqye",
            "name"
        ],
        date_column='trade_date',
        start_date=str((datetime.datetime.now() + datetime.timedelta(days=-31)).strftime('%Y%m%d')),
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=1,
        limit=3000,
        interval=0.2
    )


if __name__ == '__main__':
    init()
