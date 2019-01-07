from zlib import crc32
import binascii
from zlib import crc32
import random
import requests
from bs4 import BeautifulSoup
import urllib.parse
import base64
import traceback
import time


headers={
    'Accept': 'application/json, text/javascript, */*; q=0.01'
    , 'Accept-Encoding': 'gzip, deflate'
    , 'Accept-Language': 'zh-CN,zh;q=0.9'
    , 'Connection': 'keep-alive'
    ,
    'Cookie': 'ASP.NET_SessionId=foiygopapmkibqdszq55qmw2; Hm_lvt_69fff6aaf37627a0e2ac81d849c2d313=1546844118; _qddaz=QD.8cpiis.3hs0de.jqlz1sgj; _qdda=3-1.dz4yr; _qddab=3-55hdxl.jqlz1sgl; _qddamta_4006385550=3-0; tencentSig=4597393408; cqvip_usersessionid=1c956e0a-71f5-4a9a-89bc-18087b63a262; __utma=164835757.1017260104.1546844159.1546844159.1546844159.1; __utmc=164835757; __utmz=164835757.1546844159.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmb=164835757.1.10.1546844159; PacketUser:AutoLogin=1; Hm_lpvt_69fff6aaf37627a0e2ac81d849c2d313=1546844621'
    , 'Host': 'www.cqvip.com'
    , 'Referer': 'http://www.cqvip.com/main/search.aspx'
    ,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    , 'X-Requested-With': 'XMLHttpRequest'
}

# keyValue=顺尔宁 %E9%A1%BA%E5%B0%94%E5%AE%81
keyValue = urllib.parse.quote('顺尔宁')
# ur1 = 'http://www.cqvip.com/data/main/search.aspx?action=so&tid=0&k=%E9%A1%BA%E8%80%B3%E5%AE%81&w=&o=&mn=&issn=&cnno=&rid=0&c=&gch=&cnt=&curpage=0&perpage=0&ids=&valicode=&_=1546853772212'
url = 'http://www.cqvip.com/data/main/search.aspx?action=so&tid=0&k={}&w=&o=&mn=&issn=&cnno=&rid=0&c=&gch=&cnt=&curpage={}&perpage=0&ids=&valicode=&_={}'.format(keyValue, 0, int(time.time()*1000))
r = requests.get(url, headers=headers)
r.encoding = 'utf-8'
# print(r.text)
r_json = r.json()
print(r_json)
# 这里指定解析器为html.parser（python默认的解析器），指定html文档编码为utf-8
soup = BeautifulSoup(r_json['message'], 'lxml', from_encoding='utf-8')
# alinks = soup.find_all(attrs={'target': '_blank'})
alinks = soup.select('.cqvip-log-click')
print(alinks)

i = 0
for alink in alinks:
    i = i + 1
    # print(i, alink.text, alink['href'])
    download_url = 'http://www.cqvip.com{}'.format(alink['href'])
    #     # # print(download_url)
    download_r = requests.get(download_url, headers=headers)
    download_r.encoding = 'utf-8'
    # print(download_r.text)
    download_soup = BeautifulSoup(download_r.text, 'html.parser', from_encoding='utf-8')
    download_a = download_soup.select('.download')
    if(download_a):
        print(i, alink.text, 'http://www.cqvip.com{}'.format(download_a[0]['href']))

# url1 = 'http://kns.cnki.net/kns/detail/detail.aspx?QueryID=16&CurRec=1&recid=&FileName=ZFYB201823065&DbName=CJFDTEMP&DbCode=CJFQ&yx=&pr=&URLID='
# r1 = requests.get(url1, headers=headers)
# print(r1.text)
