# 导入依赖包
# !/usr/bin/python3

import psycopg2


class PgUtil(object):

    def __init__(self, host: str, port: int, user: str, password: str, db: str):
        # 创建连接对象
        self.db = conn = psycopg2.connect(database=db, user=user, password=password,host=host, port=port)
        self.cursor = conn.cursor()  # 创建指针对象

    def execute(self, execute_sql):
        if isinstance(execute_sql, str):
            try:
                # 执行sql语句
                self.cursor.execute(execute_sql)
                # 提交到数据库执行
            except Exception as e:
                # Rollback in case there is any error
                print('Exception: ', e)
                self.db.rollback()
            self.db.commit()
        else:
            print('error ,plesase input string')

    def execute_batch(self, batch_sql):
        if isinstance(batch_sql, list):
            for each in batch_sql:
                try:
                    # 执行sql语句
                    self.cursor.execute(each)
                    # 提交到数据库执行
                except Exception as e:
                    # Rollback in case there is any error
                    print('Exception: ', e)
                    self.db.rollback()
            self.db.commit()
        else:
            print('error ,plesase input list')

    def closes(self):
        # 关闭数据库连接
        self.db.close()

    def closes(self):
        # 关闭数据库连接
        self.db.close()


if __name__ == '__main__':
    host = "172.16.5.212"
    port = 5432
    user = "bigdata"
    password = "bigdata"
    db = "loan_market"
    pgUtil = PgUtil(host, port, user, password, db)

    sql = "INSERT INTO public.toutiao_video " \
          "(source_site,source_site_tag,video_id,media_name,title,abstract,keywords,tag" \
          ",video_duration,source_url,article_type,large_mode,large_image_url" \
          ",publish_time,create_time,check_status,check_user_id,check_time,update_time)" \
          "VALUES" \
          "('source_site','source_site_tag','video_id','media_name','title','abstract','keywords','tag'," \
          "'video_duration','source_url','article_type','large_mode','large_image_url'," \
          "'publish_time','2018-11-19 17:39:46',NULL,NULL,NULL,'2018-11-19 17:39:30.905143')";

    pgUtil.execute(sql)


