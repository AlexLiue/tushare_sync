# Sync Tushare Data to MySQL 
同步 Tushare 的股票交易数据到本地 MySQL 进行存储

## 使用方法

### Step1: 修改配置文件信息(本地数据库地址 / Tushare 账号 token), 配置文件模板参考 [`application.ini.example`](application.ini.example)
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
说明1: 部分表数据量相对较小火不具备增量同步逻辑，因此选择每日全量同步



## 已完成的同步表

| 表名              |      接口名      | 表说明                                         |  
|:----------------|:-------------:|:--------------------------------------------|  
| stock_basic     |  stock_basic  | 沪深股票-基础信息-股票列表                              |  
| trade_cal       |   trade_cal   | 沪深股票-基础信息-交易日历                              |  
| name_change     |  namechange   | 沪深股票-基础信息-股票曾用名                             |  
| hs_const        |   hs_const    | 沪深股票-基础信息-沪深股通成份股                           |
| stk_rewards     |  stk_rewards  | 沪深股票-基础信息-管理层薪酬和持股（数据量较大,不存在日更新逻辑, 选择性同步）   |  
| bak_basic       |   bak_basic   | 沪深股票-基础信息-备用列表(数据量较大, 2000积分每分钟只能调用2次,独立处理) |  
| daily           |     daily     | 沪深股票-行情数据-A股日线行情                            |  
| weekly          |    weekly     | 沪深股票-行情数据-A股周线行情                            |  
| monthly         |    monthly    | 沪深股票-行情数据-A股月线行情                            |  
| money_flow      |   moneyflow   | 沪深股票-行情数据-个股资金流向                            |  
| A               |       B       | C                                           |  
| A               |       B       | C                                           |  
| A               |       B       | C                                           |  


## 其他
欢迎提问或 Bug 提交
