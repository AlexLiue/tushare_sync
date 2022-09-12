-- stock.stock_basic definition


DROP TABLE IF EXISTS `stock_basic`;
CREATE TABLE `stock_basic`
(
    `id`           bigint    NOT NULL AUTO_INCREMENT COMMENT ' 主键 ',
    `ts_code`      varchar(16)                                                   DEFAULT NULL COMMENT ' TS代码 ',
    `symbol`       varchar(16)                                                   DEFAULT NULL COMMENT ' 股票代码 ',
    `name`         varchar(64)                                                   DEFAULT NULL COMMENT ' 股票名称 ',
    `area`         varchar(32)                                                   DEFAULT NULL COMMENT ' 地域 ',
    `industry`     varchar(32)                                                   DEFAULT NULL COMMENT ' 所属行业 ',
    `fullname`     varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci  DEFAULT NULL COMMENT ' 股票全称 ',
    `enname`       varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT ' 英文全称 ',
    `cnspell`      varchar(32)                                                   DEFAULT NULL COMMENT ' 拼音缩写 ',
    `market`       varchar(32)                                                   DEFAULT NULL COMMENT ' 市场类型:主板/创业板/科创板/CDR',
    `exchange`     varchar(32)                                                   DEFAULT NULL COMMENT ' 交易所代码 ',
    `curr_type`    varchar(32)                                                   DEFAULT NULL COMMENT ' 交易货币 ',
    `list_status`  varchar(32)                                                   DEFAULT NULL COMMENT ' 上市状态 L上市 D退市 P暂停上市 ',
    `list_date`    date                                                          DEFAULT NULL COMMENT ' 上市日期 ',
    `delist_date`  date                                                          DEFAULT NULL COMMENT ' 退市日期 ',
    `is_hs`        varchar(32)                                                   DEFAULT NULL COMMENT ' 是否沪深港通标:N否 H沪股通 S深股通 ',
    `created_time` timestamp NOT NULL                                            DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time` timestamp NOT NULL                                            DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4902 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='基础信息';



