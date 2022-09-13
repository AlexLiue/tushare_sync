-- stock.concept definition

DROP TABLE IF EXISTS `concept`;
CREATE TABLE `concept`
(
    `id`           bigint    NOT NULL AUTO_INCREMENT COMMENT '主键',
    `code`         varchar(8)         DEFAULT NULL COMMENT '概念分类ID',
    `name`         varchar(32)        DEFAULT NULL COMMENT '概念分类名称',
    `src`          varchar(4)         DEFAULT NULL COMMENT '来源',
    `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='沪深股票-市场参考数据-概念股分类（已经停止维护）';
