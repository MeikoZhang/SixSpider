# 导入依赖包
# !/usr/bin/python3

import psycopg2
import json
import time


class PgUtil(object):

    def __init__(self):
        # 创建连接对象
        self.db = conn = psycopg2.connect(database="loan_market", user="bigdata", password="bigdata", host="172.16.5.212", port="5432")
        self.cursor = conn.cursor()  # 创建指针对象

    def insert(self, sql):

        json_insert = json.loads(sql)
        # print(json_insert)
        for video in json_insert:
            # SQL 插入语句
            # print(video.get('media_name',''))
            sql = """INSERT INTO "toutiao_video" ("source_site", "source_site_tag", "video_id", "media_name", "title", "abstract", "keywords", "tag", "video_duration", "source_url", "article_type", "large_mode", "large_image_url", "publish_time", "create_time") 
                  VALUES ('{}', '{}', '{}', '{}','{}','{}', '{}', '{}', '{}','{}', '{}', '{}', '{}', '{}', '{}');"""\
                .format(video.get('source_site',''), video.get('source_site_tag',''), video.get('video_id',''),
                  video.get('media_name',''), video.get('title',''), video.get('abstract',''),
                  video.get('keywords',''), video.get('tag',''), video.get('video_duration',''),
                  video.get('source_url',''), video.get('article_type',''), video.get('large_mode',''),
                  video.get('large_image_url',''), video.get('publish_time',''), time.strftime("%Y-%m-%d %H:%M:%S"))

            try:
                # 执行sql语句
                # self.cursor.execute("INSERT INTO student(id,name,sex)VALUES(%s,%s,%s)", (2, 'Taxol', 'F'))
                # 插入数据
                self.cursor.execute(sql)
            except Exception as e:
                # Rollback in case there is any error
                # print('Exception: ', e)
                # self.db.rollback()
                return
        # 提交到数据库执行
        self.db.commit()


def closes(self):
    # 关闭数据库连接
    self.db.close()


if __name__ == '__main__':
    sql = [{
        'video_id': 1,
        'media_name': 'Runoob',
        'url': 'http://www.runoob.com'
    },
        {
            'video_id': 2,
            'media_name': 'test2',
            'url': 'http://www.runoob.com'
        }
    ]
    PgUtil().insert(json.dumps(sql))


