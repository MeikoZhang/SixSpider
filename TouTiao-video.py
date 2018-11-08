#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-11-08 09:49:36
# Project: zzw_test

from pyspider.libs.base_handler import *

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=10)
    def on_start(self):
        self.crawl(
            'https://www.365yg.com/api/pc/feed/?min_behot_time=1541658442&category=video_new&utm_source=toutiao&widen=1&tadrequire=true&as=A1955BBE231D77E&cp=5BE32D27776EBE1&_signature=cT2ocxAZKuHbEujzv9P-Y3E9qG',
            callback=self.index_page)

    @config(age=10 * 60)
    def index_page(self, response):
        return [{
            "title": x['title'],
            "image": x['image_url'],
            "source": x['source_url'],
            "video_id": x['video_id']
        } for x in response.json['data']
        ]


