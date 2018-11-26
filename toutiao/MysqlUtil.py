#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pymysql
import json
import time


class MysqlUtil(object):

    def __init__(self):
        db = pymysql.connect("kvcong.com", "test", "6e683c8c2f", "test", charset='utf8')
        self.db = db
        self.cursor = db.cursor()

    def insert(self, sql):

        json_insert = json.loads(sql)
        # print(json_insert)
        for video in json_insert:
            # SQL 插入语句
            # print(video.get('media_name',''))
            sql = """INSERT INTO `test`.`toutiao_video` (`source_site`, `source_site_tag`, `video_id`, `media_name`, `title`, `abstract`, `keywords`, `tag`, `video_duration`, `source_url`, `article_type`, `large_mode`, `large_image_url`, `publish_time`, `create_time`) 
                  VALUES ('{}', '{}', '{}', '{}','{}','{}', '{}', '{}', '{}','{}', '{}', '{}', '{}', '{}', '{}');"""\
                .format(video.get('source_site', ''), video.get('source_site_tag', ''), video.get('video_id', ''),
                  video.get('media_name', ''), video.get('title', ''), video.get('abstract', ''),
                  video.get('keywords', ''), video.get('tag', ''), video.get('video_duration', ''),
                  video.get('source_url', ''), video.get('article_type', ''), video.get('large_mode', ''),
                  video.get('large_image_url', ''), video.get('publish_time', ''), time.strftime("%Y-%m-%d %H:%M:%S"))

            try:
                # 执行sql语句
                self.cursor.execute(sql)
                # 提交到数据库执行
            except Exception as e:
                # Rollback in case there is any error
                print('Exception: ', e)
                self.db.rollback()

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
    MysqlUtil().insert(json.dumps(sql))
