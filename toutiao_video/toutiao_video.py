#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-11-08 09:49:36
# Project: zzw_test

import time
from pyspider.libs.base_handler import *
from toutiao_video import ToutiaoRequest as ttr
from db import MysqlUtil


class Handler(BaseHandler):
    crawl_config = {
        'header': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'm.365yg.com',
            'Upgrade-Insecure-Requests': '1',
            'Cookie': 'tt_webid=6625475797447607822; _ga=GA1.2.1625766023.1542613797; _gid=GA1.2.1374947038.1542613797; csrftoken=dee2e2deb7718b844aa5662aeca51b3e; _ba=BA0.2-20181119-51225-5LsRrZyZfDwnoeh6gTJJ; __tasessionId=3jxtd6ld11542617753708',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36'
        },
        "timeout": 120,
        "connect_timeout": 60,
        "retries": 0,
        "fetch_type": None,
        "auto_recrawl": False,
        "mysql_host": "47.101.146.57",
        "mysql_port": 2018,
        "mysql_db": "dm_report",
        "mysql_user": "root",
        "mysql_password": "Liuku!!!111",
        "mysql_charset": "utf8"
    }

    @every(seconds=20)
    def on_start(self):
        url = 'http://m.365yg.com/list/?tag=video&ac=wap&count=20&format=json_raw'
        param = ttr.toutiao("", url).getParam()
        request_url = url + param
        self.crawl(request_url, callback=self.index_page, headers=self.crawl_config["header"])

    @config(age=3 * 20)
    def index_page(self, response):
        if response and response.cookies:
            self.crawl_config["header"]["Cookie"] = response.cookies

        jarray = [{
            "source_site": video.get('source_site', 'https://m.toutiao_video.com'),
            "source_site_tag": video.get('source_site_tag', 'video'),
            "video_id": video.get('video_id', ''),
            "media_name": video.get('media_name', ''),
            "title": video.get('title', ''),
            "abstract": video.get('abstract', ''),
            "keywords": video.get('keywords', ''),
            "tag": video.get('tag', ''),
            "video_duration": video.get('video_duration', ''),
            "source_url": video.get('url', ''),
            "article_type": video.get('article_type', ''),
            "large_mode": video.get('large_mode', ''),
            "large_image_url": video.get('large_image_url', ''),
            "publish_time": video.get('publish_time', ''),
            "comment_count": video.get('comment_count', '')
        } for video in response.json['data'] if video.get('label', '视频') != '广告'
        ]
        self.insert_mysql(jarray)
        return jarray

    def insert_mysql(self, jarray):
        batch_sql = []
        for video in jarray:
            # SQL 插入语句
            # print(video.get('media_name',''))
            sql = """INSERT INTO `test`.`toutiao_video` (`source_site`, `source_site_tag`, `video_id`, `media_name`, `title`, `abstract`, `keywords`, `tag`, `video_duration`, `source_url`, `article_type`, `large_mode`, `large_image_url`, `publish_time`, `create_time`) 
                  VALUES ('{}', '{}', '{}', '{}','{}','{}', '{}', '{}', '{}','{}', '{}', '{}', '{}', '{}', '{}');""" \
                .format(video.get('source_site', ''), video.get('source_site_tag', ''), video.get('video_id', ''),
                        video.get('media_name', ''), video.get('title', ''), video.get('abstract', ''),
                        video.get('keywords', ''), video.get('tag', ''), video.get('video_duration', ''),
                        video.get('source_url', ''), video.get('article_type', ''), video.get('large_mode', ''),
                        video.get('large_image_url', ''), video.get('publish_time', ''),
                        time.strftime("%Y-%m-%d %H:%M:%S"))
            batch_sql.append(sql)
        # 插入mysql
        msUtil = MysqlUtil(self.crawl_config["mysql_host"], self.crawl_config["mysql_port"],
                           self.crawl_config["mysql_user"]
                           , self.crawl_config["mysql_password"], self.crawl_config["mysql_db"],
                           self.crawl_config["mysql_charset"])
        #
        msUtil.execute_batch(batch_sql)


if __name__ == '__main__':
    t = Handler()
    print(t.crawl('https://www.365yg.com/'))
