# Sync Tushare Data to MySQL - 股票数据获取
- 同步 [Tushare](https://tushare.pro) 的股票交易数据到本地 MySQL 进行存储, 采用 T + 0 同步方式
- 首先从 Tushare 拉取全量历史数据
- 然后每日下午 从 Tushare 拉取当日增量数据
- 数据包含: A股、港股、日线、周线、月线等

## 使用方法

### Step1: 修改配置文件信息(本地数据库地址信息、Tushare 账号 token)
```shell
mv application.ini.template application.ini
# 然后修改 application.ini 中的 mysql 的地址信息 和 Tushare 账号 token
```

### Step2: 全量初始化同步
```shell
python data_syn.py --mode init
```
说明1: 执行前要求 application.ini 配置中的 mysql.database 库已创建, 程序会自动在该数据库下创建数据表   
说明2: Tushare 对不同积分的账户存在权限限制, 本程序代码要求 积分额度 2000 以上, 如不足可根据权限自行删减 [data_syn.py](data_syn.py) 中的部分表   
说明3: 部分表数据同步存在流量限制, 全量初始化时间相对较长   

### Step3: 每日增量拉取同步
```shell
python data_syn.py --mode append
```
说明1: 部分表数据量相对较小或者不具备增量同步逻辑，因此选择每日全量同步

## MySQL 结果数据示列
沪深股票-行情数据-A股日线行情（daily表数据）
```text
id |ts_code  |trade_date|open  |high  |low   |close |pre_close|change|pct_chg|vol      |amount     |
---+---------+----------+------+------+------+------+---------+------+-------+---------+-----------+
  1|689009.SH|2022-09-09| 43.05|  43.9|  42.7|  43.7|    43.03|  0.67| 1.5571| 15372.24|  66680.763|
  2|873223.BJ|2022-09-09|   3.8|  3.87|  3.79|  3.82|     3.79|  0.03| 0.7916|  6070.21|   2322.889|
  3|873169.BJ|2022-09-09|  6.38|  6.41|  6.36|  6.39|     6.38|  0.01| 0.1567|  1865.95|   1190.126|
  4|872925.BJ|2022-09-09| 15.89| 15.92| 15.68| 15.87|    15.92| -0.05|-0.3141|     20.5|     32.486|
  5|871981.BJ|2022-09-09|  16.8|  16.8| 16.58| 16.75|    16.68|  0.07| 0.4197|   686.83|   1142.099|
  6|871970.BJ|2022-09-09|  9.01|  9.03|  9.01|  9.02|     9.01|  0.01|  0.111|    119.0|    107.361|
  7|871857.BJ|2022-09-09|  9.11|  9.11|  8.96|   9.0|     8.99|  0.01| 0.1112|    57.68|     51.906|
  8|871642.BJ|2022-09-09|  7.04|  7.04|  6.89|  7.04|     7.04|   0.0|    0.0|   552.55|    383.902|
```

## 已完成的同步表
### 常规处理的表
| MySQL表名                                                             | Tushare  接口名          | 数据说明                                                                           |  
|:--------------------------------------------------------------------|:----------------------|:-------------------------------------------------------------------------------|  
| [stock_basic](tables/stock_basic/stock_basic.sql)                   | stock_basic           | [沪深股票-基础信息-股票列表](https://tushare.pro/document/2?doc_id=25) (每日全量覆盖)            |  
| [trade_cal](tables/trade_cal/trade_cal.sql)                         | trade_cal             | [沪深股票-基础信息-交易日历](https://tushare.pro/document/2?doc_id=26) (每日全量覆盖)            |  
| [name_change](tables/name_change/name_change.sql)                   | namechange            | [沪深股票-基础信息-股票曾用名](https://tushare.pro/document/2?doc_id=100) (每日全量覆盖)          |  
| [hs_const](tables/hs_const/hs_const.sql)                            | hs_const              | [沪深股票-基础信息-沪深股通成份股](https://tushare.pro/document/2?doc_id=104) (每日全量覆盖)        |
| [stk_rewards](tables/stk_rewards/stk_rewards.sql)                   | stk_rewards           | [沪深股票-基础信息-管理层薪酬和持股](https://tushare.pro/document/2?doc_id=194) (每日增量覆盖近10日数据) |
| [daily](tables/daily/daily.sql)                                     | daily                 | [沪深股票-行情数据-A股日线行情](https://tushare.pro/document/2?doc_id=27)                   |  
| [weekly](tables/weekly/weekly.sql)                                  | weekly                | [沪深股票-行情数据-A股周线行情](https://tushare.pro/document/2?doc_id=144)                  |  
| [monthly](tables/monthly/monthly.sql)                               | monthly               | [沪深股票-行情数据-A股月线行情](https://tushare.pro/document/2?doc_id=145)                  |  
| [money_flow](tables/money_flow/money_flow.sql)                      | moneyflow             | [沪深股票-行情数据-个股资金流向](https://tushare.pro/document/2?doc_id=170)                  |  
| [stk_limit](tables/stk_limit/stk_limit.sql)                         | stk_limit             | [沪深股票-行情数据-每日涨跌停价格](https://tushare.pro/document/2?doc_id=183)                 |  
| [money_flow_hsgt](tables/money_flow_hsgt/money_flow_hsgt.sql)       | moneyflow_hsgt        | [沪深股票-行情数据-沪深港通资金流向](https://tushare.pro/document/2?doc_id=47)                 |  
| [hsgt_top10](tables/hsgt_top10/hsgt_top10.sql)                      | hsgt_top10            | [沪深股票-行情数据-沪深股通十大成交股](https://tushare.pro/document/2?doc_id=48)                |  
| [ggt_top10](tables/ggt_top10/ggt_top10.sql)                         | ggt_top10             | [沪深股票-行情数据-港股通十大成交股](https://tushare.pro/document/2?doc_id=49)                 |
| [ggt_daily](tables/ggt_daily/ggt_daily.sql)                         | ggt_daily             | [沪深股票-行情数据-港股通每日成交统计](https://tushare.pro/document/2?doc_id=196)               |
| [bak_daily](tables/bak_daily/bak_daily.sql)                         | bak_daily             | [沪深股票-行情数据-备用行情](https://tushare.pro/document/2?doc_id=255)                    |  
| [forecast](tables/forecast/forecast.sql)                            | forecast              | [沪深股票-财务数据-业绩预告](https://tushare.pro/document/2?doc_id=45)                     |  
| [express](tables/express/express.sql)                               | express               | [沪深股票-财务数据-业绩快报](https://tushare.pro/document/2?doc_id=46)                     |  
| [fina_indicator](tables/fina_indicator/fina_indicator.sql)          | fina_indicator        | [沪深股票-财务数据-财务指标数据](https://tushare.pro/document/2?doc_id=79)                   |  
| [fina_mainbz](tables/fina_mainbz/fina_mainbz.sql)                   | fina_mainbz           | [沪深股票-财务数据-主营业务构成](https://tushare.pro/document/2?doc_id=81)                   |  
| [disclosure_date](tables/disclosure_date/disclosure_date.sql)       | disclosure_date       | [沪深股票-财务数据-财报披露计划](https://tushare.pro/document/2?doc_id=162)                  |
| [margin_detail](tables/margin_detail/margin_detail.sql)             | margin_detail         | [沪深股票-市场参考数据-融资融券交易明细](https://tushare.pro/document/2?doc_id=59)               |  
| [top_list](tables/top_list/top_list.sql)                            | top_list              | [沪深股票-市场参考数据-龙虎榜每日明细](https://tushare.pro/document/2?doc_id=106)               |  
| [top_inst](tables/top_inst/top_inst.sql)                            | top_inst              | [沪深股票-市场参考数据-龙虎榜机构交易明细](https://tushare.pro/document/2?doc_id=107)             |  
| [repurchase](tables/repurchase/repurchase.sql)                      | repurchase            | [沪深股票-市场参考数据-股票回购](https://tushare.pro/document/2?doc_id=124)                                                           |
| [share_float](tables/share_float/share_float.sql)                   | share_float           | [沪深股票-市场参考数据-限售股解禁](https://tushare.pro/document/2?doc_id=160)                                                          |
| [stk_holder_number](tables/stk_holder_number/stk_holder_number.sql) | stk_holdernumber      | [沪深股票-市场参考数据-股东人数](https://tushare.pro/document/2?doc_id=166)                                                           |


## 特殊处理
| MySQL表名                                                    | Tushare  接口名    | 数据说明                                                                            |  
|:-----------------------------------------------------------|:----------------|:--------------------------------------------------------------------------------|
| [bak_basic](tables/bak_basic/bak_basic.sql)                | bak_basic       | [沪深股票-基础信息-备用列表](https://tushare.pro/document/2?doc_id=262)（受限:2/min）           |  
| [concept](tables/concept/concept.sql)                      | concept         | [沪深股票-市场参考数据-概念股分类](https://tushare.pro/document/2?doc_id=125)（已经停止维护）          |
| [concept_detail](tables/concept_detail/concept_detail.sql) | concept_detail  | [沪深股票-市场参考数据-概念股列表](https://tushare.pro/document/2?doc_id=126) （已经停止维护）         |
| [cyq_perf](tables/cyq_perf/cyq_perf.sql)                   | cyq_perf        | [沪深股票-特色数据-每日筹码及胜率](https://tushare.pro/document/2?doc_id=293) （受限:5/min,10/h)  |
| [cyq_chips](tables/cyq_chips/cyq_chips.sql)                | cyq_chips       | [沪深股票-市场参考数据-每日筹码分布](https://tushare.pro/document/2?doc_id=294) (受限:5/min,10/h) |



## 主要接口函数
```python
import datetime

import time
from utils.utils import get_tushare_api,get_mock_connection,get_logger,exec_mysql_sql,min_date
def exec_sync_without_ts_code(table_name, api_name, fields,
                              date_column, start_date, end_date, date_step, limit, interval):
    """
    执行数据同步并存储
    :param table_name: 表名
    :param api_name: API 名
    :param fields: 字段列表
    :param date_column: 增量时间字段列
    :param start_date: 开始时间
    :param end_date: 结束时间
    :param date_step: 分段查询间隔, 由于 Tushare 分页查询存在性能瓶颈, 因此采用按时间分段拆分微批查询
    :param limit: 每次查询的记录条数
    :param interval: 每次查询的时间间隔
    :return: None
    """
    # 创建 API / Connection / Logger 对象
    ts_api = get_tushare_api()
    connection = get_mock_connection()
    logger = get_logger(table_name, 'data_syn.log')

    # 清理历史数据
    clean_sql = "DELETE FROM %s WHERE %s>='%s' AND %s<='%s'" % \
                (table_name, date_column, start_date, date_column, end_date)
    logger.info('Execute Clean SQL [%s]' % clean_sql)
    exec_mysql_sql(clean_sql)

    # 数据同步时间开始时间和结束时间, 包含前后边界
    start = datetime.datetime.strptime(start_date, '%Y%m%d')
    end = datetime.datetime.strptime(end_date, '%Y%m%d')

    step_start = start  # 微批开始时间
    step_end = min_date(start + datetime.timedelta(date_step - 1), end)  # 微批结束时间

    while step_start <= end:
        start_date = str(step_start.strftime('%Y%m%d'))
        end_date = str(step_end.strftime('%Y%m%d'))
        offset = 0
        while True:
            logger.info("Query [%s] from tushare with api[%s] start_date[%s] end_date[%s]"
                        " from offset[%d] limit[%d]" % (table_name, api_name, start_date, end_date, offset, limit))

            data = ts_api.query(api_name,
                                **{
                                    "start_date": start_date,
                                    "end_date": end_date,
                                    "offset": offset,
                                    "limit": limit
                                },
                                fields=fields)
            time.sleep(interval)
            if data.last_valid_index() is not None:
                size = data.last_valid_index() + 1
                logger.info('Write [%d] records into table [%s] with [%s]' % (size, table_name, connection.engine))
                data.to_sql(table_name, connection, index=False, if_exists='append', chunksize=limit)
                offset = offset + size
                if size < limit:
                    break
            else:
                break
        # 更新下一次微批时间段
        step_start = step_start + datetime.timedelta(date_step)
        step_end = min_date(step_end + datetime.timedelta(date_step), end)

```
## 接口使用示例
以 沪深股票-行情数据-A股日线行情（daily）为例   
### 全量历史数据初始化

```python
from utils.utils import exec_mysql_script, exec_sync_without_ts_code
import os
import datetime


def init():
    # 创建表
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    exec_mysql_script(dir_path)

    exec_sync_without_ts_code(
        table_name='daily',
        api_name='daily',
        fields=[
            "ts_code",
            "trade_date",
            "open",
            "high",
            "low",
            "close",
            "pre_close",
            "change",
            "pct_chg",
            "vol",
            "amount"
        ],
        start_date='19901219',
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=1,
        limit=5000,
        interval=0.3
    )
```
### 增量数据每日更新
其中： start_date 可以前回溯一段时间, 防止原始数据中断或者延迟导致的数据丢失

```python
from utils.utils import exec_sync_without_ts_code
import datetime


def append():
    exec_sync_without_ts_code(
        table_name='daily',
        api_name='daily',
        fields=[
            "ts_code",
            "trade_date",
            "open",
            "high",
            "low",
            "close",
            "pre_close",
            "change",
            "pct_chg",
            "vol",
            "amount"
        ],
        start_date=str((datetime.datetime.now() + datetime.timedelta(days=-7)).strftime('%Y%m%d')),
        end_date=str(datetime.datetime.now().strftime('%Y%m%d')),
        date_step=1,
        limit=5000,
        interval=0.3
    )
```

## 执行日志说明
相关日志打印存储在 项目根目录/logs/data_syn.log 文件中, 日志示例
```shell
ssh://anaconda@47.240.xxx.xxx:22/home/anaconda/anaconda3/bin/python -u /app/stock_tushare_syn/data_syn.py --mode init
2022-09-10 09:57:57,588 - stock_basic - INFO - Execute SQL [DROP TABLE IF EXISTS `stock_basic`]
2022-09-10 09:57:57,732 - stock_basic - INFO - Execute SQL [CREATE TABLE `stock_basic`(`id` bigint NOT NULL AUTO_INCREMENT COMMENT ' 主键 ',`ts_code` varchar(16) DEFAULT NULL COMMENT ' TS代码 ',`symbol` varchar(16) DEFAULT NULL COMMENT ' 股票代码 ',`name` varchar(32) DEFAULT NULL COMMENT ' 股票名称 ',`area` varchar(32) DEFAULT NULL COMMENT ' 地域 ',`industry` varchar(32) DEFAULT NULL COMMENT ' 所属行业 ',`fullname` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT ' 股票全称 ',`enname` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT ' 英文全称 ',`cnspell` varchar(32) DEFAULT NULL COMMENT ' 拼音缩写 ',`market` varchar(32) DEFAULT NULL COMMENT ' 市场类型:主板/创业板/科创板/CDR',`exchange` varchar(32) DEFAULT NULL COMMENT ' 交易所代码 ',`curr_type` varchar(32) DEFAULT NULL COMMENT ' 交易货币 ',`list_status` varchar(32) DEFAULT NULL COMMENT ' 上市状态 L上市 D退市 P暂停上市 ',`list_date` date DEFAULT NULL COMMENT ' 上市日期 ',`delist_date` date DEFAULT NULL COMMENT ' 退市日期 ',`is_hs` varchar(32) DEFAULT NULL COMMENT ' 是否沪深港通标:N否 H沪股通 S深股通 ',PRIMARY KEY (`id`)) ENGINE=InnoDB AUTO_INCREMENT=4902 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='基础信息']
2022-09-10 09:57:57,768 - stock_basic - INFO - Execute result: Total [2], Succeed [2] , Failed [0] 
2022-09-10 09:57:58,045 - stock_basic - INFO - Query data from tushare with api[stock_basic], fields[ts_code,symbol,name,area,industry,fullname,enname,cnspell,market,exchange,curr_type,list_status,list_date,delist_date,is_hs]
2022-09-10 09:57:59,047 - stock_basic - INFO - Write [4909] records into table [stock_basic] with [Engine(mysql://root:***@47.240.xxx.xxx:3320/stock?charset=utf8&use_unicode=1)]
2022-09-10 09:57:59,683 - trade_cal - INFO - Execute SQL [DROP TABLE IF EXISTS `trade_cal`]
2022-09-10 09:57:59,696 - trade_cal - INFO - Execute SQL [CREATE TABLE `trade_cal`(`id` bigint NOT NULL AUTO_INCREMENT COMMENT ' 主键 ',`exchange` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '交易所 SSE上交所 SZSE深交所',`cal_date` date DEFAULT NULL COMMENT '日历日期',`is_open` varchar(2) DEFAULT NULL COMMENT '是否交易 0休市 1交易',`pretrade_date` date DEFAULT NULL COMMENT '上一个交易日',PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='交易日历']
2022-09-10 09:57:59,716 - trade_cal - INFO - Execute result: Total [2], Succeed [2] , Failed [0] 
2022-09-10 09:57:59,720 - trade_cal - INFO - Query data from tushare with api[trade_cal], start[19700101]- end[20220910], fields[exchange,cal_date,is_open,pretrade_date]
2022-09-10 09:58:00,476 - trade_cal - INFO - Write [11589] records into table [trade_cal] with [Engine(mysql://root:***@47.240.xxx.xxx:3320/stock?charset=utf8&use_unicode=1)]
2022-09-10 09:58:00,929 - name_change - INFO - Execute SQL [DROP TABLE IF EXISTS `name_change`]
2022-09-10 09:58:00,944 - name_change - INFO - Execute SQL [CREATE TABLE `name_change`(`id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',`ts_code` varchar(16) DEFAULT NULL COMMENT 'TS代码',`name` varchar(32) DEFAULT NULL COMMENT '证券名称',`start_date` date DEFAULT NULL COMMENT '开始日期',`end_date` date DEFAULT NULL COMMENT '结束日期',`ann_date` date DEFAULT NULL COMMENT '公告日期',`change_reason` varchar(64) DEFAULT NULL COMMENT '变更原因',PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='股票曾用名']
2022-09-10 09:58:00,964 - name_change - INFO - Execute result: Total [2], Succeed [2] , Failed [0] 
2022-09-10 09:58:00,967 - name_change - INFO - Query data from tushare with api[namechange], fields[ts_code,name,start_date,end_date,ann_date,change_reason]
2022-09-10 09:58:01,700 - name_change - INFO - Write [10000] records into table [stock_basic] with [Engine(mysql://root:***@47.240.xxx.xxx:3320/stock?charset=utf8&use_unicode=1)]
```


## 其他

欢迎提问或 提交 Bug / PR   


