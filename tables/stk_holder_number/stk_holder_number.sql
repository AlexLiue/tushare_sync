-- stock.stk_holder_number definition

DROP TABLE IF EXISTS `stk_holder_number`;
CREATE TABLE `stk_holder_number`
(
    `ts_code`      varchar(16)        DEFAULT NULL COMMENT 'TS股票代码',
    `ann_date`     int                DEFAULT NULL COMMENT '公告日期',
    `end_date`     int                DEFAULT NULL COMMENT '截止日期',
    `holder_nums`  int                DEFAULT NULL COMMENT '股东户数',
    `holder_num`   int                DEFAULT NULL COMMENT '股东总户数（A+B）',
    `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
     KEY `stk_holder_number_ts_code` (`ts_code`, `ann_date`) USING BTREE,
     KEY `stk_holder_number_ann_date` (`ann_date`, `ts_code`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT ='沪深股票-市场参考数据-股东人数';
