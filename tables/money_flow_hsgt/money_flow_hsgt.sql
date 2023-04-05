-- stock.money_flow_hsgt definition

DROP TABLE IF EXISTS `money_flow_hsgt`;
CREATE TABLE `money_flow_hsgt`
(
    `trade_date`   int                DEFAULT NULL COMMENT '交易日期',
    `ggt_ss`       double             DEFAULT NULL COMMENT '港股通（上海）',
    `ggt_sz`       double             DEFAULT NULL COMMENT '港股通（深圳）',
    `hgt`          double             DEFAULT NULL COMMENT '沪股通（百万元）',
    `sgt`          double             DEFAULT NULL COMMENT '深股通（百万元）',
    `north_money`  double             DEFAULT NULL COMMENT '北向资金（百万元）',
    `south_money`  double             DEFAULT NULL COMMENT '南向资金（百万元）',
    `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
     KEY `money_flow_hsgt_trade_date` (`trade_date`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT ='沪深股票-行情数据-沪深港通资金流向';
