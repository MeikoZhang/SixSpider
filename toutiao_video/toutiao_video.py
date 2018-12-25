#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-11-08 09:49:36
# Project: zzw_test

import time
import json
from pyspider.libs.base_handler import *
from toutiao_video import ToutiaoRequest as ttr
from db import MysqlUtil
import random
from zlib import crc32
import requests
import base64
import traceback


class Handler(BaseHandler):
    crawl_config = {
        'header': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'm.365yg.com',
            'Upgrade-Insecure-Requests': '1',
            'Cookie': 'tt_webid=6625475797447607822; _ga=GA1.2.1625766023.1542613797; _gid=GA1.2.1374947038.1542613797;csrftoken=dee2e2deb7718b844aa5662aeca51b3e; _ba=BA0.2-20181119-51225-5LsRrZyZfDwnoeh6gTJJ; __tasessionId=3jxtd6ld11542617753708',
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

    @every(seconds=30)
    def on_start(self):
        url = 'http://m.365yg.com/list/?tag=video&ac=wap&count=20&format=json_raw'
        param = ttr.toutiao("", url).getParam()
        request_url = url + param
        self.crawl(request_url, callback=self.index_page, headers=self.crawl_config["header"])

    @config(age=15)
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
            "watch_count": video.get('video_detail_info', '').get('video_watch_count', '0'),
            "comment_count": video.get('comment_count', '0')
        } for video in response.json['data'] if video.get('label', '视频') != '广告'
        ]
        batch_sql = []
        for video in jarray:
            if video.get('source_url', '').startswith('http://toutiao.com/group/'):
                video['source_url'] = self.get_real_url(video.get('video_id'))

            # SQL 插入语句
            sql = """INSERT INTO `toutiao_video` (`source_site`, `source_site_tag`, `video_id`, `media_name`, `title`, `abstract`, `keywords`, `tag`, `video_duration`, `source_url`, `article_type`, `large_mode`, `large_image_url`, `publish_time`,`watch_count`,`comment_count`,`create_time`) VALUES ('{}', '{}', '{}', '{}','{}','{}', '{}', '{}', '{}','{}', '{}', '{}', '{}', '{}','{}','{}', '{}');""".format(
                video.get('source_site', ''), video.get('source_site_tag', ''), video.get('video_id', ''),
                video.get('media_name', ''), video.get('title', ''), video.get('abstract', ''),
                video.get('keywords', ''), video.get('tag', ''), video.get('video_duration', ''),
                video.get('source_url', ''), video.get('article_type', ''), video.get('large_mode', ''),
                video.get('large_image_url', ''), video.get('publish_time', ''), video.get('watch_count', ''),
                video.get('comment_count', ''), time.strftime("%Y-%m-%d %H:%M:%S"))
            batch_sql.append(sql)
        # 插入mysql
        msUtil = MysqlUtil.MysqlUtil(self.crawl_config["mysql_host"], self.crawl_config["mysql_port"],
                                     self.crawl_config["mysql_user"], self.crawl_config["mysql_password"],
                                     self.crawl_config["mysql_db"], self.crawl_config["mysql_charset"])
        msUtil.execute_batch(batch_sql)
        return jarray

    @staticmethod
    def get_real_url(video_id):
        r = ''
        for i in range(0, 16):
            r = r + str(random.randint(1, 9))
        crc = crc32('/video/urls/v/1/toutiao/mp4/{}?r={}'.format(video_id, str(r)).encode('utf-8'))
        url = 'http://i.snssdk.com/video/urls/v/1/toutiao/mp4/{}?r={}&s={}'.format(video_id, r, crc)
        try:
            r = requests.get(url)
            r_json = r.json()
            video_list = r_json['data']['video_list']
            if video_list:
                video_1 = video_list.get('video_1', None)
                video_2 = video_list.get('video_2', None)
                video_3 = video_list.get('video_3', None)
                if video_3:
                    video_url = video_3
                elif video_2:
                    video_url = video_2
                elif video_1:
                    video_url = video_1
                else:
                    print("no video", video_id, url)
                    return None
                if video_url:
                    return str(base64.b64decode(video_url['main_url'].encode('utf-8')), 'utf-8')
        except Exception as e:
            print("somethings error", video_id, url)
            print(traceback.format_exc())
            return None

    @config(priority=2)
    def detail_page(self, response):
        return response

    def on_result(self, result):
        return
