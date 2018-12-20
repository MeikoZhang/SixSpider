#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-12-17 16:52:03
# Project: netease_video

from pyspider.libs.base_handler import *
import json
import time


class Handler(BaseHandler):
    crawl_config = {
        'itag': 'v223',
        'video_url': 'https://3g.163.com/touch/nc/api/video/recommend/{}/0-20.do?callback=&{}',
        'channel': {"推荐": "Video_Recom"
            , "搞笑": "Video_Funny"
            , "美女": "Video_Beauty"
            , "新闻现场": "Video_Scene"
            , "萌物": "Video_Adorable"
            , "八卦": "Video_Gossip"
            , "猎奇": "Video_Curious"
            , "黑科技": "Video_Technology"
            , "涨姿势": "Video_Knowledge"
            , "二次元": "Video_Comic"
            , "军武": "Video_Military"
            , "影视": "Video_Movies"
            , "音乐": "Video_Music"
            , "小品": "Video_Opusculum"},
        'header': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': '',
            'Host': '3g.163.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36'
        }
    }

    @every(minutes=1)
    def on_start(self):
        self.crawl('https://3g.163.com/touch/video/', callback=self.index_page, headers=self.crawl_config["header"],
                   validate_cert=False)

    @config(age=2 * 60)
    def index_page(self, response):
        if response and response.cookies:
            self.crawl_config["header"]["Cookie"] = response.cookies

        for k, v in self.crawl_config['channel'].items():
            self.crawl(self.crawl_config['video_url'].format(v, time.time()), callback=self.detail_page,
                       headers=self.crawl_config["header"], validate_cert=False)

    @config(priority=2)
    def detail_page(self, response):
        jarray = []
        # 截取头尾，转化json
        text_json = json.loads(response.text[1:-1])
        if isinstance(text_json, dict):
            for channel, video_list in text_json.items():
                # 遍历内容
                if isinstance(video_list, list):
                    for video in video_list:
                        if isinstance(video, dict):
                            print(video)
                            jarray.append(video)

        return jarray
