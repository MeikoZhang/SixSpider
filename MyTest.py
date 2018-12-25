import time
import execjs
import os
import selenium
import json
import db.MysqlUtil as mu
import db.PgUtil as pu
import requests
from selenium import webdriver
from db import MysqlUtil
import random
from zlib import crc32
import pymysql
import base64
import traceback
import binascii
import re

crawl_config = {
    "mysql_host": "47.101.146.57",
    "mysql_port": 2018,
    "mysql_db": "dm_report",
    "mysql_user": "root",
    "mysql_password": "Liuku!!!111",
    "mysql_charset": "utf8"
}
db = pymysql.connect(host="47.101.146.57", port=2018, user="root", password="Liuku!!!111", db="dm_report",
                     charset="utf8")
db.autocommit(True)
cursor = db.cursor(pymysql.cursors.SSCursor)
cursor.execute("select * from toutiao_video where id > 100000")
results = cursor.fetchall()
if cursor:
    for row in results:
        id = row[0]
        video_id = row[3]
        source_url = row[10]

        if source_url.startswith('http://toutiao.com/group/'):
            print("record id", id)

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
                    video_url = None
                    if video_3:
                        video_url = video_3
                    elif video_2:
                        video_url = video_2
                    elif video_1:
                        video_url = video_1
                    else:
                        print("no video", video_id, url)

                    if video_url:
                        video_real_url = str(base64.b64decode(video_url['main_url'].encode('utf-8')), 'utf-8')
                        # print(video_real_url)
                        try:
                            cursor.execute("update toutiao_video set source_url='{}' where id={}"
                                           .format(video_real_url, id))
                            print("update success", id, video_real_url)
                        except Exception as e:
                            print("update sql error", id, video_real_url)
                            print(traceback.format_exc())
            except Exception as e:
                print("somethings error", video_id, url)
                print(traceback.format_exc())

cursor.close()
db.close()
