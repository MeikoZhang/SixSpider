import execjs

import execjs
import os
from toutiao import ToutiaoRequest as ttr
# 先导入selenium模块，没安装的自行百度安装就好
import selenium
import json
import db.MysqlUtil as mu
import db.PgUtil as pu


# 参考https://blog.csdn.net/weixin_39416561/article/details/82111455
def get_js():
    # 打开JS文件
    f = open(r"/Users/krison/PycharmProjects/SixSpider/toutiao_video/signature.js", 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    ctx = execjs.compile(htmlstr)
    return ctx.call('get_as_cp_signature')


# t = ttr.toutiao_video(os.getcwd(),'https://www.toutiao.com/ch/news_tech/')
# print(t.getParam())

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
# mu.MysqlUtil().insert(json.dumps(sql))
# pu.PgUtil().insert(json.dumps(sql))
# handler = BaseHandler()
# response = handler.crawl('http://m.365yg.com')
# print(response)
# print("2'1'3".replace(chr(39), "\\'"))

