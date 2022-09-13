-- stock.cyq_perf definition

DROP TABLE IF EXISTS `cyq_perf`;
CREATE TABLE `cyq_perf`
(
    `id`           bigint    NOT NULL AUTO_INCREMENT COMMENT '主键',
    `ts_code`      varchar(16)        DEFAULT NULL COMMENT '股票代码',
    `trade_date`   date               DEFAULT NULL COMMENT '交易日期',
    `his_low`      double             DEFAULT NULL COMMENT '历史最低价',
    `his_high`     double             DEFAULT NULL COMMENT '历史最高价',
    `cost_5pct`    double             DEFAULT NULL COMMENT '5分位成本',
    `cost_15pct`   double             DEFAULT NULL COMMENT '15分位成本',
    `cost_50pct`   double             DEFAULT NULL COMMENT '50分位成本',
    `cost_85pct`   double             DEFAULT NULL COMMENT '85分位成本',
    `cost_95pct`   double             DEFAULT NULL COMMENT '95分位成本',
    `weight_avg`   double             DEFAULT NULL COMMENT '加权平均成本',
    `winner_rate`  double             DEFAULT NULL COMMENT '胜率',
    `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='沪深股票-特色数据-每日筹码及胜率';
