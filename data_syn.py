"""
数据同步程序入口
要求 Tushare 积分 2000 以上
"""

import argparse

from tables.bak_basic import bak_basic
from tables.bak_daily import bak_daily
from tables.concept import concept
from tables.concept_detail import concept_detail
from tables.cyq_chips import cyq_chips
from tables.cyq_perf import cyq_perf
from tables.daily import daily
from tables.disclosure_date import disclosure_date
from tables.express import express
from tables.fina_indicator import fina_indicator
from tables.fina_mainbz import fina_mainbz
from tables.forecast import forecast
from tables.ggt_daily import ggt_daily
from tables.ggt_top10 import ggt_top10
from tables.hs_const import hs_const
from tables.hsgt_top10 import hsgt_top10
from tables.margin_detail import margin_detail
from tables.money_flow import money_flow
from tables.money_flow_hsgt import money_flow_hsgt
from tables.monthly import monthly
from tables.name_change import name_change
from tables.stk_holder_number import stk_holder_number
from tables.stk_limit import stk_limit
from tables.stk_rewards import stk_rewards
from tables.stock_basic import stock_basic
from tables.top_inst import top_inst
from tables.top_list import top_list
from tables.trade_cal import trade_cal
from tables.weekly import weekly


# 全量历史初始化
def sync(drop_exist):
    stock_basic.sync(drop_exist)  # 沪深股票-基础信息-股票列表
    trade_cal.sync(drop_exist)  # 沪深股票-基础信息-交易日历
    name_change.sync(drop_exist)  # 沪深股票-基础信息-股票曾用名
    hs_const.sync(drop_exist)  # 沪深股票-基础信息-沪深股通成份股
    stk_rewards.sync(drop_exist)  # 沪深股票-基础信息-管理层薪酬和持股
    daily.sync(drop_exist)  # 沪深股票-行情数据-A股日线行情
    weekly.sync(drop_exist)  # 沪深股票-行情数据-A股周线行情
    monthly.sync(drop_exist)  # 沪深股票-行情数据-A股月线行情
    money_flow.sync(drop_exist)  # 沪深股票-行情数据-个股资金流向
    stk_limit.sync(drop_exist)  # 沪深股票-行情数据-每日涨跌停价格
    money_flow_hsgt.sync(drop_exist)  # 沪深股票-行情数据-沪深港通资金流向
    hsgt_top10.sync(drop_exist)  # 沪深股票-行情数据-沪深股通十大成交股
    ggt_top10.sync(drop_exist)  # 沪深股票-行情数据-港股通十大成交股
    ggt_daily.sync(drop_exist)  # 沪深股票-行情数据-港股通每日成交统计
    forecast.sync(drop_exist)  # 沪深股票-财务数据-业绩预告
    express.sync(drop_exist)  # 沪深股票-财务数据-业绩快报
    fina_indicator.sync(drop_exist)  # 沪深股票-财务数据-财务指标数据
    fina_mainbz.sync(drop_exist)  # 沪深股票-财务数据-主营业务构成
    disclosure_date.sync(drop_exist)  # 沪深股票-财务数据-财报披露计划
    margin_detail.sync(drop_exist)  # 沪深股票-市场参考数据-融资融券交易明细
    top_list.sync(drop_exist)  # 沪深股票-市场参考数据-龙虎榜每日明细
    top_inst.sync(drop_exist)  # 沪深股票-市场参考数据-龙虎榜机构明细
    stk_holder_number.sync(drop_exist)  # 沪深股票-市场参考数据-股东人数


def sync_spc(drop_exist):
    bak_basic.sync(drop_exist)  # 沪深股票-基础信息-备用列表 （读取限制,每分钟调用2次, 每天最多访问该接口20次）
    concept.sync(drop_exist)  # 沪深股票-市场参考数据-概念股分类（已经停止维护）
    concept_detail.sync(drop_exist)  # 沪深股票-市场参考数据-概念股列表 （已经停止维护）
    cyq_perf.sync(drop_exist)  # 沪深股票-特色数据-每日筹码及胜率（受限:5/min,10/h)
    cyq_chips.sync(drop_exist)  # 沪深股票-特色数据-每日筹码分布 (受限:5/min,10/h)
    bak_daily.sync(drop_exist)  # 沪深股票-行情数据-备用行情


def use_age():
    print('Useage: python data_syn.py --mode [init | append | init_spc | append_spc] [--drop_exist]')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='sync mode args')

    parser.add_argument('--mode', required=True, choices=['normal', 'special'],
                        type=str, default='',
                        help='同步模式: normal(同步常规表),'
                             ' special(同步特殊表)')
    parser.add_argument('--drop_exist', action='store_true',
                        help='初始化建表过程如果表已存在 Drop 后再建')

    args = parser.parse_args()
    mode = args.mode
    drop_exist = args.drop_exist
    print('Args: --mode [%s] --drop-exist [%s]' % (mode, drop_exist))

    if mode == 'normal':
        sync(drop_exist)
    elif mode == 'special':
        sync_spc(drop_exist)
    else:
        use_age()
