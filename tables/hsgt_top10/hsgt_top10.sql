-- stock.hsgt_top10 definition

DROP TABLE IF EXISTS `hsgt_top10`;
CREATE TABLE `hsgt_top10`
(
    `trade_date`   int                DEFAULT NULL COMMENT '交易日期',
    `ts_code`      varchar(16)        DEFAULT NULL COMMENT '股票代码',
    `name`         varchar(64)        DEFAULT NULL COMMENT '股票名称',
    `close`        double             DEFAULT NULL COMMENT '收盘价',
    `change`       double             DEFAULT NULL COMMENT '涨跌幅',
    `rank`         int                DEFAULT NULL COMMENT '资金排名',
    `market_type`  int                DEFAULT NULL COMMENT '市场类型（1：沪市 3：深市）',
    `amount`       double             DEFAULT NULL COMMENT '成交金额',
    `net_amount`   double             DEFAULT NULL COMMENT '净成交金额',
    `buy`          double             DEFAULT NULL COMMENT '买入金额',
    `sell`         double             DEFAULT NULL COMMENT '卖出金额',
    `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
     KEY `hsgt_top10_ts_code` (`ts_code`, `trade_date`) USING BTREE,
     KEY `hsgt_top10_trade_date` (`trade_date`, `ts_code`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT ='沪深股票-行情数据-沪深股通十大成交股';
