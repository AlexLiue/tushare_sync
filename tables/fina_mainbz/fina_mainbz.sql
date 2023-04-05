-- stock.fina_mainbz definition

DROP TABLE IF EXISTS `fina_mainbz`;
CREATE TABLE `fina_mainbz`
(
    `ts_code`      varchar(16)        DEFAULT NULL COMMENT 'TS代码',
    `end_date`     int                DEFAULT NULL COMMENT '报告期',
    `bz_item`      varchar(64)        DEFAULT NULL COMMENT '主营业务项目',
    `bz_code`      varchar(16)        DEFAULT NULL COMMENT '项目代码',
    `bz_sales`     double             DEFAULT NULL COMMENT '主营业务收入(元)',
    `bz_profit`    double             DEFAULT NULL COMMENT '主营业务利润(元)',
    `bz_cost`      double             DEFAULT NULL COMMENT '主营业务成本(元)',
    `curr_type`    varchar(16)        DEFAULT NULL COMMENT '货币代码',
    `update_flag`  varchar(2)         DEFAULT NULL COMMENT '是否更新',
    `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
     KEY `fina_mainbz_ts_code` (`ts_code`, `end_date`) USING BTREE,
     KEY `fina_mainbz_end_date` (`end_date`, `ts_code`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT ='沪深股票-财务数据-主营业务构成';
