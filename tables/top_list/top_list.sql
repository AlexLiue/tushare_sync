-- stock.top_list definition

DROP TABLE IF EXISTS `top_list`;
CREATE TABLE `top_list`
(
    `id`            bigint    NOT NULL AUTO_INCREMENT COMMENT '主键',
    `trade_date`    date               DEFAULT NULL COMMENT '交易日期',
    `ts_code`       varchar(16)        DEFAULT NULL COMMENT 'TS代码',
    `name`          varchar(64)        DEFAULT NULL COMMENT '股票名称',
    `close`         double             DEFAULT NULL COMMENT '收盘价',
    `pct_change`    double             DEFAULT NULL COMMENT '涨跌幅',
    `turnover_rate` double             DEFAULT NULL COMMENT '换手率',
    `amount`        double             DEFAULT NULL COMMENT '总成交额',
    `l_sell`        double             DEFAULT NULL COMMENT '龙虎榜卖出额',
    `l_buy`         double             DEFAULT NULL COMMENT '龙虎榜买入额',
    `l_amount`      double             DEFAULT NULL COMMENT '龙虎榜成交额',
    `net_amount`    double             DEFAULT NULL COMMENT '龙虎榜净买入额',
    `net_rate`      double             DEFAULT NULL COMMENT '龙虎榜净买额占比',
    `amount_rate`   double             DEFAULT NULL COMMENT '龙虎榜成交额占比',
    `float_values`  double             DEFAULT NULL COMMENT '当日流通市值',
    `reason`        text COMMENT '上榜理由',
    `created_time`  timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time`  timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='沪深股票-市场参考数据-龙虎榜每日明细';