-- stock.weekly definition

DROP TABLE IF EXISTS `weekly`;
CREATE TABLE `weekly`
(
    `id`           bigint    NOT NULL AUTO_INCREMENT COMMENT '主键',
    `ts_code`      varchar(16)        DEFAULT NULL COMMENT '股票代码',
    `trade_date`   date               DEFAULT NULL COMMENT '交易日期',
    `close`        double             DEFAULT NULL COMMENT '周收盘价',
    `open`         double             DEFAULT NULL COMMENT '周开盘价',
    `high`         double             DEFAULT NULL COMMENT '周最高价',
    `low`          double             DEFAULT NULL COMMENT '周最低价',
    `pre_close`    double             DEFAULT NULL COMMENT '上一周收盘价',
    `change`       double             DEFAULT NULL COMMENT '周涨跌额',
    `pct_chg`      double             DEFAULT NULL COMMENT '周涨跌幅 （未复权，如果是复权请用 通用行情接口 ）',
    `vol`          double             DEFAULT NULL COMMENT '周成交量',
    `amount`       double             DEFAULT NULL COMMENT '周成交额',
    `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='沪深股票-行情数据-A股周线行情';
