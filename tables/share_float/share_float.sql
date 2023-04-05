-- stock.share_float definition

DROP TABLE IF EXISTS `share_float`;
CREATE TABLE `share_float`
(
    `ts_code`      varchar(16)        DEFAULT NULL COMMENT 'TS代码',
    `ann_date`     int                DEFAULT NULL COMMENT '公告日期',
    `float_date`   int                DEFAULT NULL COMMENT '解禁日期',
    `float_share`  double             DEFAULT NULL COMMENT '流通股份',
    `float_ratio`  double             DEFAULT NULL COMMENT '流通股份占总股本比率',
    `holder_name`  varchar(64)        DEFAULT NULL COMMENT '股东名称',
    `share_type`   varchar(32)        DEFAULT NULL COMMENT '股份类型',
    `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
     KEY `share_float_ts_code` (`ts_code`, `ann_date`) USING BTREE,
     KEY `share_float_ann_date` (`ann_date`, `ts_code`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT ='沪深股票-市场参考数据-限售股解禁';