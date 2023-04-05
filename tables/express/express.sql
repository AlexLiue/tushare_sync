-- stock.express definition

DROP TABLE IF EXISTS `express`;
CREATE TABLE `express`
(
    `ts_code`                    varchar(16)        DEFAULT NULL COMMENT 'TS股票代码',
    `ann_date`                   int                DEFAULT NULL COMMENT '公告日期',
    `end_date`                   int                DEFAULT NULL COMMENT '报告期',
    `revenue`                    double             DEFAULT NULL COMMENT '营业收入(元)',
    `operate_profit`             double             DEFAULT NULL COMMENT '营业利润(元)',
    `total_profit`               double             DEFAULT NULL COMMENT '利润总额(元)',
    `n_income`                   double             DEFAULT NULL COMMENT '净利润(元)',
    `total_assets`               double             DEFAULT NULL COMMENT '总资产(元)',
    `total_hldr_eqy_exc_min_int` double             DEFAULT NULL COMMENT '股东权益合计(不含少数股东权益)(元)',
    `diluted_eps`                double             DEFAULT NULL COMMENT '每股收益(摊薄)(元)',
    `diluted_roe`                double             DEFAULT NULL COMMENT '净资产收益率(摊薄)(%)',
    `yoy_net_profit`             double             DEFAULT NULL COMMENT '去年同期修正后净利润',
    `bps`                        double             DEFAULT NULL COMMENT '每股净资产',
    `yoy_sales`                  double             DEFAULT NULL COMMENT '同比增长率:营业收入',
    `yoy_op`                     double             DEFAULT NULL COMMENT '同比增长率:营业利润',
    `yoy_tp`                     double             DEFAULT NULL COMMENT '同比增长率:利润总额',
    `yoy_dedu_np`                double             DEFAULT NULL COMMENT '同比增长率:归属母公司股东的净利润',
    `yoy_eps`                    double             DEFAULT NULL COMMENT '同比增长率:基本每股收益',
    `yoy_roe`                    double             DEFAULT NULL COMMENT '同比增减:加权平均净资产收益率',
    `growth_assets`              double             DEFAULT NULL COMMENT '比年初增长率:总资产',
    `yoy_equity`                 double             DEFAULT NULL COMMENT '比年初增长率:归属母公司的股东权益',
    `growth_bps`                 double             DEFAULT NULL COMMENT '比年初增长率:归属于母公司股东的每股净资产',
    `or_last_year`               double             DEFAULT NULL COMMENT '去年同期营业收入',
    `op_last_year`               double             DEFAULT NULL COMMENT '去年同期营业利润',
    `tp_last_year`               double             DEFAULT NULL COMMENT '去年同期利润总额',
    `np_last_year`               double             DEFAULT NULL COMMENT '去年同期净利润',
    `eps_last_year`              double             DEFAULT NULL COMMENT '去年同期每股收益',
    `open_net_assets`            double             DEFAULT NULL COMMENT '期初净资产',
    `open_bps`                   double             DEFAULT NULL COMMENT '期初每股净资产',
    `perf_summary`               text COMMENT '业绩简要说明',
    `is_audit`                   varchar(16)        DEFAULT NULL COMMENT '是否审计： 1是 0否',
    `remark`                     text COMMENT '备注',
    `created_time`               timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_time`               timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
     KEY `express_ts_code` (`ts_code`, `ann_date`) USING BTREE,
     KEY `express_ann_date` (`ann_date`, `ts_code`) USING BTREE
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_0900_ai_ci COMMENT ='沪深股票-财务数据-业绩快报';
