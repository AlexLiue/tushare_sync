-- stock.repurchase definition

DROP TABLE IF EXISTS `repurchase`;
CREATE TABLE `repurchase`
(
    `ts_code`      varchar(16)        DEFAULT NULL COMMENT 'TS代码',
    `ann_date`     int                DEFAULT NULL COMMENT '公告日期',
    `end_date`     int                DEFAULT NULL COMMENT '截止日期',
    `proc`         varchar(32)        DEFAULT NULL COMMENT '进度',
    `exp_date`     int                DEFAULT NULL COMMENT '过期日期',
    `vol`          double             DEFAULT NULL COMMENT '回购数量',
    `amount`       double             DEFAULT NULL COMMENT '回购金额',
    `high_limit`   double             DEFAULT NULL COMMENT '回购最高价',
    `low_limit`    double             DEFAULT NULL COMMENT '回购最低价',
    `repo_goal`    varchar(64)        DEFAULT NULL COMMENT '回购目的',
    `update_flag`  varchar(2)         DEFAULT NULL COMMENT '更新标识',
    `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
     KEY `repurchase_ts_code` (`ts_code`, `ann_date`) USING BTREE,
     KEY `repurchase_ann_date` (`ann_date`, `ts_code`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT ='沪深股票-市场参考数据-股票回购';