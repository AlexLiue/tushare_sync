-- stock.bak_basic definition

DROP TABLE IF EXISTS `bak_basic`;
CREATE TABLE `bak_basic`
(
    `id`                bigint    NOT NULL AUTO_INCREMENT COMMENT '主键',
    `trade_date`        date               DEFAULT NULL COMMENT '交易日期',
    `ts_code`           varchar(16)        DEFAULT NULL COMMENT 'TS股票代码',
    `name`              varchar(64)        DEFAULT NULL COMMENT '股票名称',
    `industry`          varchar(32)        DEFAULT NULL COMMENT '所属行业',
    `area`              varchar(32)        DEFAULT NULL COMMENT '地域',
    `pe`                double             DEFAULT NULL COMMENT '市盈率（动）',
    `float_share`       double             DEFAULT NULL COMMENT '流通股本（亿）',
    `total_share`       double             DEFAULT NULL COMMENT '总股本（亿）',
    `total_assets`      double             DEFAULT NULL COMMENT '总资产（亿）',
    `liquid_assets`     double             DEFAULT NULL COMMENT '流动资产（亿）',
    `fixed_assets`      double             DEFAULT NULL COMMENT '固定资产（亿）',
    `reserved`          double             DEFAULT NULL COMMENT '公积金',
    `reserved_pershare` double             DEFAULT NULL COMMENT '每股公积金',
    `eps`               double             DEFAULT NULL COMMENT '每股收益',
    `bvps`              double             DEFAULT NULL COMMENT '每股净资产',
    `pb`                double             DEFAULT NULL COMMENT '市净率',
    `list_date`         date               DEFAULT NULL COMMENT '上市日期',
    `undp`              double             DEFAULT NULL COMMENT '未分配利润',
    `per_undp`          double             DEFAULT NULL COMMENT '每股未分配利润',
    `rev_yoy`           double             DEFAULT NULL COMMENT '收入同比（%）',
    `profit_yoy`        double             DEFAULT NULL COMMENT '利润同比（%）',
    `gpr`               double             DEFAULT NULL COMMENT '毛利率（%）',
    `npr`               double             DEFAULT NULL COMMENT '净利润率（%）',
    `holder_num`        int                DEFAULT NULL COMMENT '股东人数',
    `created_time`      timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time`      timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='备用列表';
