-- stock.disclosure_date definition

DROP TABLE IF EXISTS `disclosure_date`;
CREATE TABLE `disclosure_date`
(
    `id`           bigint    NOT NULL AUTO_INCREMENT COMMENT '主键',
    `ts_code`      varchar(16)        DEFAULT NULL COMMENT 'TS代码',
    `ann_date`     int               DEFAULT NULL COMMENT '最新披露公告日',
    `end_date`     int               DEFAULT NULL COMMENT '报告期',
    `pre_date`     int               DEFAULT NULL COMMENT '预计披露日期',
    `actual_date`  int               DEFAULT NULL COMMENT '实际披露日期',
    `modify_date`  varchar(64)        DEFAULT NULL COMMENT '披露日期修正记录',
    `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='沪深股票-财务数据-财报披露计划';
