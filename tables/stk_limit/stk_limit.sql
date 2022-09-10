-- stock.stk_limit definition

DROP TABLE IF EXISTS `stk_limit`;
CREATE TABLE `stk_limit`
(
    `id`         bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
    `trade_date` date        DEFAULT NULL COMMENT '交易日期',
    `ts_code`    varchar(16) DEFAULT NULL COMMENT 'TS股票代码',
    `pre_close`  double      DEFAULT NULL COMMENT '昨日收盘价',
    `up_limit`   double      DEFAULT NULL COMMENT '涨停价',
    `down_limit` double      DEFAULT NULL COMMENT '跌停价',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='沪深股票-行情数据-每日涨跌停价格';