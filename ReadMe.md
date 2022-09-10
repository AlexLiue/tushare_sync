# Sync Tushare Data to MySQL 
- 同步 Tushare 的股票交易数据到本地 MySQL 进行存储, 采用 T + 1 同步方式
- 首先从 Tushare 拉取全量历史数据
- 然后每日从 Tushare 拉取昨日增量数据

## 使用方法

### Step1: 修改配置文件信息(本地数据库地址 / Tushare 账号 token)
```shell
mv application.ini.example application.ini
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



## 已完成的同步表

| 表名                 |         接口名         | 表说明                                                        |  
|:-------------------|:-------------------:|:-----------------------------------------------------------|  
| stock_basic        |     stock_basic     | 沪深股票-基础信息-股票列表                                             |  
| trade_cal          |      trade_cal      | 沪深股票-基础信息-交易日历                                             |  
| name_change        |     namechange      | 沪深股票-基础信息-股票曾用名                                            |  
| hs_const           |      hs_const       | 沪深股票-基础信息-沪深股通成份股                                          |
| stk_rewards        |     stk_rewards     | 沪深股票-基础信息-管理层薪酬和持股（数据量较大,不存在日更新逻辑, 选择性同步）     |  
| bak_basic          |      bak_basic      | 沪深股票-基础信息-备用列表(数据量较大, 2000积分每分钟只能调用2次,独立处理)     |  
| daily              |        daily        | 沪深股票-行情数据-A股日线行情                                           |  
| weekly             |       weekly        | 沪深股票-行情数据-A股周线行情                                           |  
| monthly            |       monthly       | 沪深股票-行情数据-A股月线行情                                           |  
| money_flow         |      moneyflow      | 沪深股票-行情数据-个股资金流向                                           |  
| stk_limit          |      stk_limit      | 沪深股票-行情数据-每日涨跌停价格                                          |  
| money_flow_hsgt    |   moneyflow_hsgt    | 沪深股票-行情数据-沪深港通资金流向                                         |  
| hsgt_top10         |   hsgt_top10        | 沪深股票-行情数据-沪深股通十大成交股                                        |  


## 其他
欢迎提问或 Bug / PR 提交




接口：


