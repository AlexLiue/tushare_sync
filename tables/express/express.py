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
from utils.utils import exec_create_table_script, exec_sync_with_spec_date_column, query_last_sync_date, max_date, \
    get_cfg

begin_date = "20040101"
limit = 2000
interval = 2


def exec_sync(start_date, end_date):
    global limit
    global interval
    exec_sync_with_spec_date_column(
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
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        interval=interval)


# 全量初始化表数据
def sync(drop_exist):
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_create_table_script(dir_path, drop_exist)

    # 查询历史最大同步日期
    global begin_date
    cfg = get_cfg()
    date_query_sql = "select max(ann_date) date from %s.express" % cfg['mysql']['database']
    last_date = query_last_sync_date(date_query_sql)
    start_date = max_date(last_date, begin_date)
    end_date = str(datetime.datetime.now().strftime('%Y%m%d'))

    exec_sync(start_date, end_date)


if __name__ == '__main__':
    sync(True)
