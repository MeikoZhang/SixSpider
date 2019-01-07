from zlib import crc32
import binascii
from zlib import crc32
import random
import requests
from bs4 import BeautifulSoup
import urllib.parse
import base64
import traceback


headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'Ecp_notFirstLogin=vmsGV7; Ecp_ClientId=5190107132200887006; Ecp_IpLoginFail=190107180.154.19.189; ASP.NET_SessionId=ms2sgoedxyhq4wijks2krclk; SID_kns=123112; SID_crrs=125132; SID_klogin=125141; RsPerPage=20; _pk_ref=%5B%22%22%2C%22%22%2C1546838613%2C%22http%3A%2F%2Fwww.cnki.net%2F%3FUID%3DWEEvREcwSlJHSldTTEYzVDhsN3d3MVZPQmtrRHdsZXBsT2kwYkIvL2lQST0%3D%249A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!%26autoLogin%3D1%22%5D; _pk_ses=*; SID_krsnew=125131; cnkiUserKey=79c89227-9f6c-2235-67a5-4f435198b5a1; SID_kcms=124106; SID_knsdelivery=125121; KNS_SortType=; Ecp_lout=1; LID=; IsLogin=',
    'Host': 'kns.cnki.net',
    'Referer': 'http://kns.cnki.net/kns/brief/default_result.aspx',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36'
}
# dbCatalog=中国学术文献网络出版总库
# keyValue=顺尔宁 # %E9%A1%BA%E5%B0%94%E5%AE%81
keyValue = urllib.parse.quote('顺尔宁')
url = 'http://kns.cnki.net/kns/brief/brief.aspx?pagename=ASP.brief_default_result_aspx&isinEn=1&dbPrefix=SCDB' \
      '&dbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93' \
      '&ConfigFile=SCDBINDEX.xml&research=off&t=1546840215538&keyValue={}&S=1&sorttype='.format(keyValue)
r = requests.get(url, headers=headers)
r.encoding = 'utf-8'
# 这里指定解析器为html.parser（python默认的解析器），指定html文档编码为utf-8
soup = BeautifulSoup(r.text, 'html.parser', from_encoding='utf-8')
# print(type(soup))
# print(r.text)
# alinks = soup.find_all(attrs={'target': '_blank'})
alinks = soup.select('.fz14')
# print(alinks)
# print([x.text for x in alinks])
i = 0
for alink in alinks:
    i = i + 1
    # print(alink.text, alink['href'])
    download_url = 'http://kns.cnki.net{}'.format(alink['href'])
    # print(download_url)
    download_r = requests.get(download_url, headers=headers)
    download_r.encoding = 'utf-8'
    # print(download_r.text)
    download_soup = BeautifulSoup(download_r.text, 'html.parser', from_encoding='utf-8')
    download_a = download_soup.select('#pdfDown')
    if(download_a):
        print(i, alink.text, download_a[0]['href'])

# url1 = 'http://kns.cnki.net/kns/detail/detail.aspx?QueryID=16&CurRec=1&recid=&FileName=ZFYB201823065&DbName=CJFDTEMP&DbCode=CJFQ&yx=&pr=&URLID='
# r1 = requests.get(url1, headers=headers)
# print(r1.text)
