# coding=gbk

import requests
from bs4 import BeautifulSoup
import time
import os
import sys
import http.cookiejar as HC
import random
import traceback
import urllib
from urllib import parse
from numpy import random
import re
import json
import logging
from logging.handlers import TimedRotatingFileHandler

# base_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
base_path = r"E:\文档"

log_fmt = '%(asctime)s\tFile \"%(filename)s\",line %(lineno)s\t%(levelname)s: %(message)s'
formatter = logging.Formatter(log_fmt)

# 控制台log配置
# 默认是sys.stderr
log_console_handler = logging.StreamHandler(sys.stdout)
log_console_handler.setLevel(logging.INFO)
log_console_handler.setFormatter(formatter)

# 文件log配置
log_file_handler = TimedRotatingFileHandler(filename=os.path.join(base_path, r"article\cnki_run.log"), when="D", interval=1, backupCount=7, encoding='utf-8')
log_file_handler.setLevel(logging.INFO)
log_file_handler.setFormatter(formatter)
log_file_handler.suffix = "%Y-%m-%d_%H-%M.log"
log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log$")

# log初始化
log = logging.getLogger()
log.setLevel(logging.INFO)
log.addHandler(log_file_handler)
log.addHandler(log_console_handler)


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    , 'Accept-Encoding': 'gzip, deflate'
    , 'Accept-Language': 'zh-CN,zh;q=0.9'
    , 'Cache-Control': 'max-age=0'
    , 'Connection': 'keep-alive'
    , 'Host': 'kns.cnki.net'
    , 'Upgrade-Insecure-Requests': '1'
    ,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

# 登陆信息
data = {
    'userName': 'sherry.huang@goal-noah.com',
    'pwd': '33530912'
}

# 下载文件存储目录
# file_dir = os.path.join(base_path, "中国知网")
cur_day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
if cur_day > '2019-02-01':
    exit()

file_dir = os.path.join(base_path, "中国知网", cur_day)
if os.path.exists(file_dir):
    print("目录{}已存在，下载文件中...".format(file_dir))
else:
    print("目录{}不存在，创建该目录...".format(file_dir))
    os.mkdir(file_dir)

file_dir_files = os.listdir(file_dir)
# 已下载文件列表
file_m = os.path.join(base_path, "中国知网目录.txt")
files_m = []

# 其他目录列表 - 标题 数组
other_list = []

# 请求的全局session
session = requests.Session()

cookie_path = os.path.join(base_path, r"article\article-cnki-cookie.txt")

session.cookies = HC.MozillaCookieJar(filename=cookie_path)

session.get('http://www.cnki.net/', headers=headers)
session.get('http://kns.cnki.net/kns/brief/result.aspx?dbprefix=SCDB&crossDbcodes=CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',
            headers=headers)
session.get('http://kns.cnki.net/kns/brief/result.aspx', headers=headers)


def load_list():
    # 加载自己目录
    files_m.clear()
    for f_file in open(file_m, "r", encoding='utf-8'):
        if len(f_file.split(",")) < 2:
            continue
        # print(f_file.strip())
        files_m.append(f_file.split(",")[1])
        # print(">>")

    # 加载其他目录
    other_list.clear()
    files = os.listdir(base_path)
    for file in files:
        if file.find("目录") > 0 and file != "中国知网目录.txt":
            for f_file in open(os.path.join(base_path, file), "r", encoding='utf-8'):
                if len(f_file.split(",")) < 2:
                    continue
                other_list.append(f_file.split(",")[0])


def login():
    # 多步登陆获取完整cookie
    session.get(
        'http://kns.cnki.net/kns/brief/result.aspx?dbprefix=SCDB&crossDbcodes=CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',
        headers=headers)
    # cookie新增SID_klogin
    session.get('http://kns.cnki.net/KLogin/Request/GetKFooter.ashx', headers=headers)
    if int(time.time()) > 1548950400:
        exit(0)
    r = session.get('http://login.cnki.net/TopLogin/api/loginapi/Login?isAutoLogin=false&'
                    + urllib.parse.urlencode(data) + '&_=' + str(int(time.time() * 1000)))
    user_info = json.loads(r.text[1: -1])
    if user_info.get('IsSuccess'):
        log.info('登陆成功 ... ' + json.dumps(user_info))
        login_header = {
            'Host': 'login.cnki.net',
            'Pragma': 'no-cache',
            'Referer': 'http://kns.cnki.net/kns/brief/result.aspx?dbprefix=SCDB&crossDbcodes=CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD'
        }
        session.post('http://kns.cnki.net/kns/Loginid.aspx', data={'uid': user_info.get('Uid')},
                     headers={**headers, **login_header})
        session.cookies.save()
    else:
        log.error('登陆失败 ... ' + json.dumps(user_info))
        exit('登陆失败 ... ')

    try:
        session.cookies.load(ignore_discard=True, ignore_expires=True)
        cookie_str = ""
        for cookie in session.cookies:
            # print(cookie.name, cookie.value)
            cookie_str = cookie_str + cookie.name + "=" + cookie.value + ";"
        cookie_str = cookie_str + 'cnkiUserKey=09335600-3228-c095-c5cd-b1459792ec88'
        # print(cookie_str)
        headers['Cookie'] = cookie_str

    except Exception as e:
        log.error('未找到cookies文件')
        log.error(traceback.format_exc())


def get_total(key):
    load_list()
    headers[
        'Referer'] = 'Referer: http://kns.cnki.net/kns/brief/result.aspx?dbprefix=SCDB&crossDbcodes=CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD'

    s_handle_data = {
        'action': ''
        , 'NaviCode': '*'
        , 'ua': '1.21'
        , 'isinEn': '1'
        , 'PageName': 'ASP.brief_result_aspx'
        , 'DbPrefix': 'SCDB'
        , 'DbCatalog': '中国学术文献网络出版总库'
        , 'ConfigFile': 'SCDB.xml'
        , 'db_opt': 'CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD'
        , 'expertvalue': key
        , 'publishdate_from': '2018-12-24'
        , 'his': '0'
        , '__': 'Thu Jan 10 2019 15:05:25 GMT+0800 (中国标准时间)'
    }
    # 设置查询条件，请求一次
    total_url = 'http://kns.cnki.net/kns/request/SearchHandler.ashx'
    r_param = session.post(total_url, data=s_handle_data, headers=headers)
    param_dict = dict(parse.parse_qsl("pagename=" + r_param.text))

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
    log.info("找到 {} 条结果，共分 {} 页".format(result_count, page_count))

    # 开始分页下载
    for page_num in range(page_count):
        get_list(key, page_num + 1, param_dict)
        time.sleep(2)
    log.info(">>>>>>>>>>程序执行完成 .................")


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
        tr_authors = ""
        authors_a = tds[2].select('a')
        for author_a in authors_a:
            tr_authors = tr_authors + "_" + author_a.text
        # 首作
        tr_author = ""
        if len(authors_a) > 0:
            tr_author = authors_a[0].text

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
            log.info("文件类型未知，原文类型{}".format(type))

        # 输出表格列表
        log.info("{},{},{},{},{},{}".format(tr_order, tr_title, tr_author, tr_file_type, tr_time.strip(), tr_db.strip()))
        # 文件重复去重
        file_will_write = os.path.join(file_dir, tr_title)

        if_down = True
        # 相同网站文件重复去重-标题名加作者
        if tr_title+"_"+tr_author in files_m:
            log.info('\t文件已存在当前网站目录列表 ... {}'.format(os.path.join(file_dir, tr_title)))
            if_down = False

        # 不同网站重复去重-根据标题
        if tr_title in other_list:
            log.info('\t文件已存在其他网站目录列表 ... {}'.format(os.path.join(file_dir, tr_title)))
            if_down = False

        # for f in file_dir_files:
        #     if f.startswith(tr_title):
        #         print('\t{},{}'.format(f, tr_title))
        #         print('\t文件已存在 ... {}'.format(os.path.join(file_dir, f)))
        #         if_down = False
        #         with open(file_m, "a") as fm:
        #             fm.write(tr_title + "," + os.path.join(file_dir, f) + "\n")
        #         continue
        if if_down:
            log.info('\t文件不存在，开始下载 ... {}'.format(file_will_write))
            download_url = 'http://kns.cnki.net/kns' + tr_down_url[2:] + '&dflag=pdfdown'
            log.info('\t下载链接 ... {}'.format(download_url))
            download(tr_title, tr_author, download_url)
            time.sleep(6)


def download(title, author, down_url):
    # print(down_url)
    down_headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
                    }
    down_cookie_str = ""
    for cookie in session.cookies:
        down_cookie_str = down_cookie_str + cookie.name + "=" + cookie.value + ";"
    # down_headers['Cookie'] = 'Ecp_ClientId=6190110100400259207; Ecp_IpLoginFail=190110180.154.19.189; cnkiUserKey=4b9d957f-13fe-14e8-d403-3e23572f9704; Ecp_lout=1; LID=WEEvREcwSlJHSldTTEYzVDhsN3d3MVE5VHVvSUlqLzBCZEQrbUdPS0dIaz0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!; Ecp_session=1; ASP.NET_SessionId=mxjqbr3lvwl3xccwtevicvwd; SID_kns=011115; SID=011101; KNS_SortType=; RsPerPage=20; _pk_ref=%5B%22%22%2C%22%22%2C1547198945%2C%22http%3A%2F%2Fwww.cnki.net%2F%22%5D; _pk_ses=*'
    down_headers['Cookie'] = down_cookie_str[:-1]
    # print_cookie()

    down_headers['Host'] = get_host(down_url)['host']
    r_d = session.get(down_url, headers=down_headers, allow_redirects=False)
    loc_pubdownload = r_d.headers.get('Location', None)

    # 这一步验证是否已支付，如果未支付，该步骤则返回的是页面，没有location
    if loc_pubdownload:
        # print(session.cookies)
        down_headers['Host'] = get_host(loc_pubdownload)['host']
        r_pubdownload = session.get(loc_pubdownload, headers=down_headers, allow_redirects=False)
        r_pubdownload.encoding = 'utf-8'
        # print(r_pubdownload.status_code)
        # print(r_pubdownload.text)

        if r_pubdownload.status_code == 200:
            # 返回的是页面
            log.info('\t文章未支付，支付中 ...')
            time.sleep(2)
            pay_data = {
                'pid': 'cjfq',
                'uid': requests.utils.dict_from_cookiejar(session.cookies).get('LID')
            }

            r_pay = session.post(loc_pubdownload, data=pay_data, headers=down_headers, allow_redirects=False)
            r_pay.encoding = 'utf-8'
            if r_pay.status_code == 302:
                log.info('\t文章支付完成 ...{}'.format(r_pay.headers))
                # 返回的是文件流
                # 循环直到r = 200, 重定向到最后的下载链接，
                r = r_pay
                try:
                    while r.status_code == 302:
                        r_location = r.headers.get('Location')
                        if str(r_location).startswith("http"):
                            down_headers['Host'] = get_host(r.headers.get('Location'))['host']
                        else:
                            r_location = "http://" + down_headers['Host'] + "/cjfdsearch/" + r_location
                        r = session.get(r_location, headers=down_headers, allow_redirects=False)
                except:
                    log.error(traceback.format_exc())
                    log.error(r.headers)
                    exit()

                # 保存文件
                save_file(title, author, r)
            else:
                log.error('\t文章支付无效 ...{}'.format(r_pay.headers))
                log.error('\t文章链接 ...{}'.format('http://kns.cnki.net/kns' + down_url[2:]))

        else:
            # 返回的是文件流
            log.info('\t文章不需要支付，直接下载 ...')
            # 循环直到r = 200, 重定向到最后的下载链接
            r = r_pubdownload
            try:
                while r.status_code == 302:
                    r_location = r.headers.get('Location')
                    if str(r_location).startswith("http"):
                        down_headers['Host'] = get_host(r.headers.get('Location'))['host']
                    else:
                        r_location = "http://" + down_headers['Host'] + "/cjfdsearch/" + r_location
                    r = session.get(r_location, headers=down_headers, allow_redirects=False)
            except:
                log.error(traceback.format_exc())
                log.error(r.headers)
                exit()

            # 保存文件
            save_file(title, author, r)
    else:
        log.error('\t下载文章连接无效，{}'.format(loc_pubdownload))


# 获取请求url域名
def get_host(url):
    pattern = re.compile(r'(.*?)://(.*?)/', re.S)
    response = re.search(pattern, url)
    if response:
        return {'header': str(response.group(1)).strip(), 'host': str(response.group(2)).strip()}
    else:
        return None


def save_file(title, author, response):
    if response.headers.get('Content-Disposition'):
        # 检测编码, 获取header中文文件名
        file_name_str = str(bytes(response.headers['Content-Disposition'], encoding="iso-8859-1"), encoding="GBK")
        file_name = file_name_str.split('filename=')[1]
        # print(file_name)

        file2write = os.path.join(file_dir, file_name)
        if os.path.exists(file2write):
            log.info('\t文件已存在 ... {}'.format(file2write))
            with open(file_m, "a", encoding='utf-8') as fm:
                fm.write("{},{},{}\n".format(title, title+"_"+author, file2write))
        else:
            # 下载内容
            with open(file2write, "wb") as code:
                code.write(response.content)
                log.info('\t文件下载完成 ... {}'.format(file2write))
            with open(file_m, "a", encoding='utf-8') as fm:
                fm.write("{},{},{}\n".format(title, title+"_"+author, file2write))

    else:
        log.error('\t文件无法下载 ... {}'.format(response.headers))
        log.error(response.text)


def print_cookie():
    for cookie in session.cookies:
        log.info(cookie.name, cookie.value)


login()
log.info("》》》》》》》》》查询第一组关键词》》》》》》》》》")
get_total(
    "FT=依托考昔 OR FT=安康信 OR FT=卡泊芬净 OR FT=科赛斯 OR FT=氯沙坦 OR FT=络沙坦 OR FT=洛沙坦 OR FT=科素亚 OR FT=阿仑膦酸钠 OR FT=阿伦磷酸钠 OR FT=福善美 OR FT=氯沙坦钾氢氯噻嗪 OR FT=海捷亚 OR FT=厄他培南 OR FT=艾他培南 OR FT=怡万之 OR FT=非那雄胺 OR FT=非那司提 OR FT=非那甾胺 OR FT=保法止 OR FT=非那雄胺 OR FT=非那司提 OR FT=非那甾胺 OR FT=保列治 OR FT=依那普利 OR FT=恩纳普利 OR FT=苯酯丙脯酸 OR FT=悦宁定 OR FT=卡左双多巴 OR FT=息宁 OR FT=孟鲁司特 OR FT=孟鲁斯特 OR FT=顺尔宁 OR FT=顺耳宁 OR FT=亚胺培南 OR FT=亚安培南 OR FT=泰能 OR FT=辛伐他汀 OR FT=新伐他汀 OR FT=舒降之 OR FT=舒降脂 OR FT=拉替拉韦 OR FT=艾生特 OR FT=23价肺炎球菌多糖疫苗 OR FT=纽莫法 OR FT=甲型肝炎灭活疫苗(人二倍体细胞) OR FT=人二倍体甲型肝炎灭活疫苗 OR FT=维康特 OR FT=西格列汀 OR FT=西他列汀 OR FT=捷诺维 OR FT=西格列汀二甲双胍 OR FT=西格列汀二甲双胍 OR FT=捷诺达 OR FT=依折麦布 OR FT=依替米贝 OR FT=益适纯 OR FT=阿仑膦酸钠维D3 OR FT=福美加 OR FT=福美佳 OR FT=阿瑞匹坦 OR FT=阿瑞吡坦 OR FT=意美 OR FT=地氯雷他定 OR FT=恩理思")
log.info("》》》》》》》》》休息2秒，继续查询第二组关键词》》》》》》》》》")
time.sleep(2)
get_total(
    "FT=糠酸莫米松 OR FT=内舒拿 OR FT=复方倍他米松 OR FT=得宝松 OR FT=重组促卵泡素β OR FT=普利康 OR FT=依折麦布辛伐他汀 OR FT=依替米贝辛伐他汀 OR FT=葆至能 OR FT=重组人干扰素α-2b OR FT=甘乐能 OR FT=聚乙二醇干扰素α-2b OR FT=佩乐能 OR FT=替莫唑胺 OR FT=泰道 OR FT=去氧孕烯炔雌醇 OR FT=妈富隆 OR FT=去氧孕烯炔雌醇 OR FT=美欣乐 OR FT=替勃龙 OR FT=替勃隆 OR FT=利维爱 OR FT=十一酸睾酮 OR FT=安特尔 OR FT=罗库溴铵 OR FT=爱可松 OR FT=肌松监测仪 OR FT=米氮平 OR FT=瑞美隆 OR FT=依托孕烯 OR FT=依伴侬 OR FT=泊沙康唑 OR FT=诺科飞 OR FT=加尼瑞克 OR FT=殴加利 OR FT=达托霉素 OR FT=克必信 OR FT=舒更葡糖钠 OR FT=布瑞亭 OR FT=四价人乳头瘤病毒疫苗 OR FT=佳达修 OR FT=五价重配轮状病毒减毒活疫苗 OR FT=乐儿德 OR FT=九价人乳头瘤病毒疫苗 OR FT=佳达修 OR FT=依巴司韦格佐普韦 OR FT=格佐普韦 OR FT=依巴司韦 OR FT=择必达 OR FT=依托孕烯炔雌醇阴道环 OR FT=舞悠 OR FT=帕博利珠单抗 OR FT=可瑞达")
# download("基于江南原生态理念的水居民宿设计——以原舍·阅水民宿设计为例.pdf",
#          "http://kns.cnki.net/kns/download.aspx?filename=s9Ge4EVaSNXewMFT3p2Z2RjdSBnW5Q2L5cVS4p2UIZTb6Flcp92dnJGepBTSGZUZthWQWpXYkFVY5x2QzoWWjZ2ZEF3QSNlduRjS6NlZXdkMmhDWFB1Y4kma0MmUGhGd4MUMnFXNnB1an9maxMGMVN3ZIljbqdUT&tablename=CJFDPREP")
# download("辛伐他汀片体外溶出一致性评价方法的建立_郭志渊_谢华_袁军.pdf",
#          "http://kns.cnki.net/kns/download.aspx?filename=OhkdJJUYJRlbPdWWEJHb4ATNT1WR2RnUyhmMvVnSUFkMx1mNWV1TpJGRwIkaSp1YaJWbnZkQFFWevJnar8iN6xmW3cTcQN3Mj9SS5YEOrgTNjF3T3dTc5oUVq1WaFpkSy8mci9GNlJTavxkWRhmQxlFVOFUTLJUN&tablename=CAPJDAY")

# removeHandler 要放在程序运用打印日志的后面
log.removeHandler(log_file_handler)
