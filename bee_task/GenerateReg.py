import pymysql
import logging
import sys
import re
import uuid
import time
import random
import traceback
import math
from logging.handlers import TimedRotatingFileHandler


class GenerateReg(object):
    def __init__(self):
        # 初始化数据库
        # 数仓数据库
        self.db = pymysql.connect(host="47.101.147.20", port=3306, user="root", password="Big!!!data111",
                                  db="dm_report", charset="utf8")
        # 业务系统
        self.business_db = pymysql.connect(host="172.19.200.63", port=3306, user="bigdata", password="6yhn7UJM",
                                           db="loan_market", charset="utf8")

        # 初始化log
        log_fmt = '%(asctime)s\tFile \"%(filename)s\",line %(lineno)s\t%(levelname)s: %(message)s'
        formatter = logging.Formatter(log_fmt)

        # 控制台log配置
        # 默认是sys.stderr
        log_console_handler = logging.StreamHandler(sys.stdout)
        log_console_handler.setLevel(logging.INFO)
        log_console_handler.setFormatter(formatter)

        # 文件log配置
        log_file_handler = TimedRotatingFileHandler(filename="generateReg.log", when="D", interval=1, backupCount=7, encoding='utf-8')
        log_file_handler.setLevel(logging.INFO)
        log_file_handler.setFormatter(formatter)
        log_file_handler.suffix = "%Y-%m-%d_%H-%M"
        log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}$")

        # log初始化
        self.log = logging.getLogger()
        self.log.setLevel(logging.INFO)
        self.log.addHandler(log_file_handler)
        self.log.addHandler(log_console_handler)

    def get_user(self, num=0):
        b_cursor = self.business_db.cursor()
        b_cursor.execute("select max(customer_id) from customer_info where register_channel = 'sys_reg'")
        b_total = b_cursor.fetchone()[0]
        if b_total:
            b_total = str(b_total)
        else:
            b_total = "0"

        cursor = self.db.cursor()
        get_user_sql = "select a.PHONE from dm_report.ind_info a " \
                       "where CUSTOMERID > '" + b_total + "'" \
                       "and PHONE is not null and PHONE <> '00000000000' and length(PHONE) > 10 limit " + str(num)
        cursor.execute(get_user_sql)
        rows = cursor.fetchall()
        users = []
        for row in rows:
            users.append(row[0])
        self.log.info("要生成注册的用户手机号:{}".format(users))
        return users

    def reg_user(self, user_reg):
        reg_sql = '''INSERT INTO `customer_info` (
                    `customer_id`,
                    `register_channel`,
                    `real_name`,
                    `sex`,
                    `cert_id`,
                    `mobile`,
                    `status`,
                    `create_user`,
                    `update_user`,
                    `create_time`,
                    `update_time`
                )
                VALUES
                    (
                        '{}',
                        'sys_reg',
                        NULL,
                        NULL,
                        NULL,
                        '{}',
                        '1',
                        'sys',
                        'sys',
                        '{}',
                        '{}'
                    )
                '''

        reg_cursor = self.business_db.cursor()
        for u in user_reg:
            user_id = 'MC' + time.strftime('%Y%m%d') + str(uuid.uuid1()).replace('-', '')[:19]
            # 5分钟之前的时间随机
            before_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + random.randint(-300, 0)))
            try:
                # 执行sql语句
                reg_cursor.execute(reg_sql.format(user_id, u, before_time, before_time))
                # 提交到数据库执行
                self.business_db.commit()
            except Exception as e:
                # Rollback in case there is any error
                self.log.error(traceback.format_exc())
                self.log.error('register Exception: ', e)
                self.db.rollback()
        # db注册操作提交
        self.log.info("reg over")

    def user_login(self):
        login_cursor = self.business_db.cursor()
        login_cursor.execute("SELECT max(id) FROM customer_info")
        reg_count = int(login_cursor.fetchone()[0])
        # 9-22点13小时，每5分钟一次，每小时执行12次
        take_count = math.ceil(reg_count * random.randint(50, 60) / 100 / (13*12))
        self.log.info("将要取{}条记录进行登陆".format(take_count))

        # 随机取出的id
        login_ids = [str(random.randint(1, reg_count)) for i in range(take_count)]
        login_cursor.execute("SELECT id FROM customer_info where id in({})".format(','.join(login_ids)))
        row_take = login_cursor.fetchall()
        login_take = []
        for row_i in row_take:
            login_take.append(row_i[0])
        self.log.info(("要生成登陆的用户id:{}".format(login_take)))

        # 记录插入登陆表
        login_sql = '''INSERT INTO `customer_login_history` (
                    `customer_id`,
                    `login_terminal`,
                    `login_time`,
                    `create_time`,
                    `update_time`
                )
                VALUES
                    (
                        '{}',
                        'sys_login',
                        '{}',
                        now(),
                        now()
                    );'''
        for login_id in login_take:
            # 5分钟之前的时间随机
            login_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + random.randint(-300, 0)))
            try:
                # 执行sql语句
                login_cursor.execute(login_sql.format(login_id, login_time))
                # db注册操作提交
                self.business_db.commit()
            except Exception as e:
                # Rollback in case there is any error
                self.log.error(traceback.format_exc())
                self.log.error('login Exception: ', e)
                self.db.rollback()

        self.log.info("login over")

    def closes(self):
        # 关闭数据库连接
        self.db.close()
        self.business_db.close()


if __name__ == '__main__':
    # 初始化 db，log
    gr = GenerateReg()
    # 随机选取3-7条记录
    user2reg = gr.get_user(5 + random.randint(-2, 2))
    # 选取用户生成注册
    gr.reg_user(user2reg)
    # 选取用户生成登陆
    gr.user_login()
    # # 关闭 db
    gr.closes()


