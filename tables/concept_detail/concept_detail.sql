-- stock.concept_detail definition


DROP TABLE IF EXISTS `concept_detail`;
CREATE TABLE `concept_detail`
(
    `code`         varchar(8)         DEFAULT NULL COMMENT '概念代码',
    `concept_name` varchar(32)        DEFAULT NULL COMMENT '概念名称',
    `ts_code`      varchar(16)        DEFAULT NULL COMMENT '股票代码',
    `name`         varchar(64)        DEFAULT NULL COMMENT '股票名称',
    `in_date`      int                DEFAULT NULL COMMENT '纳入日期',
    `out_date`     int                DEFAULT NULL COMMENT '剔除日期',
    `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
     KEY `concept_detail` (`code`, `concept_name`) USING BTREE,
     KEY `concept_detail` (`concept_name`, `code`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT ='沪深股票-市场参考数据-概念股列表 （已经停止维护）';
