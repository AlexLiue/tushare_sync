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
def init(drop_exist):
    # stock_basic.init(drop_exist)  # 沪深股票-基础信息-股票列表
    # trade_cal.init(drop_exist)  # 沪深股票-基础信息-交易日历
    # name_change.init(drop_exist)  # 沪深股票-基础信息-股票曾用名
    # hs_const.init(drop_exist)  # 沪深股票-基础信息-沪深股通成份股
    # stk_rewards.init(drop_exist)  # 沪深股票-基础信息-管理层薪酬和持股
    # daily.init(drop_exist)  # 沪深股票-行情数据-A股日线行情
    weekly.init(drop_exist)  # 沪深股票-行情数据-A股周线行情
    monthly.init(drop_exist)  # 沪深股票-行情数据-A股月线行情
    money_flow.init(drop_exist)  # 沪深股票-行情数据-个股资金流向
    stk_limit.init(drop_exist)  # 沪深股票-行情数据-每日涨跌停价格
    money_flow_hsgt.init(drop_exist)  # 沪深股票-行情数据-沪深港通资金流向
    hsgt_top10.init(drop_exist)  # 沪深股票-行情数据-沪深股通十大成交股
    ggt_top10.init(drop_exist)  # 沪深股票-行情数据-港股通十大成交股
    ggt_daily.init(drop_exist)  # 沪深股票-行情数据-港股通每日成交统计
    forecast.init(drop_exist)  # 沪深股票-财务数据-业绩预告
    express.init(drop_exist)  # 沪深股票-财务数据-业绩快报
    fina_indicator.init(drop_exist)  # 沪深股票-财务数据-财务指标数据
    fina_mainbz.init(drop_exist)  # 沪深股票-财务数据-主营业务构成
    disclosure_date.init(drop_exist)  # 沪深股票-财务数据-财报披露计划
    margin_detail.init(drop_exist)  # 沪深股票-市场参考数据-融资融券交易明细
    top_list.init(drop_exist)  # 沪深股票-市场参考数据-龙虎榜每日明细
    top_inst.init(drop_exist)  # 沪深股票-市场参考数据-龙虎榜机构明细
    stk_holder_number.init(drop_exist)  # 沪深股票-市场参考数据-股东人数


# 增量数据追加同步
def append():
    stock_basic.append()  # 沪深股票-基础信息-股票列表
    trade_cal.append()  # 沪深股票-基础信息-交易日历
    name_change.append()  # 沪深股票-基础信息-股票曾用名
    hs_const.append()  # 沪深股票-基础信息-沪深股通成份股
    stk_rewards.append()  # 沪深股票-基础信息-管理层薪酬和持股
    daily.append()  # 沪深股票-行情数据-A股日线行情
    weekly.append()  # 沪深股票-行情数据-A股周线行情
    monthly.append()  # 沪深股票-行情数据-A股月线行情
    money_flow.append()  # 沪深股票-行情数据-个股资金流向
    stk_limit.append()  # 沪深股票-行情数据-每日涨跌停价格
    money_flow_hsgt.append()  # 沪深股票-行情数据-沪深港通资金流向
    hsgt_top10.append()  # 沪深股票-行情数据-沪深股通十大成交股
    ggt_top10.append()  # 沪深股票-行情数据-港股通十大成交股
    ggt_daily.append()  # 沪深股票-行情数据-港股通每日成交统计
    forecast.append()  # 沪深股票-财务数据-业绩预告
    express.append()  # 沪深股票-财务数据-业绩快报
    fina_indicator.append()  # 沪深股票-财务数据-财务指标数据
    fina_mainbz.append()  # 沪深股票-财务数据-主营业务构成
    disclosure_date.append()  # 沪深股票-财务数据-财报披露计划
    margin_detail.append()  # 沪深股票-市场参考数据-融资融券交易明细
    top_list.append()  # 沪深股票-市场参考数据-龙虎榜每日明细
    top_inst.append()  # 沪深股票-市场参考数据-龙虎榜机构明细
    stk_holder_number.append()  # 沪深股票-市场参考数据-股东人数


def init_spc():
    bak_basic.init(drop_exist)  # 沪深股票-基础信息-备用列表 （读取限制,每分钟调用2次, 每天最多访问该接口20次）
    concept.init(drop_exist)  # 沪深股票-市场参考数据-概念股分类（已经停止维护）
    concept_detail.init(drop_exist)  # 沪深股票-市场参考数据-概念股列表 （已经停止维护）
    cyq_perf.init(drop_exist)  # 沪深股票-特色数据-每日筹码及胜率（受限:5/min,10/h)
    cyq_chips.init(drop_exist)  # 沪深股票-特色数据-每日筹码分布 (受限:5/min,10/h)
    bak_daily.init(drop_exist)  # 沪深股票-行情数据-备用行情


def append_spc():
    bak_basic.append()  # 沪深股票-基础信息-备用列表 （读取限制,每分钟调用2次, 每天最多访问该接口20次）
    cyq_perf.append()  # 沪深股票-特色数据-每日筹码及胜率（受限:5/min,10/h)
    cyq_chips.append()  # 沪深股票-特色数据-每日筹码分布 (受限:5/min,10/h)
    bak_daily.append()  # 沪深股票-行情数据-备用行情( 受限:50/天)


def use_age():
    print('Useage: python data_syn.py --mode [init | append | init_spc | append_spc] [--drop_exist]')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='sync mode args')

    parser.add_argument('--mode', required=True, choices=['init', 'append', 'init_spc', 'append_spc'],
                        type=str, default='',
                        help='同步模式: init(初始化模式),'
                             ' append(增量追加模式),'
                             ' init_spc(初始化特殊处理模式),'
                             ' append_spc(特殊处理增量追加模式)')
    parser.add_argument('--drop_exist', action='store_true',
                        help='初始化建表过程如果表已存在 Drop 后再建')

    args = parser.parse_args()
    mode = args.mode
    drop_exist = args.drop_exist
    print('Args: --mode [%s] --drop_exist [%s]' % (mode, drop_exist))

    if mode == 'init':
        init(drop_exist)
    elif mode == 'append':
        append()
    elif mode == init_spc:
        init_spc()
    elif mode == 'append_spc':
        append_spc()
    else:
        use_age()
