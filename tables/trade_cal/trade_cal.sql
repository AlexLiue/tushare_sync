-- stock.trade_cal definition

DROP TABLE IF EXISTS `trade_cal`;
CREATE TABLE `trade_cal`
(
    `id`            bigint    NOT NULL AUTO_INCREMENT COMMENT ' 主键 ',
    `exchange`      varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '交易所 SSE上交所 SZSE深交所',
    `cal_date`      int                                                         DEFAULT NULL COMMENT '日历日期',
    `is_open`       varchar(2)                                                   DEFAULT NULL COMMENT '是否交易 0休市 1交易',
    `pretrade_date` int                                                         DEFAULT NULL COMMENT '上一个交易日',
    `created_time`  timestamp NOT NULL                                           DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time`  timestamp NOT NULL                                           DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='交易日历';
