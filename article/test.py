
from zlib import crc32
import binascii
from zlib import crc32
import random
import requests
from bs4 import BeautifulSoup
import urllib.parse
import base64
import traceback
import os
import re
import urllib.parse



# 获取请求url域名
def get_host(url):
    pattern = re.compile(r'(.*?)://(.*?)/', re.S)
    response = re.search(pattern, url)
    if response:
        return {'header': str(response.group(1)).strip(), 'host': str(response.group(2)).strip()}
    else:
        return None


file_name_re = re.compile(r".*?([\u4E00-\u9FA5]+\.pdf)")

download_url = r"http://aws.download.cqvip.com/DownPaper.dll?DownCurPaper&CD=2020&Info=BIGDABABBHAOAFAFAPAAHBBPBHBIACABAHABAIAHANAHAAAIBIABADADAJAHAG&FILE=043/001/7100875058.pdf&FileName=%e7%b3%a0%e9%85%b8%e8%8e%ab%e7%b1%b3%e6%9d%be%e9%bc%bb%e5%96%b7%e5%89%82%e8%81%94%e5%90%88%e5%ad%9f%e9%b2%81%e6%96%af%e7%89%b9%e9%92%a0%e6%b2%bb%e7%96%97%e5%8f%98%e5%ba%94%e6%80%a7%e9%bc%bb%e7%82%8e%e7%9a%84%e7%96%97%e6%95%88%e5%88%86%e6%9e%90.pdf"
file_name = download_url.split('FileName=')[1]
print(file_name)

if not file_name_re.match(file_name):
    file_name = urllib.parse.unquote(file_name)
    if not file_name_re.match(file_name):
        print('\t文件名获取失败，无法生成文件名 ..... {}'.format(file_name))

if file_name:
    file2write = os.path.join(r"C:/Users/krison/Downloads/", file_name)
    print(file2write)

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        , 'Accept-Encoding': 'gzip, deflate'
        , 'Accept-Language': 'zh-CN,zh;q=0.9'
        , 'Connection': 'keep-alive'
        , 'Host': get_host(download_url)['host']
        , 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }
    print(headers)

    f = requests.get(download_url, headers=headers)
    print(f.headers)
    with open(file2write, "wb") as code:
        code.write(f.content)
        # 更新目录
    print('文件下载完成 ... {}'.format(file2write))

