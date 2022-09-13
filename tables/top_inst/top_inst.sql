-- stock.top_inst definition

CREATE TABLE `top_inst`
(
    `id`           bigint    NOT NULL AUTO_INCREMENT COMMENT '主键',
    `trade_date`   date               DEFAULT NULL COMMENT '交易日期',
    `ts_code`      varchar(16)        DEFAULT NULL COMMENT 'TS代码',
    `exalter`      varchar(64)        DEFAULT NULL COMMENT '营业部名称',
    `buy`          double             DEFAULT NULL COMMENT '买入额（万）',
    `buy_rate`     double             DEFAULT NULL COMMENT '买入占总成交比例',
    `sell`         double             DEFAULT NULL COMMENT '卖出额（万）',
    `sell_rate`    double             DEFAULT NULL COMMENT '卖出占总成交比例',
    `net_buy`      double             DEFAULT NULL COMMENT '净成交额（万）',
    `side`         varchar(2)         DEFAULT NULL COMMENT '买卖类型0买入1卖出',
    `reason`       text,
    `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='沪深股票-市场参考数据-龙虎榜机构明细';