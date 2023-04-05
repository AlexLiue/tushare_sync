-- stock.stk_rewards definition

DROP TABLE IF EXISTS `stk_rewards`;
CREATE TABLE `stk_rewards`
(
    `ts_code`      varchar(16)        DEFAULT NULL COMMENT 'TS股票代码',
    `ann_date`     int                DEFAULT NULL COMMENT '公告日期',
    `end_date`     int                DEFAULT NULL COMMENT '截止日期',
    `name`         varchar(64)        DEFAULT NULL COMMENT '姓名',
    `title`        varchar(64)        DEFAULT NULL COMMENT '职务',
    `reward`       double             DEFAULT NULL COMMENT '报酬',
    `hold_vol`     double             DEFAULT NULL COMMENT '持股数',
    `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
     KEY `stk_rewards_ts_code` (`ts_code`, `ann_date`) USING BTREE,
     KEY `stk_rewards_ann_date` (`ann_date`, `ts_code`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT ='管理层薪酬和持股';