"""
数据同步共享函数定义
1. 提供配置信息加载函数
1. 提供数据库 Engine or Connection 对象创建函数
2. 提供 tushare DataApi 对象函数
"""

import configparser
import datetime
import os
import pymysql
import tushare as ts
from sqlalchemy import create_engine
import logging
import time


# 加载配置信息函数
def get_cfg():
    cfg = configparser.ConfigParser()
    file_name = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../application.ini'))
    cfg.read(file_name)
    return cfg


# 获取 MySQL Connection 对象
def get_mock_connection():
    cfg = get_cfg()
    db_host = cfg['mysql']['host']
    db_user = cfg['mysql']['user']
    db_password = cfg['mysql']['password']
    db_port = cfg['mysql']['port']
    db_database = cfg['mysql']['database']
    db_url = 'mysql://%s:%s@%s:%s/%s?charset=utf8&use_unicode=1' % (db_user, db_password, db_host, db_port, db_database)
    return create_engine(db_url)


def get_mysql_connection():
    cfg = get_cfg()
    return pymysql.connect(host=cfg['mysql']['host'],
                           port=int(cfg['mysql']['port']),
                           user=cfg['mysql']['user'],
                           passwd=cfg['mysql']['password'],
                           db=cfg['mysql']['database'],
                           charset='utf8')


# 构建 Tushare 查询 API 接口对象
def get_tushare_api():
    cfg = get_cfg()
    token = cfg['tushare']['token']
    return ts.pro_api(token=token, timeout=300)


# 获取日志文件打印输出对象
def get_logger(log_name, file_name):
    cfg = get_cfg()
    log_level = cfg['logging']['level']
    backup_days = int(cfg['logging']['backupDays'])
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
    log_file = os.path.join(log_dir, '%s.%s' % (file_name, str(datetime.datetime.now().strftime('%Y-%m-%d'))))
    if file_name != '':
        if not os.path.exists(log_dir):
            logger.info("Make logger dir [%s]" % str(log_dir))
            os.makedirs(log_dir)
        clen_file = os.path.join(log_dir, 'file_name.%s' %
                                 str((datetime.datetime.now() +
                                      datetime.timedelta(days=-backup_days)).strftime('%Y-%m-%d'))
                                 )

        if os.path.exists(clen_file):
            os.remove(clen_file)
        handler = logging.FileHandler(log_file, encoding='utf-8')
        file_fmt = '[%(asctime)s] [%(levelname)s] [ %(filename)s:%(lineno)s - %(name)s ] %(message)s '
        formatter = logging.Formatter(file_fmt)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.info("Logger File [%s]" % log_file)
    return logger


def exec_mysql_sql(sql):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    counts = cursor.execute(sql + ';')
    conn.commit()
    cursor.close()
    conn.close()
    return counts


# 执行 SQL 脚本
def exec_mysql_script(script_dir):
    cfg = get_cfg()
    logger = get_logger(str(script_dir).split('/')[-1], cfg['logging']['filename'])
    db = get_mysql_connection()
    cursor = db.cursor()
    count = 0
    flt_cnt = 0
    suc_cnt = 0
    str1 = ''
    for home, dirs, files in os.walk(script_dir):
        for filename in files:
            if filename.endswith('.sql'):
                dirname = os.path.dirname(os.path.abspath(__file__))
                fullname = os.path.join(dirname, script_dir, filename)
                file_object = open(fullname)
                for line in file_object:
                    if not line.startswith("--") and not line.startswith('/*'):  # 处理注释
                        str1 = str1 + ' ' + ' '.join(line.strip().split())  # pymysql一次只能执行一条sql语句
                file_object.close()  # 循环读取文件时关闭文件很重要，否则会引起bug
    for commandSQL in str1.split(';'):
        command = commandSQL.strip()
        if command != '':
            try:
                logger.info('Execute SQL [%s]' % command.strip())
                cursor.execute(command.strip() + ';')
                count = count + 1
                suc_cnt = suc_cnt + 1
            except db.DatabaseError as e:
                print(e)
                print(command)
                flt_cnt = flt_cnt + 1
                pass
    logger.info('Execute result: Total [%s], Succeed [%s] , Failed [%s] ' % (count, suc_cnt, flt_cnt))
    cursor.close()
    db.close()
    if flt_cnt > 0:
        raise Exception('Execute SQL script [%s] failed. ' % script_dir)


# 获取两个日期的最小值
def min_date(date1, date2):
    if date1 <= date2:
        return date1
    else:
        return date2


def exec_sync(table_name, api_name, fields, date_column, start_date, end_date, date_step,
              limit, interval, ts_code_mode, ts_code_limit):
    """
    执行数据同步并存储
    :param table_name: 表名
    :param api_name: API 名
    :param fields: 字段列表
    :param date_column: 增量时间字段列
    :param start_date: 开始时间
    :param end_date: 结束时间
    :param date_step: 分段查询间隔, 由于 Tushare 分页查询存在性能瓶颈, 因此采用按时间分段拆分微批查询
    :param limit: 每次查询的记录条数
    :param interval: 每次查询的时间间隔
    :param ts_code_mode: 是否股票代码是否必须为非空, 如果为 true 则需要先查询股票代码, 获取参数
    :param ts_code_limit: 每次同步的 ts_code 的记录数据
    :return: None
    """
    if ts_code_mode == 'false' or ts_code_mode == '':
        exec_sync_without_ts_code(table_name, api_name, fields,
                                  date_column, start_date, end_date, date_step, limit, interval)
    else:
        exec_sync_with_ts_code(table_name, api_name, fields,
                               date_column, start_date, end_date, date_step, limit, interval, ts_code_limit)


def exec_sync_with_ts_code(table_name, api_name, fields, date_column, start_date, end_date, date_step,
                           limit, interval, ts_code_limit):
    # 创建 API / Connection / Logger 对象
    ts_api = get_tushare_api()
    connection = get_mock_connection()
    logger = get_logger(table_name, 'data_syn.log')

    max_retry = 0
    while max_retry < 3:
        try:
            # 清理历史数据
            clean_sql = "DELETE FROM %s WHERE %s>='%s' AND %s<='%s'" % \
                        (table_name, date_column, start_date, date_column, end_date)
            logger.info('Execute Clean SQL [%s]' % clean_sql)
            counts = exec_mysql_sql(clean_sql)
            logger.info("Execute Clean SQL Affect [%d] records" % counts)

            logger.info(
                "Sync table[%s] in ts_code mode start_date[%s] end_date[%s]" % (table_name, start_date, end_date))

            ts_code_offset = 0  # 读取偏移量
            while True:
                logger.info("Query ts_code from tushare with api[stock_basic] from ts_code_offset[%d] ts_code_limit[%d]"
                            % (ts_code_offset, ts_code_limit))
                df_ts_code = ts_api.stock_basic(**{
                    "limit": ts_code_limit,
                    "offset": ts_code_offset
                }, fields=[
                    "ts_code"
                ])
                time.sleep(interval)
                if df_ts_code.last_valid_index() is not None:
                    ts_code = df_ts_code['ts_code'].str.cat(sep=',')
                    logger.info("Current ts_code[%s]" % ts_code)
                    start = datetime.datetime.strptime(start_date, '%Y%m%d')
                    end = datetime.datetime.strptime(end_date, '%Y%m%d')

                    step_start = start  # 微批开始时间
                    step_end = min_date(start + datetime.timedelta(date_step - 1), end)  # 微批结束时间

                    while step_start <= end:
                        start_date = str(step_start.strftime('%Y%m%d'))
                        end_date = str(step_end.strftime('%Y%m%d'))
                        offset = 0
                        while True:
                            logger.info(
                                "Query [%s] from tushare with api[%s] ts_code[%s-%s] start_date[%s] end_date[%s]"
                                " from offset[%d] limit[%d]" % (
                                    table_name, api_name, ts_code_offset, ts_code_offset + ts_code_limit,
                                    start_date, end_date, offset, limit))

                            data = ts_api.query(api_name,
                                                **{
                                                    "ts_code": ts_code,
                                                    "start_date": start_date,
                                                    "end_date": end_date,
                                                    "offset": offset,
                                                    "limit": limit
                                                },
                                                fields=fields)
                            time.sleep(interval)
                            if data.last_valid_index() is not None:
                                size = data.last_valid_index() + 1
                                logger.info(
                                    'Write [%d] records into table [%s] with [%s]' % (
                                        size, table_name, connection.engine))
                                data.to_sql(table_name, connection, index=False, if_exists='append', chunksize=limit)
                                offset = offset + size
                                if size < limit:
                                    break
                            else:
                                break
                        # 更新下一次微批时间段
                        step_start = step_start + datetime.timedelta(date_step)
                        step_end = min_date(step_end + datetime.timedelta(date_step), end)
                    ts_code_offset = ts_code_offset + df_ts_code.last_valid_index() + 1
                else:
                    break

            break
        except Exception as e:
            logger.error("Get Exception[%s]" % e.__cause__)
            time.sleep(3)
        max_retry += 1


# fields 字段列表
def exec_sync_without_ts_code(table_name, api_name, fields,
                              date_column, start_date, end_date, date_step, limit, interval):
    """
    执行数据同步并存储
    :param table_name: 表名
    :param api_name: API 名
    :param fields: 字段列表
    :param date_column: 增量时间字段列
    :param start_date: 开始时间
    :param end_date: 结束时间
    :param date_step: 分段查询间隔, 由于 Tushare 分页查询存在性能瓶颈, 因此采用按时间分段拆分微批查询
    :param limit: 每次查询的记录条数
    :param interval: 每次查询的时间间隔
    :return: None
    """

    # 创建 API / Connection / Logger 对象
    ts_api = get_tushare_api()
    connection = get_mock_connection()
    logger = get_logger(table_name, 'data_syn.log')

    max_retry = 0
    while max_retry < 3:
        try:
            # 清理历史数据
            clean_sql = "DELETE FROM %s WHERE %s>='%s' AND %s<='%s'" % \
                        (table_name, date_column, start_date, date_column, end_date)
            logger.info('Execute Clean SQL [%s]' % clean_sql)
            counts = exec_mysql_sql(clean_sql)
            logger.info("Execute Clean SQL Affect [%d] records" % counts)

            # 数据同步时间开始时间和结束时间, 包含前后边界
            start = datetime.datetime.strptime(start_date, '%Y%m%d')
            end = datetime.datetime.strptime(end_date, '%Y%m%d')

            step_start = start  # 微批开始时间
            step_end = min_date(start + datetime.timedelta(date_step - 1), end)  # 微批结束时间

            while step_start <= end:
                start_date = str(step_start.strftime('%Y%m%d'))
                end_date = str(step_end.strftime('%Y%m%d'))
                offset = 0
                while True:
                    logger.info("Query [%s] from tushare with api[%s] start_date[%s] end_date[%s]"
                                " from offset[%d] limit[%d]" % (
                                    table_name, api_name, start_date, end_date, offset, limit))

                    data = ts_api.query(api_name,
                                        **{
                                            "start_date": start_date,
                                            "end_date": end_date,
                                            "offset": offset,
                                            "limit": limit
                                        },
                                        fields=fields)
                    time.sleep(interval)
                    if data.last_valid_index() is not None:
                        size = data.last_valid_index() + 1
                        logger.info(
                            'Write [%d] records into table [%s] with [%s]' % (size, table_name, connection.engine))
                        data.to_sql(table_name, connection, index=False, if_exists='append', chunksize=limit)
                        offset = offset + size
                        if size < limit:
                            break
                    else:
                        break
                # 更新下一次微批时间段
                step_start = step_start + datetime.timedelta(date_step)
                step_end = min_date(step_end + datetime.timedelta(date_step), end)
            break
        except Exception as e:
            logger.error("Get Exception[%s]" % e.__cause__)
            time.sleep(3)
        max_retry += 1


# fields 字段列表
#
def exec_sync_with_spec_date_column(table_name, api_name, fields, date_column,
                                    start_date, end_date, limit, interval):
    """
    执行数据同步并存储-基于 trade_date 字段
    :param table_name: 表名
    :param api_name: API 名
    :param fields: 字段列表
    :param date_column: 增量时间字段列
    :param start_date: 开始时间
    :param end_date: 结束时间
    :param limit: 每次查询的记录条数
    :param interval: 每次查询的时间间隔
    :return: None
    """

    # 创建 API / Connection / Logger 对象
    ts_api = get_tushare_api()
    connection = get_mock_connection()
    logger = get_logger(table_name, 'data_syn.log')

    max_retry = 0
    while max_retry < 3:
        try:
            # 清理历史数据
            clean_sql = "DELETE FROM %s WHERE %s>='%s' AND %s<='%s'" % \
                        (table_name, date_column, start_date, date_column, end_date)
            logger.info('Execute Clean SQL [%s]' % clean_sql)
            counts = exec_mysql_sql(clean_sql)
            logger.info("Execute Clean SQL Affect [%d] records" % counts)

            # 数据同步时间开始时间和结束时间, 包含前后边界
            start = datetime.datetime.strptime(start_date, '%Y%m%d')
            end = datetime.datetime.strptime(end_date, '%Y%m%d')

            step = start  # 微批开始时间

            while step <= end:
                step_date = str(step.strftime('%Y%m%d'))
                offset = 0
                while True:
                    logger.info("Query [%s] from tushare with api[%s] %s[%s]"
                                " from offset[%d] limit[%d]" % (
                                    table_name, api_name, date_column, step_date, offset, limit))
                    data = ts_api.query(api_name,
                                        **{
                                            date_column: step_date,
                                            "offset": offset,
                                            "limit": limit
                                        },
                                        fields=fields)
                    time.sleep(interval)
                    if data.last_valid_index() is not None:
                        size = data.last_valid_index() + 1
                        logger.info(
                            'Write [%d] records into table [%s] with [%s]' % (size, table_name, connection.engine))
                        data.to_sql(table_name, connection, index=False, if_exists='append', chunksize=limit)
                        offset = offset + size
                        if size < limit:
                            break
                    else:
                        break
                # 更新下一次微批时间段
                step = step + datetime.timedelta(days=1)
            break
        except Exception as e:
            logger.error("Get Exception[%s]" % e.__cause__)
            time.sleep(3)
        max_retry += 1


if __name__ == '__main__':
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data_syn', 'trade_cal')
    exec_mysql_script(dir_path)
