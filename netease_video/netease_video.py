#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-12-17 16:52:03
# Project: netease_video

from pyspider.libs.base_handler import *
import json
import time
from db import MysqlUtil


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
        'channel_type': {"Video_Movies": "video_movie"
            , "Video_Gossip": "video_variety"
            , "Video_Music": "video_music"
            , "Video_Funny": "video_funny"
            , "Video_Scene": "video_domestic"
            , "Video_Adorable": "video_child"
            , "Video_Curious": "video_life"
            , "Video_Military": "video_military"
            , "Video_Technology": "video_tech"
            , "Video_Comic": "video_comic"
            , "Video_Opusculum": "video_shortsketch"
            , "Video_Beauty": "video_beauty"
            , "Video_Recom": "video_recom"
            , "Video_Knowledge": "video_knowledge"},
        'header': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': '_ntes_nnid=3384e64fbdea397b3ef25890f3ae1ac2,1545014667201; _ntes_nuid=3384e64fbdea397b3ef25890f3ae1ac2; _antanalysis_s_id=1546494056834; Province=021; City=021; NNSSPID=2237fe761e094a848025c7ac308832c2',
            'Host': '3g.163.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36'
        },
        "mysql_host": "47.101.146.57",
        "mysql_port": 2018,
        "mysql_db": "dm_report",
        "mysql_user": "root",
        "mysql_password": "Liuku!!!111",
        "mysql_charset": "utf8"
    }

    @every(seconds=120)
    def on_start(self):
        self.crawl('https://3g.163.com/touch/video/?ver=c', callback=self.index_page, validate_cert=False)

    @config(age=60)
    def index_page(self, response):
        if response and response.cookies:
            self.crawl_config["header"]["Cookie"] = response.cookies

        for k, v in self.crawl_config['channel'].items():
            self.crawl(self.crawl_config['video_url'].format(v, int(time.time())), callback=self.detail_page,
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
                            # video['tag']=channel
                            # print(video)
                            video_tag = self.crawl_config["channel_type"].get(channel, None)
                            print(video['vid'], video_tag)
                            if video_tag:
                                video['tag'] = video_tag
                                jarray.append(video)

        batch_sql = []
        for video in jarray:
            # SQL 插入语句
            sql = """INSERT INTO `netease_video` (`source_site`, `source_site_tag`, `video_id`, `media_name`, `title`, `abstract`, `keywords`, `tag`, `video_duration`, `source_url`, `article_type`, `large_mode`, `large_image_url`, `publish_time`,`watch_count`,`comment_count`,`reply_id`,`create_time`) VALUES ('{}', '{}', '{}', '{}','{}','{}', '{}', '{}', '{}','{}', '{}', '{}', '{}', '{}','{}','{}','{}', '{}');""".format(
                'https://3g.163.com/touch/video/', video.get('video', 'video'), video.get('vid', ''),
                video.get('videosource', ''), video.get('title', ''), video.get('mp4_url', ''),
                video.get('keywords', ''), video.get('tag', ''), video.get('length', ''), video.get('mp4_url', ''),
                video.get('article_type', ''), video.get('large_mode', ''), video.get('cover', ''),
                video.get('putime', ''), video.get('playCount', ''), video.get('replyCount', ''),
                video.get('replyid', ''), time.strftime("%Y-%m-%d %H:%M:%S"))
            batch_sql.append(sql)
        # 插入mysql
        msUtil = MysqlUtil.MysqlUtil(self.crawl_config["mysql_host"], self.crawl_config["mysql_port"],
                                     self.crawl_config["mysql_user"], self.crawl_config["mysql_password"],
                                     self.crawl_config["mysql_db"], self.crawl_config["mysql_charset"])
        msUtil.execute_batch(batch_sql)
        return jarray

    def on_result(self, result):
        return

