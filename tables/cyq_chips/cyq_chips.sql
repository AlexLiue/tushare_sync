-- stock.cyq_chips definition

DROP TABLE IF EXISTS `cyq_chips`;
CREATE TABLE `cyq_chips`
(
    `ts_code`      varchar(16)        DEFAULT NULL COMMENT '股票代码',
    `trade_date`   int                DEFAULT NULL COMMENT '交易日期',
    `price`        double             DEFAULT NULL COMMENT '成本价格',
    `percent`      double             DEFAULT NULL COMMENT '价格占比（%）',
    `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
     KEY `cyq_chips_ts_code` (`ts_code`, `trade_date`) USING BTREE,
     KEY `cyq_chips_trade_date` (`trade_date`, `ts_code`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT ='沪深股票-市场参考数据-每日筹码分布';

