-- stock.forecast definition

DROP TABLE IF EXISTS `forecast`;
CREATE TABLE `forecast`
(
    `ts_code`         varchar(16)        DEFAULT NULL COMMENT 'TS股票代码',
    `ann_date`        int                DEFAULT NULL COMMENT '公告日期',
    `end_date`        int                DEFAULT NULL COMMENT '报告期',
    `type`            varchar(16)        DEFAULT NULL COMMENT '业绩预告类型',
    `p_change_min`    double             DEFAULT NULL COMMENT '预告净利润变动幅度下限（%）',
    `p_change_max`    double             DEFAULT NULL COMMENT '预告净利润变动幅度上限（%）',
    `net_profit_min`  double             DEFAULT NULL COMMENT '预告净利润下限（万元）',
    `net_profit_max`  double             DEFAULT NULL COMMENT '预告净利润上限（万元）',
    `last_parent_net` double             DEFAULT NULL COMMENT '上年同期归属母公司净利润',
    `notice_times`    int                DEFAULT NULL COMMENT '公布次数',
    `first_ann_date`  int                DEFAULT NULL COMMENT '首次公告日',
    `summary`         text COMMENT '业绩预告摘要',
    `change_reason`   text COMMENT '业绩变动原因',
    `created_time`    timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time`    timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
     KEY `forecast_ts_code` (`ts_code`, `ann_date`) USING BTREE,
     KEY `forecast_ann_date` (`ann_date`, `ts_code`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT ='沪深股票-财务数据-业绩预告';
