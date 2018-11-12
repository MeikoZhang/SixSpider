#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-11-08 09:49:36
# Project: zzw_test
import os
import json
from pyspider.libs.base_handler import *
from toutiao import ToutiaoRequest as ttr
from toutiao import MysqlUtil as msUtil


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=10)
    def on_start(self):
        url = 'https://m.toutiao.com/list/?tag=video&ac=wap&count=20&format=json_raw'
        param = ttr.toutiao("", url).getParam()
        request_url = url.join(param)
        self.crawl(request_url, callback=self.index_page)

    @config(age=10 * 60)
    def index_page(self, response):
        jarray = [{
            "source_site": video.get('source_site',''),
            "source_site_tag": video.get('source_site_tag',''),
            "video_id": video.get('video_id',''),
            "media_name": video.get('media_name',''),
            "title": video.get('title',''),
            "abstract": video.get('abstract',''),
            "keywords": video.get('keywords',''),
            "tag": video.get('tag',''),
            "video_duration": video.get('video_duration',''),
            "source_url": video.get('source_url',''),
            "article_type": video.get('article_type',''),
            "large_mode": video.get('large_mode',''),
            "large_image_url": video.get('large_image_url',''),
            "publish_time": video.get('publish_time','')
        } for video in response.json['data'] if video.get('label', '视频') == '视频'
        ]
        msUtil.MysqlUtil().insert(json.dumps(jarray))
        return jarray
