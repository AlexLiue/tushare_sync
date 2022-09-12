-- stock.margin_detail definition

DROP TABLE IF EXISTS `margin_detail`;
CREATE TABLE `margin_detail`
(
    `id`           bigint    NOT NULL AUTO_INCREMENT COMMENT '主键',
    `trade_date`   date               DEFAULT NULL COMMENT '交易日期',
    `ts_code`      varchar(16)        DEFAULT NULL COMMENT 'TS股票代码',
    `name`         varchar(128)       DEFAULT NULL COMMENT '股票名称',
    `rzye`         double             DEFAULT NULL COMMENT '融资余额(元)',
    `rqye`         double             DEFAULT NULL COMMENT '融券余额(元)',
    `rzmre`        double             DEFAULT NULL COMMENT '融资买入额(元)',
    `rqyl`         double             DEFAULT NULL COMMENT '融券余量（手）',
    `rzche`        double             DEFAULT NULL COMMENT '融资偿还额(元)',
    `rqchl`        double             DEFAULT NULL COMMENT '融券偿还量(手)',
    `rqmcl`        double             DEFAULT NULL COMMENT '融券卖出量(股,份,手)',
    `rzrqye`       double             DEFAULT NULL COMMENT '融资融券余额(元)',
    `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='沪深股票-市场参考数据-融资融券交易明细';