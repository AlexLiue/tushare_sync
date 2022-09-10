-- stock.name_change definition

DROP TABLE IF EXISTS `name_change`;
CREATE TABLE `name_change`
(
    `id`            bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
    `ts_code`       varchar(16) DEFAULT NULL COMMENT 'TS代码',
    `name`          varchar(32) DEFAULT NULL COMMENT '证券名称',
    `start_date`    date        DEFAULT NULL COMMENT '开始日期',
    `end_date`      date        DEFAULT NULL COMMENT '结束日期',
    `ann_date`      date        DEFAULT NULL COMMENT '公告日期',
    `change_reason` varchar(64) DEFAULT NULL COMMENT '变更原因',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='股票曾用名';