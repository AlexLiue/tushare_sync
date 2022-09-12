"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2022/9/10 06:40
# @Author  : PcLiu
# @FileName: express.py
===========================

沪深股票-财务数据-业绩预告
接口：express，可以通过数据工具调试和查看数据。 每次 3500 条
描述：获取上市公司业绩快报
权限：用户需要至少800积分才可以调取，具体请参阅积分获取办法

提示：当前接口只能按单只股票获取其历史数据，如果需要获取某一季度全部上市公司数据，请使用express_vip接口（参数一致），需积攒5000积分。
tushare 接口说明：https://tushare.pro/document/2?doc_id=46
"""

import os
import datetime
from utils.utils import exec_mysql_script, exec_sync

# 全量初始化表数据
def init():
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_mysql_script(dir_path)

    exec_sync(
        table_name='express',
        api_name='express',
        fields=[
            "ts_code",
            "ann_date",
            "end_date",
            "revenue",
            "operate_profit",
            "total_profit",
            "n_income",
            "total_assets",
            "total_hldr_eqy_exc_min_int",
            "diluted_eps",
            "diluted_roe",
            "yoy_net_profit",
            "bps",
            "perf_summary",
            "is_audit",
            "remark",
            "open_bps",
            "open_net_assets",
            "eps_last_year",
            "np_last_year",
            "tp_last_year",
            "op_last_year",
            "or_last_year",
            "growth_bps",
            "yoy_equity",
            "growth_assets",
            "yoy_roe",
            "yoy_eps",
            "yoy_dedu_np",
            "yoy_tp",
            "yoy_op",
            "yoy_sales"
        ],
        date_column='ann_date',
        start_date='20040101',
        end_date = str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=365,
        limit=2000,
        interval=2
    )


# 增量追加表数据
def append():
    exec_sync(
        table_name='express',
        api_name='express',
        fields=[
            "ts_code",
            "ann_date",
            "end_date",
            "revenue",
            "operate_profit",
            "total_profit",
            "n_income",
            "total_assets",
            "total_hldr_eqy_exc_min_int",
            "diluted_eps",
            "diluted_roe",
            "yoy_net_profit",
            "bps",
            "perf_summary",
            "is_audit",
            "remark",
            "open_bps",
            "open_net_assets",
            "eps_last_year",
            "np_last_year",
            "tp_last_year",
            "op_last_year",
            "or_last_year",
            "growth_bps",
            "yoy_equity",
            "growth_assets",
            "yoy_roe",
            "yoy_eps",
            "yoy_dedu_np",
            "yoy_tp",
            "yoy_op",
            "yoy_sales"
        ],
        date_column='ann_date',
        start_date=str((datetime.datetime.now() + datetime.timedelta(days=-180)).strftime('%Y%m%d')),
        end_date = str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=365,
        limit=2000,
        interval=2
    )


if __name__ == '__main__':
    append()
