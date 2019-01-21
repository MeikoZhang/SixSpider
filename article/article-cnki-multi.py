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
base_path = r"E:\�ĵ�"

log_fmt = '%(asctime)s\tFile \"%(filename)s\",line %(lineno)s\t%(levelname)s: %(message)s'
formatter = logging.Formatter(log_fmt)

# ����̨log����
# Ĭ����sys.stderr
log_console_handler = logging.StreamHandler(sys.stdout)
log_console_handler.setLevel(logging.INFO)
log_console_handler.setFormatter(formatter)

# �ļ�log����
log_file_handler = TimedRotatingFileHandler(filename=os.path.join(base_path, r"article\cnki_run.log"), when="D", interval=1, backupCount=7, encoding='utf-8')
log_file_handler.setLevel(logging.INFO)
log_file_handler.setFormatter(formatter)
log_file_handler.suffix = "%Y-%m-%d_%H-%M.log"
log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log$")

# log��ʼ��
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

# ��½��Ϣ
data = {
    'userName': 'sherry.huang@goal-noah.com',
    'pwd': '33530912'
}

# �����ļ��洢Ŀ¼
# file_dir = os.path.join(base_path, "�й�֪��")
cur_day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
if cur_day > '2019-02-01':
    exit()

file_dir = os.path.join(base_path, "�й�֪��", cur_day)
if os.path.exists(file_dir):
    print("Ŀ¼{}�Ѵ��ڣ������ļ���...".format(file_dir))
else:
    print("Ŀ¼{}�����ڣ�������Ŀ¼...".format(file_dir))
    os.mkdir(file_dir)

file_dir_files = os.listdir(file_dir)
# �������ļ��б�
file_m = os.path.join(base_path, "�й�֪��Ŀ¼.txt")
files_m = []

# ����Ŀ¼�б� - ���� ����
other_list = []

# �����ȫ��session
session = requests.Session()

cookie_path = os.path.join(base_path, r"article\article-cnki-cookie.txt")

session.cookies = HC.MozillaCookieJar(filename=cookie_path)

session.get('http://www.cnki.net/', headers=headers)
session.get('http://kns.cnki.net/kns/brief/result.aspx?dbprefix=SCDB&crossDbcodes=CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',
            headers=headers)
session.get('http://kns.cnki.net/kns/brief/result.aspx', headers=headers)


def load_list():
    # �����Լ�Ŀ¼
    files_m.clear()
    for f_file in open(file_m, "r", encoding='utf-8'):
        if len(f_file.split(",")) < 2:
            continue
        # print(f_file.strip())
        files_m.append(f_file.split(",")[1])
        # print(">>")

    # ��������Ŀ¼
    other_list.clear()
    files = os.listdir(base_path)
    for file in files:
        if file.find("Ŀ¼") > 0 and file != "�й�֪��Ŀ¼.txt":
            for f_file in open(os.path.join(base_path, file), "r", encoding='utf-8'):
                if len(f_file.split(",")) < 2:
                    continue
                other_list.append(f_file.split(",")[0])


def login():
    # �ಽ��½��ȡ����cookie
    session.get(
        'http://kns.cnki.net/kns/brief/result.aspx?dbprefix=SCDB&crossDbcodes=CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',
        headers=headers)
    # cookie����SID_klogin
    session.get('http://kns.cnki.net/KLogin/Request/GetKFooter.ashx', headers=headers)
    if int(time.time()) > 1548950400:
        exit(0)
    r = session.get('http://login.cnki.net/TopLogin/api/loginapi/Login?isAutoLogin=false&'
                    + urllib.parse.urlencode(data) + '&_=' + str(int(time.time() * 1000)))
    user_info = json.loads(r.text[1: -1])
    if user_info.get('IsSuccess'):
        log.info('��½�ɹ� ... ' + json.dumps(user_info))
        login_header = {
            'Host': 'login.cnki.net',
            'Pragma': 'no-cache',
            'Referer': 'http://kns.cnki.net/kns/brief/result.aspx?dbprefix=SCDB&crossDbcodes=CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD'
        }
        session.post('http://kns.cnki.net/kns/Loginid.aspx', data={'uid': user_info.get('Uid')},
                     headers={**headers, **login_header})
        session.cookies.save()
    else:
        log.error('��½ʧ�� ... ' + json.dumps(user_info))
        exit('��½ʧ�� ... ')

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
        log.error('δ�ҵ�cookies�ļ�')
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
        , 'DbCatalog': '�й�ѧ��������������ܿ�'
        , 'ConfigFile': 'SCDB.xml'
        , 'db_opt': 'CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD'
        , 'expertvalue': key
        , 'publishdate_from': '2018-12-24'
        , 'his': '0'
        , '__': 'Thu Jan 10 2019 15:05:25 GMT+0800 (�й���׼ʱ��)'
    }
    # ���ò�ѯ����������һ��
    total_url = 'http://kns.cnki.net/kns/request/SearchHandler.ashx'
    r_param = session.post(total_url, data=s_handle_data, headers=headers)
    param_dict = dict(parse.parse_qsl("pagename=" + r_param.text))

    # ��ȡ��ѯ�б�
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
    log.info("�ҵ� {} ����������� {} ҳ".format(result_count, page_count))

    # ��ʼ��ҳ����
    for page_num in range(page_count):
        get_list(key, page_num + 1, param_dict)
        time.sleep(2)
    log.info(">>>>>>>>>>����ִ����� .................")


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
    # ��ȡ��ѯ�б�
    list_url = 'http://kns.cnki.net/kns/brief/brief.aspx?' + urllib.parse.urlencode(page_data)
    r_list_doc = session.get(list_url, headers=headers)
    r_list_doc.encoding = 'utf-8'
    # print(r_list_doc.text)

    soup = BeautifulSoup(r_list_doc.text, 'lxml', from_encoding='utf-8')
    headers['Referer'] = list_url
    trs = soup.select('.GridTableContent tr')
    # ȥ��������
    for tr in trs[1:]:
        tds = tr.select('td')
        # ���
        tr_order = tds[0].text

        # ������
        tr_title = tds[1].select('a')[0].text

        # ����
        tr_authors = ""
        authors_a = tds[2].select('a')
        for author_a in authors_a:
            tr_authors = tr_authors + "_" + author_a.text
        # ����
        tr_author = ""
        if len(authors_a) > 0:
            tr_author = authors_a[0].text

        # ����ʱ��
        tr_time = tds[4].text

        # ���ݿ�
        tr_db = tds[5].text

        # �������� http://kns.cnki.net/kns/download.aspx
        tr_down_url = tds[7].select('a')[0].attrs['href']

        # �ļ�����
        type = tds[8].select('a')[0].attrs['title']
        if type == "HTML�Ķ�":
            tr_file_type = ".pdf"
        elif type == "�Ķ�":
            tr_file_type = ".caj"
        else:
            tr_file_type = ""
            log.info("�ļ�����δ֪��ԭ������{}".format(type))

        # �������б�
        log.info("{},{},{},{},{},{}".format(tr_order, tr_title, tr_author, tr_file_type, tr_time.strip(), tr_db.strip()))
        # �ļ��ظ�ȥ��
        file_will_write = os.path.join(file_dir, tr_title)

        if_down = True
        # ��ͬ��վ�ļ��ظ�ȥ��-������������
        if tr_title+"_"+tr_author in files_m:
            log.info('\t�ļ��Ѵ��ڵ�ǰ��վĿ¼�б� ... {}'.format(os.path.join(file_dir, tr_title)))
            if_down = False

        # ��ͬ��վ�ظ�ȥ��-���ݱ���
        if tr_title in other_list:
            log.info('\t�ļ��Ѵ���������վĿ¼�б� ... {}'.format(os.path.join(file_dir, tr_title)))
            if_down = False

        # for f in file_dir_files:
        #     if f.startswith(tr_title):
        #         print('\t{},{}'.format(f, tr_title))
        #         print('\t�ļ��Ѵ��� ... {}'.format(os.path.join(file_dir, f)))
        #         if_down = False
        #         with open(file_m, "a") as fm:
        #             fm.write(tr_title + "," + os.path.join(file_dir, f) + "\n")
        #         continue
        if if_down:
            log.info('\t�ļ������ڣ���ʼ���� ... {}'.format(file_will_write))
            download_url = 'http://kns.cnki.net/kns' + tr_down_url[2:] + '&dflag=pdfdown'
            log.info('\t�������� ... {}'.format(download_url))
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

    # ��һ����֤�Ƿ���֧�������δ֧�����ò����򷵻ص���ҳ�棬û��location
    if loc_pubdownload:
        # print(session.cookies)
        down_headers['Host'] = get_host(loc_pubdownload)['host']
        r_pubdownload = session.get(loc_pubdownload, headers=down_headers, allow_redirects=False)
        r_pubdownload.encoding = 'utf-8'
        # print(r_pubdownload.status_code)
        # print(r_pubdownload.text)

        if r_pubdownload.status_code == 200:
            # ���ص���ҳ��
            log.info('\t����δ֧����֧���� ...')
            time.sleep(2)
            pay_data = {
                'pid': 'cjfq',
                'uid': requests.utils.dict_from_cookiejar(session.cookies).get('LID')
            }

            r_pay = session.post(loc_pubdownload, data=pay_data, headers=down_headers, allow_redirects=False)
            r_pay.encoding = 'utf-8'
            if r_pay.status_code == 302:
                log.info('\t����֧����� ...{}'.format(r_pay.headers))
                # ���ص����ļ���
                # ѭ��ֱ��r = 200, �ض��������������ӣ�
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

                # �����ļ�
                save_file(title, author, r)
            else:
                log.error('\t����֧����Ч ...{}'.format(r_pay.headers))
                log.error('\t�������� ...{}'.format('http://kns.cnki.net/kns' + down_url[2:]))

        else:
            # ���ص����ļ���
            log.info('\t���²���Ҫ֧����ֱ������ ...')
            # ѭ��ֱ��r = 200, �ض���������������
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

            # �����ļ�
            save_file(title, author, r)
    else:
        log.error('\t��������������Ч��{}'.format(loc_pubdownload))


# ��ȡ����url����
def get_host(url):
    pattern = re.compile(r'(.*?)://(.*?)/', re.S)
    response = re.search(pattern, url)
    if response:
        return {'header': str(response.group(1)).strip(), 'host': str(response.group(2)).strip()}
    else:
        return None


def save_file(title, author, response):
    if response.headers.get('Content-Disposition'):
        # ������, ��ȡheader�����ļ���
        file_name_str = str(bytes(response.headers['Content-Disposition'], encoding="iso-8859-1"), encoding="GBK")
        file_name = file_name_str.split('filename=')[1]
        # print(file_name)

        file2write = os.path.join(file_dir, file_name)
        if os.path.exists(file2write):
            log.info('\t�ļ��Ѵ��� ... {}'.format(file2write))
            with open(file_m, "a", encoding='utf-8') as fm:
                fm.write("{},{},{}\n".format(title, title+"_"+author, file2write))
        else:
            # ��������
            with open(file2write, "wb") as code:
                code.write(response.content)
                log.info('\t�ļ�������� ... {}'.format(file2write))
            with open(file_m, "a", encoding='utf-8') as fm:
                fm.write("{},{},{}\n".format(title, title+"_"+author, file2write))

    else:
        log.error('\t�ļ��޷����� ... {}'.format(response.headers))
        log.error(response.text)


def print_cookie():
    for cookie in session.cookies:
        log.info(cookie.name, cookie.value)


login()
log.info("��������������������ѯ��һ��ؼ��ʡ�����������������")
get_total(
    "FT=���п��� OR FT=������ OR FT=�����Ҿ� OR FT=����˹ OR FT=��ɳ̹ OR FT=��ɳ̹ OR FT=��ɳ̹ OR FT=������ OR FT=��������� OR FT=���������� OR FT=������ OR FT=��ɳ̹��������� OR FT=������ OR FT=�������� OR FT=�������� OR FT=����֮ OR FT=�����۰� OR FT=����˾�� OR FT=�����ް� OR FT=����ֹ OR FT=�����۰� OR FT=����˾�� OR FT=�����ް� OR FT=������ OR FT=�������� OR FT=�������� OR FT=���������� OR FT=������ OR FT=����˫��� OR FT=Ϣ�� OR FT=��³˾�� OR FT=��³˹�� OR FT=˳���� OR FT=˳���� OR FT=�ǰ����� OR FT=�ǰ����� OR FT=̩�� OR FT=������͡ OR FT=�·���͡ OR FT=�潵֮ OR FT=�潵֬ OR FT=������Τ OR FT=������ OR FT=23�۷�������������� OR FT=ŦĪ�� OR FT=���͸����������(�˶�����ϸ��) OR FT=�˶�������͸���������� OR FT=ά���� OR FT=������͡ OR FT=������͡ OR FT=��ŵά OR FT=������͡����˫�� OR FT=������͡����˫�� OR FT=��ŵ�� OR FT=������ OR FT=�����ױ� OR FT=���ʴ� OR FT=���������άD3 OR FT=������ OR FT=������ OR FT=����ƥ̹ OR FT=������̹ OR FT=���� OR FT=���������� OR FT=����˼")
log.info("��������������������Ϣ2�룬������ѯ�ڶ���ؼ��ʡ�����������������")
time.sleep(2)
get_total(
    "FT=����Ī���� OR FT=������ OR FT=������������ OR FT=�ñ��� OR FT=����������ئ� OR FT=������ OR FT=������������͡ OR FT=�����ױ�������͡ OR FT=������ OR FT=�����˸����ئ�-2b OR FT=������ OR FT=���Ҷ��������ئ�-2b OR FT=������ OR FT=��Ī�� OR FT=̩�� OR FT=ȥ����ϩȲ�ƴ� OR FT=�踻¡ OR FT=ȥ����ϩȲ�ƴ� OR FT=������ OR FT=�沪�� OR FT=�沪¡ OR FT=��ά�� OR FT=ʮһ��غͪ OR FT=���ض� OR FT=�޿���� OR FT=������ OR FT=���ɼ���� OR FT=�׵�ƽ OR FT=����¡ OR FT=������ϩ OR FT=����ٯ OR FT=��ɳ���� OR FT=ŵ�Ʒ� OR FT=������� OR FT=Ź���� OR FT=����ù�� OR FT=�˱��� OR FT=��������� OR FT=����ͤ OR FT=�ļ�����ͷ���������� OR FT=�Ѵ��� OR FT=���������״�������������� OR FT=�ֶ��� OR FT=�ż�����ͷ���������� OR FT=�Ѵ��� OR FT=����˾Τ������Τ OR FT=������Τ OR FT=����˾Τ OR FT=��ش� OR FT=������ϩȲ�ƴ������� OR FT=���� OR FT=�������鵥�� OR FT=�����")
# download("���ڽ���ԭ��̬�����ˮ��������ơ�����ԭ�ᡤ��ˮ�������Ϊ��.pdf",
#          "http://kns.cnki.net/kns/download.aspx?filename=s9Ge4EVaSNXewMFT3p2Z2RjdSBnW5Q2L5cVS4p2UIZTb6Flcp92dnJGepBTSGZUZthWQWpXYkFVY5x2QzoWWjZ2ZEF3QSNlduRjS6NlZXdkMmhDWFB1Y4kma0MmUGhGd4MUMnFXNnB1an9maxMGMVN3ZIljbqdUT&tablename=CJFDPREP")
# download("������͡Ƭ�����ܳ�һ�������۷����Ľ���_��־Ԩ_л��_Ԭ��.pdf",
#          "http://kns.cnki.net/kns/download.aspx?filename=OhkdJJUYJRlbPdWWEJHb4ATNT1WR2RnUyhmMvVnSUFkMx1mNWV1TpJGRwIkaSp1YaJWbnZkQFFWevJnar8iN6xmW3cTcQN3Mj9SS5YEOrgTNjF3T3dTc5oUVq1WaFpkSy8mci9GNlJTavxkWRhmQxlFVOFUTLJUN&tablename=CAPJDAY")

# removeHandler Ҫ���ڳ������ô�ӡ��־�ĺ���
log.removeHandler(log_file_handler)
