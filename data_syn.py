"""
数据同步程序入口
要求 Tushare 积分 2000 以上
"""

import argparse
from tables.stock_basic import stock_basic
from tables.trade_cal import trade_cal
from tables.name_change import name_change
from tables.hs_const import hs_const
from tables.stk_rewards import stk_rewards
from tables.bak_basic import bak_basic
from tables.daily import daily
from tables.weekly import weekly
from tables.monthly import monthly
from tables.money_flow import money_flow
from tables.stk_limit import stk_limit
from tables.money_flow_hsgt import money_flow_hsgt
from tables.hsgt_top10 import hsgt_top10
from tables.ggt_top10 import ggt_top10
from tables.ggt_daily import ggt_daily
from tables.bak_daily import bak_daily
from tables.forecast import forecast
from tables.express import express
from tables.fina_indicator import fina_indicator
from tables.fina_mainbz import fina_mainbz
from tables.disclosure_date import disclosure_date
from tables.margin_detail import margin_detail
from tables.top_list import top_list
from tables.top_inst import top_inst
from tables.concept import concept
from tables.concept_detail import concept_detail
from tables.stk_holder_number import stk_holder_number
from tables.cyq_perf import cyq_perf
from tables.cyq_chips import cyq_chips


# 全量历史初始化
def init():
    # stock_basic.init()  # 沪深股票-基础信息-股票列表
    # trade_cal.init()  # 沪深股票-基础信息-交易日历
    # name_change.init()  # 沪深股票-基础信息-股票曾用名
    # hs_const.init()  # 沪深股票-基础信息-沪深股通成份股
    # stk_rewards.init()  # 沪深股票-基础信息-管理层薪酬和持股
    # daily.init()  # 沪深股票-行情数据-A股日线行情
    # weekly.init()  # 沪深股票-行情数据-A股周线行情
    # monthly.init()  # 沪深股票-行情数据-A股月线行情
    # money_flow.init()  # 沪深股票-行情数据-个股资金流向
    # stk_limit.init()  # 沪深股票-行情数据-每日涨跌停价格
    # money_flow_hsgt.init()  # 沪深股票-行情数据-沪深港通资金流向
    # hsgt_top10.init()  # 沪深股票-行情数据-沪深股通十大成交股
    ggt_top10.init()  # 沪深股票-行情数据-港股通十大成交股
    ggt_daily.init()  # 沪深股票-行情数据-港股通每日成交统计
    bak_daily.init()  # 沪深股票-行情数据-备用行情
    forecast.init()  # 沪深股票-财务数据-业绩预告
    express.init()  # 沪深股票-财务数据-业绩快报
    fina_indicator.init()  # 沪深股票-财务数据-财务指标数据
    fina_mainbz.init()  # 沪深股票-财务数据-主营业务构成
    disclosure_date.init()  # 沪深股票-财务数据-财报披露计划
    margin_detail.init()  # 沪深股票-市场参考数据-融资融券交易明细
    top_list.init()  # 沪深股票-市场参考数据-龙虎榜每日明细
    top_inst.init()  # 沪深股票-市场参考数据-龙虎榜机构明细
    stk_holder_number.init()  # 沪深股票-市场参考数据-股东人数


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
    bak_daily.append()  # 沪深股票-行情数据-备用行情
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
    bak_basic.init()  # 沪深股票-基础信息-备用列表 （读取限制,每分钟调用2次, 每天最多访问该接口20次）
    concept.init()  # 沪深股票-市场参考数据-概念股分类（已经停止维护）
    concept_detail.init()  # 沪深股票-市场参考数据-概念股列表 （已经停止维护）
    cyq_perf.init()  # 沪深股票-特色数据-每日筹码及胜率（受限:5/min,10/h)
    cyq_chips.init()  # 沪深股票-特色数据-每日筹码分布 (受限:5/min,10/h)


def append_spc():
    bak_basic.append()  # 沪深股票-基础信息-备用列表 （读取限制,每分钟调用2次, 每天最多访问该接口20次）
    cyq_perf.append()  # 沪深股票-特色数据-每日筹码及胜率（受限:5/min,10/h)
    cyq_chips.append()  # 沪深股票-特色数据-每日筹码分布 (受限:5/min,10/h)


def use_age():
    print('Useage: python data_syn.py --mode [init | append | init_spc | append_spc]')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='sync mode args')
    parser.add_argument("--mode", type=str, default='', help='同步模式: init(初始化模式), append(增量追加模式),'
                                                             ' init_spc(初始化特殊处理模式), append_spc(特殊处理增量追加模式)')
    args = parser.parse_args()
    mode = args.mode
    if mode == 'init':
        init()
    elif mode == 'append':
        append()
    elif mode == init_spc:
        init_spc()
    elif mode == 'append_spc':
        append_spc()
    else:
        use_age()
