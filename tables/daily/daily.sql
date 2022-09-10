-- stock.daily definition

DROP TABLE IF EXISTS `daily`;
CREATE TABLE `daily`
(
    `id`         bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
    `ts_code`    varchar(16) DEFAULT NULL COMMENT '股票代码',
    `trade_date` date        DEFAULT NULL COMMENT '交易日期',
    `open`       double      DEFAULT NULL COMMENT '开盘价',
    `high`       double      DEFAULT NULL COMMENT '最高价',
    `low`        double      DEFAULT NULL COMMENT '最低价',
    `close`      double      DEFAULT NULL COMMENT '收盘价',
    `pre_close`  double      DEFAULT NULL COMMENT '昨收价(前复权)',
    `change`     double      DEFAULT NULL COMMENT '涨跌额',
    `pct_chg`    double      DEFAULT NULL COMMENT '涨跌幅 （未复权）',
    `vol`        double      DEFAULT NULL COMMENT '成交量 （手）',
    `amount`     double      DEFAULT NULL COMMENT '成交额 （千元）',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='A股日线行情';
