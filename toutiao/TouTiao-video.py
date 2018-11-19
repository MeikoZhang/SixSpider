#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-11-08 09:49:36
# Project: zzw_test
import os
import json
from pyspider.libs.base_handler import *
from toutiao import ToutiaoRequest as ttr
from toutiao import MysqlUtil as msUtil
from toutiao import PgUtil as pgUtil


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
        "retries": 5,
        "fetch_type": None,
        "auto_recrawl": True
    }

    @every(minutes=10)
    def on_start(self):
        url = 'http://m.365yg.com/list/?tag=video&ac=wap&count=20&format=json_raw'
        param = ttr.toutiao("", url).getParam()
        request_url = url + param
        self.crawl(request_url, callback=self.index_page, headers=self.crawl_config["header"])

    @config(age=10 * 60)
    def index_page(self, response):
        if response.cookies:
            self.crawl_config["header"]["Cookies"] = response.cookies

        jarray = [{
            "source_site": video.get('source_site', 'https://m.toutiao.com'),
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
        # msUtil.MysqlUtil().insert(json.dumps(jarray))
        pgUtil.PgUtil().insert(json.dumps(jarray))
        return jarray
