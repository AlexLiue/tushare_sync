-- stock.ggt_top10 definition

DROP TABLE IF EXISTS `ggt_top10`;
CREATE TABLE `ggt_top10`
(
    `id`            bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
    `trade_date`    date        DEFAULT NULL COMMENT '交易日期',
    `ts_code`       varchar(16) DEFAULT NULL COMMENT '股票代码',
    `name`          varchar(32) DEFAULT NULL COMMENT '股票名称',
    `close`         double      DEFAULT NULL COMMENT '收盘价',
    `p_change`      double      DEFAULT NULL COMMENT '涨跌幅',
    `rank`          int         DEFAULT NULL COMMENT '资金排名',
    `market_type`   int         DEFAULT NULL COMMENT '市场类型 2：港股通（沪） 4：港股通（深）',
    `amount`        double      DEFAULT NULL COMMENT '累计成交金额',
    `net_amount`    double      DEFAULT NULL COMMENT '净买入金额',
    `sh_amount`     double      DEFAULT NULL COMMENT '沪市成交金额',
    `sh_net_amount` double      DEFAULT NULL COMMENT '沪市净买入金额',
    `sh_buy`        double      DEFAULT NULL COMMENT '沪市买入金额',
    `sh_sell`       double      DEFAULT NULL COMMENT '沪市卖出金额',
    `sz_amount`     double      DEFAULT NULL COMMENT '深市成交金额',
    `sz_net_amount` double      DEFAULT NULL COMMENT '深市净买入金额',
    `sz_buy`        double      DEFAULT NULL COMMENT '深市买入金额',
    `sz_sell`       double      DEFAULT NULL COMMENT '深市卖出金额',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='沪深股票-行情数据-港股通十大成交股';