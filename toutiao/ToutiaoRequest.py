#!coding=utf-8
import requests
import re
import json
import os
import random
import time
import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  ###禁止提醒SSL警告
import hashlib
import execjs


class toutiao(object):

    def __init__(self, path, url):
        self.path = path  # CSV保存地址
        self.url = url
        self.s = requests.session()
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'm.365yg.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Mobile Safari/537.36'
            }
        self.s.headers.update(headers)
        # self.channel = re.search('ch/(.*?)/', url).group(1)
        self.urli = None

    def closes(self):
        self.s.close()

    def getParam(self):  # 获取数据

        self.s.get(url=self.url, verify=False)
        headers = {'referer': self.url}
        self.s.headers.update(headers)

        Honey = json.loads(self.get_js())
        eas = Honey['as']
        ecp = Honey['cp']
        signature = Honey['_signature']
        min_behot_time = int(time.time())
        if self.urli == None:
            self.urli = min_behot_time - 24 * 60 * 60

        urlParam = '&min_behot_time={}&as={}&cp={}&_signature={}&i={}'\
            .format(min_behot_time, eas, ecp, signature, self.urli)
        return urlParam

    def getdata(self):  # 获取数据

        req = self.s.get(url=self.url, verify=False)
        # print (self.s.headers)
        # print(req.text)
        headers = {'referer': self.url}
        max_behot_time = '0'
        signature = '.1.hXgAApDNVcKHe5jmqy.9f4U'
        eas = 'A1E56B6786B47FE'
        ecp = '5B7674A7FF2E9E1'
        self.s.headers.update(headers)
        title = []
        source = []
        source_url = []
        comments_count = []
        tag = []
        chinese_tag = []
        label = []
        abstract = []
        behot_time = []
        nowtime = []
        duration = []
        for i in range(0, 30):  ##获取页数

            Honey = json.loads(self.get_js())
            # eas = self.getHoney(int(max_behot_time))[0]
            # ecp = self.getHoney(int(max_behot_time))[1]
            eas = Honey['as']
            ecp = Honey['cp']
            signature = Honey['_signature']
            url = 'https://www.toutiao.com/api/pc/feed/?category={}&utm_source=toutiao&widen=1&max_behot_time={}&max_behot_time_tmp={}&tadrequire=true&as={}&cp={}&_signature={}'.format(
                self.channel, max_behot_time, max_behot_time, eas, ecp, signature)
            req = self.s.get(url=url, verify=False)
            time.sleep(random.random() * 2 + 2)
            # print(req.text)
            # print(url)
            j = json.loads(req.text)

            for k in range(0, 10):

                now = time.time()
                if j['data'][k]['tag'] != 'ad':
                    title.append(j['data'][k]['title'])  ##标题
                    source.append(j['data'][k]['source'])  ##作者
                    source_url.append('https://www.toutiao.com/' + j['data'][k]['source_url'])  ##文章链接
                    try:
                        comments_count.append(j['data'][k]['comments_count'])  ###评论
                    except:
                        comments_count.append(0)

                    tag.append(j['data'][k]['tag'])  ###频道名
                    try:
                        chinese_tag.append(j['data'][k]['chinese_tag'])  ##频道中文名
                    except:
                        chinese_tag.append('')
                    try:
                        label.append(j['data'][k]['label'])  ## 标签
                    except:
                        label.append('')
                    try:
                        abstract.append(j['data'][k]['abstract'])  ###文章摘要
                    except:
                        abstract.append('')
                    behot = int(j['data'][k]['behot_time'])
                    behot_time.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(behot)))  ####发布时间
                    nowtime.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now)))  ##抓取时间
                    duration.append(now - behot)  ##发布时长
            time.sleep(2)

            # max_behot_time=str(j['next']['max_behot_time'])
            print('------------' + str(j['next']['max_behot_time']))
            print(title)
            print(source)
            print(source_url)
            print(comments_count)
            print(tag)
            print(chinese_tag)
            print(label)
            print(abstract)
            print(behot_time)
            print(nowtime)
            print(duration)
            data = {'title': title, 'source': source, 'source_url': source_url, 'comments_count': comments_count,
                    'tag': tag,
                    'chinese_tag': chinese_tag, 'label': label, 'abstract': abstract, 'behot_time': behot_time,
                    'nowtime': nowtime, 'duration': duration,
                    }

            df = pd.DataFrame(data=data)
            # df.to_csv(self.path + r'\toutiao.csv', encoding='GB18030', index=0)

    def getHoney(self, t):  #####根据JS脚本破解as ,cp
        # t = int(time.time())  #获取当前时间
        # t=1534389637
        # print(t)
        e = str('%X' % t)  ##格式化时间
        # print(e)
        m1 = hashlib.md5()  ##MD5加密
        m1.update(str(t).encode(encoding='utf-8'))  ##转化格式
        i = str(m1.hexdigest()).upper()  ####转化大写
        # print(i)
        n = i[0:5]  ##获取前5位
        a = i[-5:]  ##获取后5位
        s = ''
        r = ''
        for x in range(0, 5):
            s += n[x] + e[x]
            r += e[x + 3] + a[x]
        eas = 'A1' + s + e[-3:]
        ecp = e[0:3] + r + 'E1'
        # print(eas)
        # print(ecp)
        return eas, ecp

    def get_js(self):

        f = open(r"/Users/krison/PycharmProjects/SixSpider/toutiao/signature.js", 'r', encoding='UTF-8')
        line = f.readline()
        htmlstr = ''
        while line:
            htmlstr = htmlstr + line
            line = f.readline()
        ctx = execjs.compile(htmlstr)
        return ctx.call('get_as_cp_signature')


if __name__ == '__main__':
    url = 'https://www.toutiao.com/ch/news_tech/'
    t = toutiao("", url)
    # t.getdata()
    #
    # t.closes()
    print(t.getParam())


