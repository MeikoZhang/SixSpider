#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pymysql


class MysqlUtil(object):

    def __init__(self, host: str, port: int, user: str, password: str, db: str, charset: str):
        if charset.strip() == '':
            charset = 'utf8'

        db = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
        self.db = db
        self.cursor = db.cursor()

    def executeQuery(self, query_sql):
        if isinstance(query_sql, str):
            try:
                # 执行sql语句
                self.cursor.execute(query_sql)
                result = self.cursor.fetchall()
                self.db.commit()
                return result
                # 提交到数据库执行
            except Exception as e:
                # Rollback in case there is any error
                print('Query Exception: ', e)
        else:
            print('error ,plesase input string')
            return None

    def execute(self, execute_sql):
        if isinstance(execute_sql, str):
            try:
                # 执行sql语句
                self.cursor.execute(execute_sql)
                self.db.commit()
                # 提交到数据库执行
            except Exception as e:
                # Rollback in case there is any error
                print('Exception: ', e)
                self.db.rollback()
        else:
            print('error ,plesase input string')

    def execute_batch(self, batch_sql):
        if isinstance(batch_sql, list):
            for each in batch_sql:
                try:
                    # 执行sql语句
                    self.cursor.execute(each)
                    self.db.commit()
                    # 提交到数据库执行
                except Exception as e:
                    # Rollback in case there is any error
                    print(batch_sql)
                    print('Exception: ', e)
                    self.db.rollback()
        else:
            print('error ,plesase input list')

    def closes(self):
        # 关闭数据库连接
        self.db.close()

    def get_cursor(self):
        self.cursor


if __name__ == '__main__':
    host = "47.101.146.57"
    port = 2018
    user = "root"
    password = "Liuku!!!111"
    db = "dm_report"
    charset = 'utf8'
    mysqlUtil = MysqlUtil(host, port, user, password, db, charset)

    sql = "INSERT INTO `toutiao_video`" \
          "(`source_site`,`source_site_tag`,`video_id`,`media_name`,`title`,`abstract`,`keywords`,`tag`," \
          "`video_duration`,`source_url`,`article_type`,`large_mode`,`large_image_url`,`publish_time`," \
          "`create_time`,`check_status`,`check_user_id`,`check_time`)" \
          "VALUES('source_site','source_site_tag','video_id','media_name','title','abstract','keywords','tag'," \
          "'video_duration','source_url','article_type','large_mode','large_image_url','publish_time'," \
          "'2018-11-24 21:24:08','0','',NULL);";

    mysqlUtil.execute(sql)
