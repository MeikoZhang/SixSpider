# coding=gbk

import requests
from bs4 import BeautifulSoup
import time, os, shutil, logging
import http.cookiejar as HC
import random
import traceback
import urllib
from urllib import parse
from numpy import random
import re
import json
from urllib.parse import quote

# 登陆信息
data = {
    'userName': 'sherry.huang@goal-noah.com',
    'pwd': '33530912'
}

# 下载文件存储目录
file_dir = r"D:\文档\中国知网"

HEADER = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Host':
            'kns.cnki.net',
            'Connection':
            'keep-alive',
            'Cache-Control':
            'max-age=0',
        }

# 获取cookie
BASIC_URL = 'http://kns.cnki.net/kns/brief/result.aspx'
# 利用post请求先行注册一次
SEARCH_HANDLE_URL = 'http://kns.cnki.net/kns/request/SearchHandler.ashx'
# 发送get请求获得文献资源
GET_PAGE_URL =
# 下载的基础链接
DOWNLOAD_URL = 'http://kns.cnki.net/kns/'
# 切换页面基础链接
CHANGE_PAGE_URL = 'http://kns.cnki.net/kns/brief/brief.aspx'

# 请求的全局session
session = requests.Session()
# 保持会话
session.get('http://kns.cnki.net/kns/brief/result.aspx', headers=HEADER)
cookie_path = os.path.join(os.getcwd(), 'article-cnki-cookie.txt')


def login():
    # 多步登陆获取完整cookie
    session.cookies.clear()
    session.cookies.save()
    session.get(
        'http://kns.cnki.net/kns/brief/result.aspx?dbprefix=SCDB&crossDbcodes=CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',
        headers=HEADER)
    # cookie新增SID_klogin
    session.get('http://kns.cnki.net/KLogin/Request/GetKFooter.ashx', headers=HEADER)
    r = session.get('http://login.cnki.net/TopLogin/api/loginapi/Login?isAutoLogin=true&'
                    + urllib.parse.urlencode(data) + '&_=' + str(int(time.time() * 1000)))
    user_info = json.loads(r.text[1: -1])
    if user_info.get('IsSuccess'):
        print('登陆成功 ... ' + json.dumps(user_info))
    else:
        print('登陆失败 ... ' + json.dumps(user_info))


def get_total(key):
    static_post_data = {
        'action': '',
        'NaviCode': '*',
        'ua': '1.21',
        'isinEn': '1',
        'PageName': 'ASP.brief_default_result_aspx',
        'DbPrefix': 'SCDB',
        'DbCatalog': '中国学术期刊网络出版总库',
        'ConfigFile': 'CJFQ.xml',
        'db_opt': 'CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',  # 搜索类别（CNKI右侧的）
        'db_value': '中国学术期刊网络出版总库',
        'year_type': 'echar',
        'his': '0',
        'db_cjfqview': '中国学术期刊网络出版总库,WWJD',
        'db_cflqview': '中国学术期刊网络出版总库',
        '__': time.asctime(time.localtime()) + ' GMT+0800 (中国标准时间)',
        'expertvalue': key,
        'publishdate_from': '2018-12-24'
    }

    # 将固定字段与自定义字段组合
    post_data = static_post_data
    # 必须有第一次请求，否则会提示服务器没有用户
    first_post_res = session.post(
        SEARCH_HANDLE_URL, data=post_data, headers=HEADER)
    # get请求中需要传入第一个检索条件的值
    get_result_url = 'http://kns.cnki.net/kns/brief/brief.aspx?pagename=' + first_post_res.text + '&t=1544249384932&keyValue=&S=1&sorttype='
    # 检索结果的第一个页面
    second_get_res = session.get(get_result_url, headers=HEADER)
    change_page_pattern_compile = re.compile(r'.*?pagerTitleCell.*?<a href="(.*?)".*')
    change_page_url = re.search(change_page_pattern_compile, second_get_res.text).group(1)
    parse_page(
        self.pre_parse_page(second_get_res.text), second_get_res.text)







    # 设置查询条件，请求一次
    total_url = 'http://kns.cnki.net/kns/request/SearchHandler.ashx'
    r_param = session.post(total_url, data=s_handle_data, headers=headers)
    param_dict = dict(parse.parse_qsl("pagename=" + r_param.text))
    print(param_dict)

    # 获取查询列表
    r_list_doc = session.get(
        'http://kns.cnki.net/kns/brief/brief.aspx?pagename=' + r_param.text + '&t='
        + str(int(time.time() * 1000)) + '&keyValue=&S=1&sorttype=',
        headers=headers)
    r_list_doc.encoding = 'utf-8'
    # print(r_list_doc.text)

    soup = BeautifulSoup(r_list_doc.text, 'lxml', from_encoding='utf-8')
    result = soup.select('#resultcount')
    result_count = int(result[0].attrs['value'])
    page_size = 20
    page_count = int((result_count + page_size - 1) / page_size)
    print("找到 {} 条结果，共分 {} 页".format(result_count, page_count))

    # 开始分页下载
    for page_num in range(2):
        get_list(key, page_num + 1, param_dict)
        time.sleep(2)
    print(">>>>>>>>>>程序执行完成 .................")


def get_list(key, page_num, param_dict):
    page_data = {
        'curpage': page_num
        , 'RecordsPerPage': '20'
        , 'QueryID': random.random_integers(1, 9)
        , 'ID': ''
        , 'turnpage': page_num - 1 if page_num - 1 > 0 else page_num + 1
        , 'tpagemode': 'L'
        , 'Fields': ''
        , 'DisplayMode': 'listmode'
        , 'dbPrefix': param_dict['dbPrefix']
        , 'PageName': param_dict['pagename']
        , 'isinEn': param_dict['isinEn']
    }
    # 获取查询列表
    list_url = 'http://kns.cnki.net/kns/brief/brief.aspx?' + urllib.parse.urlencode(page_data)
    r_list_doc = session.get(list_url, headers=headers)
    r_list_doc.encoding = 'utf-8'
    # print(r_list_doc.text)

    soup = BeautifulSoup(r_list_doc.text, 'lxml', from_encoding='utf-8')
    headers['Referer'] = list_url
    trs = soup.select('.GridTableContent tr')
    # 去除标题栏
    for tr in trs[1:]:
        tds = tr.select('td')
        # 序号
        tr_order = tds[0].text

        # 标题名
        tr_title = tds[1].select('a')[0].text

        # 作者
        tr_author = ""
        authors_a = tds[2].select('a')
        for author_a in authors_a:
            tr_author = tr_author + "_" + author_a.text

        # 发表时间
        tr_time = tds[4].text

        # 数据库
        tr_db = tds[5].text

        # 下载链接 http://kns.cnki.net/kns/download.aspx
        tr_down_url = tds[7].select('a')[0].attrs['href']

        # 文件类型
        type = tds[8].select('a')[0].attrs['title']
        if type == "HTML阅读":
            tr_file_type = ".pdf"
        elif type == "阅读":
            tr_file_type = ".caj"
        else:
            tr_file_type = ""
            print("文件类型未知，原文类型{}".format(type))

        # 输出表格列表
        print(tr_order, tr_title, tr_author, tr_file_type, tr_time.strip(), tr_db.strip())
        # 文件重复去重
        file_will_write = os.path.join(file_dir, tr_title + tr_author + tr_file_type)
        if os.path.exists(file_will_write):
            print('\t文件已存在 ... {}'.format(file_will_write))
            continue
        else:
            print('\t文件不存在，开始下载 ... {}'.format(file_will_write))
            print('\t下载链接 ... {}'.format('http://kns.cnki.net/kns' + tr_down_url[2:]))
            download(file_will_write, 'http://kns.cnki.net/kns' + tr_down_url[2:])
            time.sleep(2)
            print('\t文件下载文成')


def download(file_name, down_url):
    down_headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Connection': 'keep-alive', 'Host': 'nvsm.cnki.net',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
                    }
    down_cookie_str = ""
    for cookie in session.cookies:
        down_cookie_str = down_cookie_str + cookie.name + "=" + cookie.value + ";"
    print(down_cookie_str)
    down_headers['Cookie'] = 'Ecp_ClientId=6190110100400259207; Ecp_IpLoginFail=190110180.154.19.189; cnkiUserKey=4b9d957f-13fe-14e8-d403-3e23572f9704; Ecp_lout=1; LID=WEEvREcwSlJHSldTTEYzVDhsN3d3MVE5VHVvSUlqLzBCZEQrbUdPS0dIaz0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!; Ecp_session=1; ASP.NET_SessionId=mxjqbr3lvwl3xccwtevicvwd; SID_kns=011115; SID=011101; KNS_SortType=; RsPerPage=20; _pk_ref=%5B%22%22%2C%22%22%2C1547198945%2C%22http%3A%2F%2Fwww.cnki.net%2F%22%5D; _pk_ses=*'
    # down_headers['Cookie'] = down_cookie_str

    r_d = session.get(down_url, headers=down_headers, allow_redirects=False)
    loc_pubdownload = r_d.headers.get('Location', None)

    # 这一步验证是否已支付，如果未支付，该步骤则返回的是页面，没有location
    if loc_pubdownload:
        # print(session.cookies)
        r_pubdownload = session.get(loc_pubdownload, headers=down_headers, allow_redirects=False)
        r_pubdownload.encoding = 'utf-8'
        # print(r_pubdownload.status_code)
        # print(r_pubdownload.text)
        print(r_pubdownload.headers)
        print(r_pubdownload.text)

        if r_pubdownload.status_code == 200:
            # 返回的是页面
            print('文章未支付，支付中 ...')
            time.sleep(2)
            pay_data = {
                'pid': 'cjfq',
                'uid': requests.utils.dict_from_cookiejar(session.cookies).get('LID')
            }
            r_pay = session.post(loc_pubdownload, data=pay_data, headers=down_headers, allow_redirects=False)
            r_pay.encoding = 'utf-8'
            if r_pay.headers.get('Location', None):
                print('文章支付完成 ...{}'.format(r_pay.headers))
                # 返回的是文件流
                down_headers['Host'] = get_host(r_pay.headers['Location'])['host']
                r_do = session.get(r_pay.headers['Location'], headers=down_headers, allow_redirects=False)
                down_headers['Host'] = get_host(r_do.headers['Location'])['host']
                r_new = session.get(r_do.headers['Location'], headers=down_headers, allow_redirects=False)

                save_file(file_name, r_new)
            else:
                print('文章支付无效 ...{}'.format(r_pay.headers))
                print('文章链接 ...{}'.format('http://kns.cnki.net/kns' + down_url[2:]))
                # print(r_pay.text)
                exit(1)
        else:
            # 返回的是文件流
            print('文章不需要支付，直接下载 ...')
            down_headers['Host'] = get_host(r_pubdownload.headers['Location'])['host']
            r_do = session.get(r_pubdownload.headers['Location'], headers=down_headers, allow_redirects=False)
            down_headers['Host'] = get_host(r_do.headers['Location'])['host']
            r_new = session.get(r_do.headers['Location'], headers=down_headers, allow_redirects=False)

            save_file(file_name, r_new)
    else:
        print('下载文章连接无效，{}'.format(loc_pubdownload))


# 获取请求url域名
def get_host(url):
    pattern = re.compile(r'(.*?)://(.*?)/', re.S)
    response = re.search(pattern, url)
    if response:
        return {'header': str(response.group(1)).strip(), 'host': str(response.group(2)).strip()}
    else:
        return None


def save_file(file_name, response):
    file2write = os.path.join(file_dir, file_name)
    if os.path.exists(file2write):
        print('\t文件已存在 ... {}'.format(file2write))
    else:
        # 下载内容
        with open(file2write, "wb") as code:
            code.write(response.content)
        print('\t文件下载完成 ... {}'.format(file2write))


login()
get_total("FT=依托考昔 OR FT=安康信 OR FT=卡泊芬净 OR FT=科赛斯 OR FT=氯沙坦 OR FT=络沙坦 OR FT=洛沙坦 OR FT=科素亚 OR FT=阿仑膦酸钠 OR FT=阿伦磷酸钠 OR FT=福善美 OR FT=氯沙坦钾氢氯噻嗪 OR FT=海捷亚 OR FT=厄他培南 OR FT=艾他培南 OR FT=怡万之 OR FT=非那雄胺 OR FT=非那司提 OR FT=非那甾胺 OR FT=保法止 OR FT=非那雄胺 OR FT=非那司提 OR FT=非那甾胺 OR FT=保列治 OR FT=依那普利 OR FT=恩纳普利 OR FT=苯酯丙脯酸 OR FT=悦宁定 OR FT=卡左双多巴 OR FT=息宁 OR FT=孟鲁司特 OR FT=孟鲁斯特 OR FT=顺尔宁 OR FT=顺耳宁 OR FT=亚胺培南 OR FT=亚安培南 OR FT=泰能 OR FT=辛伐他汀 OR FT=新伐他汀 OR FT=舒降之 OR FT=舒降脂 OR FT=拉替拉韦 OR FT=艾生特 OR FT=23价肺炎球菌多糖疫苗 OR FT=纽莫法 OR FT=甲型肝炎灭活疫苗(人二倍体细胞) OR FT=人二倍体甲型肝炎灭活疫苗 OR FT=维康特 OR FT=西格列汀 OR FT=西他列汀 OR FT=捷诺维 OR FT=西格列汀二甲双胍 OR FT=西格列汀二甲双胍 OR FT=捷诺达 OR FT=依折麦布 OR FT=依替米贝 OR FT=益适纯 OR FT=阿仑膦酸钠维D3 OR FT=福美加 OR FT=福美佳 OR FT=阿瑞匹坦 OR FT=阿瑞吡坦 OR FT=意美 OR FT=地氯雷他定 OR FT=恩理思")
# download("基于江南原生态理念的水居民宿设计——以原舍·阅水民宿设计为例.pdf",
#          "http://kns.cnki.net/kns/download.aspx?filename=s9Ge4EVaSNXewMFT3p2Z2RjdSBnW5Q2L5cVS4p2UIZTb6Flcp92dnJGepBTSGZUZthWQWpXYkFVY5x2QzoWWjZ2ZEF3QSNlduRjS6NlZXdkMmhDWFB1Y4kma0MmUGhGd4MUMnFXNnB1an9maxMGMVN3ZIljbqdUT&tablename=CJFDPREP")
# download("辛伐他汀片体外溶出一致性评价方法的建立_郭志渊_谢华_袁军.caj",
#          "http://nvsm.cnki.net/kns/download.aspx?filename=4RFd1sGcB9Ub3gWbCJjYHNTYM92TaRkZvd3U6pVZVF0bLZVZaNEUU9SVnlWVLFERvQnRhdlWYNkQS5mQJpEb3siUM1EeE9kVhJVcnRGZ5l0dwwkMwUVV210NtRHa6FnTNdFdIl0MG1mWJVVTZRGULRUQrdlbDZHR&tablename=CAPJDAY")
