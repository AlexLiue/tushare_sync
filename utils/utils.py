"""
数据同步共享函数定义
1. 提供配置信息加载函数
1. 提供数据库 Engine or Connection 对象创建函数
2. 提供 tushare DataApi 对象函数
"""

import configparser
import datetime
import logging
import os
import time

import pymysql
import tushare as ts
from sqlalchemy import create_engine


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


# 构建 Tushare 查询 API 接口对象
def get_tushare_api():
    cfg = get_cfg()
    token = cfg['tushare']['token']
    return ts.pro_api(token=token, timeout=300)


# 获取日志文件打印输出对象
def get_logger(log_name, file_name):
    cfg = get_cfg()
    log_level = cfg['logging']['level']
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)
    if file_name != '':
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../tables', 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        handler = logging.FileHandler(os.path.join(log_dir, file_name),
                                      encoding='utf-8')
        file_fmt = '[%(asctime)s] [%(levelname)s] [ %(filename)s:%(lineno)s - %(name)s ] %(message)s '
        formatter = logging.Formatter(file_fmt)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger



def exec_mysql_sql(sql):
    cfg = get_cfg()
    db = pymysql.connect(host=cfg['mysql']['host'],
                         port=int(cfg['mysql']['port']),
                         user=cfg['mysql']['user'],
                         passwd=cfg['mysql']['password'],
                         db=cfg['mysql']['database'],
                         charset='utf8')
    cursor = db.cursor()
    cursor.execute(sql + ';')
    cursor.close()
    db.close()

# 执行 SQL 脚本
def exec_mysql_script(script_dir):
    cfg = get_cfg()
    logger = get_logger(str(script_dir).split('/')[-1], cfg['logging']['filename'])
    db = pymysql.connect(host=cfg['mysql']['host'],
                         port=int(cfg['mysql']['port']),
                         user=cfg['mysql']['user'],
                         passwd=cfg['mysql']['password'],
                         db=cfg['mysql']['database'],
                         charset='utf8')
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
                        str1 = str1 + ' '.join(line.strip().split())  # pymysql一次只能执行一条sql语句
                file_object.close()  # 循环读取文件时关闭文件很重要，否则会引起bug
    for command in str1.split(';'):
        if command:
            try:
                logger.info('Execute SQL [%s]' % command)
                cursor.execute(command + ';')
                count = count + 1
                suc_cnt = suc_cnt + 1
            except db.DatabaseError as e:
                print(e)
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


# fields 字段列表
#
def exec_sync(table_name, api_name, fields, start_date, end_date, date_step, limit, interval):
    """
    执行数据同步并存储
    :param table_name: 表名
    :param api_name: API 名
    :param fields: 字段列表
    :param start_date: 开始时间
    :param end_date: 结束时间
    :param date_step: 分段查询间隔, 由于 Tushare 分页查询存在性能瓶颈, 因此采用按时间分段拆分微批查询
    :param limit: 每次查询的记录条数
    :param interval: 每次查询的时间间隔
    :param clean_sql: 数据存储前数据清理SQL
    :return: None
    """
    # 创建 API / Connection / Logger 对象
    ts_api = get_tushare_api()
    connection = get_mock_connection()
    logger = get_logger(table_name, 'data_syn.log')

    # 清理历史数据
    clean_sql="DELETE FROM %s WHERE trade_date>='%s' AND trade_date<='%s'" % (table_name, start_date, end_date)
    logger.info('Execute Clean SQL [%s]' % clean_sql)
    exec_mysql_sql(clean_sql)

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
                        " from offset[%d] limit[%d]" % (table_name, api_name, start_date, end_date, offset, limit))

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
                logger.info('Write [%d] records into table [%s] with [%s]' % (size, table_name, connection.engine))
                data.to_sql(table_name, connection, index=False, if_exists='append', chunksize=limit)
                offset = offset + size
                if size < limit:
                    break
            else:
                break
        # 更新下一次微批时间段
        step_start = step_start + datetime.timedelta(date_step)
        step_end = min_date(step_end + datetime.timedelta(date_step), end)


if __name__ == '__main__':
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data_syn', 'trade_cal')
    exec_mysql_script(dir_path)
