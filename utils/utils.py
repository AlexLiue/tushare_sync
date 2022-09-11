"""
数据同步共享函数定义
1. 提供配置信息加载函数
1. 提供数据库 Engine or Connection 对象创建函数
2. 提供 tushare DataApi 对象函数
"""

import configparser
import logging
import os

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
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        handler = logging.FileHandler(os.path.join(log_dir, file_name),
                                      encoding='utf-8')
        file_fmt = '[%(asctime)s] [%(levelname)s] [ %(filename)s:%(lineno)s - %(name)s ] %(message)s '
        formatter = logging.Formatter(file_fmt)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


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
    if flt_cnt > 0:
        raise Exception('Execute SQL script [%s] failed. ' % script_dir)


if __name__ == '__main__':
    dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data_syn', 'trade_cal')
    exec_mysql_script(dir_path)
