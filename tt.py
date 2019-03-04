# -*- coding:utf-8 -*-
import random
import itertools
import os
import requests
import time
import re
import pymysql

# headers = {
#     'Accept': '*/*'
#     , 'Accept-Encoding': 'gzip, deflate, br'
#     , 'Accept-Language': 'zh-CN,zh;q=0.9'
#     , 'Connection': 'keep-alive'
#     ,
#     'Cookie': 'hb_MA-8EA5-1B4E54656795_source=m.baidu.com; _ga=GA1.2.243187517.1547686966; _gid=GA1.2.872076141.1547686966; __root_domain_v=.163.com; _qddaz=QD.v74x7e.f0uqrl.jqzwuy4n; _ntes_nnid=6bfb3b5f03f02b9dd4e1398bf6b44e6a,1547686971102; _ntes_nuid=6bfb3b5f03f02b9dd4e1398bf6b44e6a; NNSSPID=36ec97b02ce24867b3ff4dacb02aff0d; _antanalysis_s_id=1547686971852; Province=0; City=0; BAIDU_SSP_lcr=https://www.baidu.com/link?url=pCG4G-LfrPw3L1ThTtF2sweSiBKvQ4DvJ60ZeeRDwO3&wd=&eqid=95151d420001fcb2000000045c3fd508; NTES_hp_textlink1=old; UM_distinctid=16859583c5042f-0a55826e3b0374-b781636-100200-16859583c519ba; s_n_f_l_n3=8a0bceb0ce0859e11547687210317; vjuids=-60184445e.168595930f9.0.ac060fcd48d33; vjlast=1547687244.1547687244.30; _antanalysis_s_id=1547687426710; __gads=ID=6b7f82e56f766cfe:T=1547687428:S=ALNI_MZdKDeslefTU4zLGxDmog0dyOIlrA; ne_analysis_trace_id=1547687748007; vinfo_n_f_l_n3=8a0bceb0ce0859e1.1.0.1547687210316.0.1547687803983'
#     , 'Host': '3g.163.com'
#     , 'Referer': 'https://3g.163.com/touch/ent/?ver=c&clickfrom=index2018_header'
#     ,
#     'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36'
# }
# r = requests.get('https://3g.163.com/touch/reconstruct/article/list/BA10TA81wangning/0-10.html', headers = headers)
# r.encoding='utf-8'
# print(r.text)


for f_file in open("/Users/krison/PycharmProjects/SixSpider/article/中国知网目录.txt", "r", encoding='utf-8'):
    if len(f_file.split("|*|")) < 2:
        print("小于2，{}".format(f_file))
        continue
    if len(f_file.split("|*|")) > 3:
        print("大于3，{}".format(f_file))
