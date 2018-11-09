#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-11-08 09:49:36
# Project: zzw_test
import os
from pyspider.libs.base_handler import *
from toutiao import ToutiaoRequest as ttr


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
        return [{
            "title": x.get('title',''),
            "media_name": x.get('media_name', ''),
            "keywords": x.get('keywords',''),
            "abstract": x.get('abstract',''),
            "url": x.get('url',''),
            "behot_time": x.get('behot_time','')
             } for x in response.json['data'] if x.get('label', '视频') == '视频'
            ]



