import requests
from bs4 import BeautifulSoup
import time
import os
import urllib


headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01'
    , 'Accept-Encoding': 'gzip, deflate'
    , 'Accept-Language': 'zh-CN,zh;q=0.9'
    , 'Connection': 'keep-alive'
    ,
    'Cookie': 'ASP.NET_SessionId=foiygopapmkibqdszq55qmw2; Hm_lvt_69fff6aaf37627a0e2ac81d849c2d313=1546844118; _qddaz=QD.8cpiis.3hs0de.jqlz1sgj; tencentSig=4597393408; cqvip_usersessionid=1c956e0a-71f5-4a9a-89bc-18087b63a262; PacketUser:AutoLogin=1; User:SUID:UserID=0; User:SUID=; _qdda=3-1.48m3ma; _qddab=3-its12y.jqndanpu; User=_uid=19028277%2427738173EE21D5737D380371B89E9A2A&_uutid=1%24DCC0C88A6597BFF91D8217A08210E402&_uunid=3%247E3FDE4AFCF8B4AFD9A2D917A54A4075&_ultid=2%24EFBC4C6D6AD4D7056B5B65E5451D5EAF&_uatid=0%2448DF86E51FCF5BD310DC2E440743581A&_uqkdy=0%24C6301CB68C5534157BA315539287132D&_upu=0%24CECCE0C6BD78DFEDB933C2BF33984F97&_upc=%24AAD5936EA2751C571FB7891B01129A16&_suid=%249425A0A64713DBCDBE3F688BAF8A2975&_uun=447229719%40qq.com&_unn=447229719%40qq.com&_uem=447229719%40qq.com&_ugid=0&_uoid=0; UM_distinctid=1682c6163253b7-0afaeb3a5e2d5c-b781636-100200-1682c616327195; _ga=GA1.2.769807723.1546931676; _gid=GA1.2.1572456567.1546932807; __utmt=1; __utma=164835757.769807723.1546931676.1546933219.1546933219.1; __utmc=164835757; __utmz=164835757.1546933219.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt_vip2=1; __utmb=164835757.1.10.1546933219; Hm_lpvt_69fff6aaf37627a0e2ac81d849c2d313=1546933219; _qddamta_4006385550=3-0'
    , 'Host': 'www.cqvip.com'
    , 'Referer': 'http://www.cqvip.com/main/search.aspx'
    ,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    , 'X-Requested-With': 'XMLHttpRequest'
}

# 登陆信息
data = {
    'Username': '447229719@qq.com',
    'Password': '33530912'
}

session = requests.Session()
# session_r = session.post('http://www.cqvip.com/User/', data, headers=headers)
print('登陆完成，获取session，设置cookies ...... ')


# 获取搜索列表
def get_list(key=None):
    # keyValue=顺尔宁 %E9%A1%BA%E5%B0%94%E5%AE%81
    if not key:
        print('没有设置关键词！！！')
        return

    key_value = urllib.parse.quote(key)
    # 获取搜索列表
    url = 'http://www.cqvip.com/data/main/search.aspx?action=so&tid=0&k={}&w=&o=&mn=&issn=&cnno=&rid=0&c=&gch=&cnt=&curpage={}&perpage=0&ids=&valicode=&_={}'.format(
        key_value, 0, int(time.time() * 1000))
    r = session.get(url, headers=headers)
    r.encoding = 'utf-8'
    # print(r.text)
    r_json = r.json()
    # print(r_json)
    # 这里指定解析器为html.parser（python默认的解析器），指定html文档编码为utf-8
    soup = BeautifulSoup(r_json['message'], 'lxml', from_encoding='utf-8')
    # alinks = soup.find_all(attrs={'target': '_blank'})
    alinks = soup.select('.cqvip-log-click')
    # print(alinks)
    i = 0
    for alink in alinks:
        i = i + 1
        print(i, alink.text, alink['href'])
        # if alink['href'] == '/QK/87088X/201004/34675601.html':
        #     get_download_url(alink)
        # print(i, alink.text, get_download_url(alink))
        down_url = get_download_url(alink)
        if down_url:
            print('下载文章链接 {}'.format(down_url))
            download(down_url)
        time.sleep(5)


def get_download_url(alink):
    # print(i, alink.text, alink['href'])
    download_url = 'http://www.cqvip.com{}'.format(alink['href'])
    #     # # print(download_url)
    download_r = session.get(download_url, headers=headers)
    download_r.encoding = 'utf-8'
    download_soup = BeautifulSoup(download_r.text, 'html.parser', from_encoding='utf-8')
    download_a = download_soup.select('.download')
    detail_headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        , 'Accept-Encoding': 'gzip, deflate'
        , 'Accept-Language': 'zh-CN,zh;q=0.9'
        , 'Cache-Control': 'max-age=0'
        , 'Connection': 'keep-alive'
        , 'Host': 'www.cqvip.com'
        , 'Upgrade-Insecure-Requests': '1'
        , 'Cookie': 'ASP.NET_SessionId=foiygopapmkibqdszq55qmw2; Hm_lvt_69fff6aaf37627a0e2ac81d849c2d313=1546844118; _qddaz=QD.8cpiis.3hs0de.jqlz1sgj; tencentSig=4597393408; cqvip_usersessionid=1c956e0a-71f5-4a9a-89bc-18087b63a262; PacketUser:AutoLogin=1; User:SUID:UserID=0; User:SUID=; _qdda=3-1.48m3ma; _qddab=3-its12y.jqndanpu; User=_uid=19028277%2427738173EE21D5737D380371B89E9A2A&_uutid=1%24DCC0C88A6597BFF91D8217A08210E402&_uunid=3%247E3FDE4AFCF8B4AFD9A2D917A54A4075&_ultid=2%24EFBC4C6D6AD4D7056B5B65E5451D5EAF&_uatid=0%2448DF86E51FCF5BD310DC2E440743581A&_uqkdy=0%24C6301CB68C5534157BA315539287132D&_upu=0%24CECCE0C6BD78DFEDB933C2BF33984F97&_upc=%24AAD5936EA2751C571FB7891B01129A16&_suid=%249425A0A64713DBCDBE3F688BAF8A2975&_uun=447229719%40qq.com&_unn=447229719%40qq.com&_uem=447229719%40qq.com&_ugid=0&_uoid=0; UM_distinctid=1682c6163253b7-0afaeb3a5e2d5c-b781636-100200-1682c616327195; _ga=GA1.2.769807723.1546931676; _gid=GA1.2.1572456567.1546932807; __utmt=1; __utma=164835757.769807723.1546931676.1546933219.1546933219.1; __utmc=164835757; __utmz=164835757.1546933219.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt_vip2=1; __utmb=164835757.1.10.1546933219; Hm_lpvt_69fff6aaf37627a0e2ac81d849c2d313=1546933219; _qddamta_4006385550=3-0'
        ,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    if download_a:
        # print(alink.text, 'http://www.cqvip.com{}'.format(download_a[0]['href']))
        detail_url = 'http://www.cqvip.com{}'.format(download_a[0]['href'])
        print(detail_url)
        detail_r = session.get(detail_url, headers=detail_headers)
        detail_r.encoding = 'utf-8'
        detail_soup = BeautifulSoup(detail_r.text, 'lxml', from_encoding='utf-8')
        detail_download = detail_soup.select('.getfile li a')
        if detail_download:
            # 下载链接
            download_file_url = detail_download[0]['href']
            print(download_file_url)
            return download_file_url
        else:
            detail_pay = detail_soup.find_all(attrs={'value': '帐户支付'})
            if detail_pay:
                # 支付
                # print(detail_pay)
                print('需要支付确认！！！')
                pay_url = 'http://www.cqvip.com/main/confirmpost.aspx'
                pay_id = detail_soup.find_all(attrs={'name': 'id'})
                print('payid', pay_id[0]['value'])
                pay_data = {
                    'mid': '1',
                    'id': pay_id[0]['value'],
                    'p2w': '0'
                }
                pay_r = session.post(pay_url, data=pay_data, headers=detail_headers)
                # print(pay_r.text)
                print('支付完成 ...')
                pay_soup = BeautifulSoup(pay_r.text, 'lxml', from_encoding='utf-8')
                pay_download = pay_soup.select('.getfile li a')
                if pay_download:
                    # 下载链接
                    pay_download_file_url = pay_download[0]['href']
                    print(pay_download_file_url)
                    return pay_download_file_url
        print(download_url, '未找到相关文章...')
        return None


def download(download_url):
    # download_url='http://ts1.download.cqvip.com/DownPaper.dll?DownCurPaper&CD=2002YY08&Info=BPGEAGBHABACAAAOAHGOBOBHBGAEAHAOAJAEAHAOBGACAHAGAIAHAA&FILE=004/004/6189266.pdf&FileName=%cb%b3%b6%fb%c4%fe%d6%ce%c1%c6%bc%b0%d4%a4%b7%c0%bf%c8%cb%d4%b1%e4%d2%ec%d0%d4%cf%f8%b4%ad%b5%c4%c1%c6%d0%a7%b9%db%b2%ec.pdf'
    # urllib.urlretrieve(download_url, os.path.join("D:/文档", "11.tar.bz2"))
    # 把下载地址发送给requests模块
    f = requests.get(download_url)
    # print(f.headers)
    # 检测编码
    # print(chardet.detect(bytes(f.headers['Content-Disposition'], encoding="iso-8859-1")))
    # print(str(bytes(f.headers['Content-Disposition'], encoding="iso-8859-1"), encoding="GB2312"))
    file_name_str = str(bytes(f.headers['Content-Disposition'], encoding="iso-8859-1"), encoding="GB2312")
    fileName = file_name_str.split('filename=')[1]
    fileName = fileName.replace('"', '').replace("'", "")
    print(fileName)
    # 下载文件
    with open(os.path.join("D:/文档", fileName), "wb") as code:
        code.write(f.content)


get_list('顺尔宁')



