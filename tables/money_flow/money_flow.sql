-- stock.money_flow definition

DROP TABLE IF EXISTS `money_flow`;
CREATE TABLE `money_flow`
(
    `id`              bigint    NOT NULL AUTO_INCREMENT COMMENT '主键',
    `ts_code`         varchar(16)        DEFAULT NULL COMMENT 'TS代码',
    `trade_date`      date               DEFAULT NULL COMMENT '交易日期',
    `buy_sm_vol`      int                DEFAULT NULL COMMENT '小单买入量（手）',
    `buy_sm_amount`   double             DEFAULT NULL COMMENT '小单买入金额（万元）',
    `sell_sm_vol`     int                DEFAULT NULL COMMENT '小单卖出量（手）',
    `sell_sm_amount`  double             DEFAULT NULL COMMENT '小单卖出金额（万元）',
    `buy_md_vol`      int                DEFAULT NULL COMMENT '中单买入量（手）',
    `buy_md_amount`   double             DEFAULT NULL COMMENT '中单买入金额（万元）',
    `sell_md_vol`     int                DEFAULT NULL COMMENT '中单卖出量（手）',
    `sell_md_amount`  double             DEFAULT NULL COMMENT '中单卖出金额（万元）',
    `buy_lg_vol`      int                DEFAULT NULL COMMENT '大单买入量（手）',
    `buy_lg_amount`   double             DEFAULT NULL COMMENT '大单买入金额（万元）',
    `sell_lg_vol`     int                DEFAULT NULL COMMENT '大单卖出量（手）',
    `sell_lg_amount`  double             DEFAULT NULL COMMENT '大单卖出金额（万元）',
    `buy_elg_vol`     int                DEFAULT NULL COMMENT '特大单买入量（手）',
    `buy_elg_amount`  double             DEFAULT NULL COMMENT '特大单买入金额（万元）',
    `sell_elg_vol`    int                DEFAULT NULL COMMENT '特大单卖出量（手）',
    `sell_elg_amount` double             DEFAULT NULL COMMENT '特大单卖出金额（万元）',
    `net_mf_vol`      int                DEFAULT NULL COMMENT '净流入量（手）',
    `net_mf_amount`   double             DEFAULT NULL COMMENT '净流入额（万元）',
    `trade_count`     int                DEFAULT NULL COMMENT '交易笔数',
    `created_time`    timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time`    timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='沪深股票-行情数据-个股资金流向';
