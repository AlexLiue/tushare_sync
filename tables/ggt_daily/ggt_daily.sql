-- stock.ggt_daily definition

DROP TABLE IF EXISTS `ggt_daily`;
CREATE TABLE `ggt_daily`
(
    `trade_date`   int                DEFAULT NULL COMMENT '交易日期',
    `buy_amount`   double             DEFAULT NULL COMMENT '买入成交金额（亿元）',
    `buy_volume`   double             DEFAULT NULL COMMENT '买入成交笔数（万笔）',
    `sell_amount`  double             DEFAULT NULL COMMENT '卖出成交金额（亿元）',
    `sell_volume`  double             DEFAULT NULL COMMENT '卖出成交笔数（万笔）',
    `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
     KEY `ggt_daily_trade_date` (`trade_date`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT ='沪深股票-行情数据-港股通每日成交统计';
