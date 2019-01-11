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

# ��½��Ϣ
data = {
    'userName': 'sherry.huang@goal-noah.com',
    'pwd': '33530912'
}

# �����ļ��洢Ŀ¼
file_dir = r"D:\�ĵ�\�й�֪��"

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

# ��ȡcookie
BASIC_URL = 'http://kns.cnki.net/kns/brief/result.aspx'
# ����post��������ע��һ��
SEARCH_HANDLE_URL = 'http://kns.cnki.net/kns/request/SearchHandler.ashx'
# ����get������������Դ
GET_PAGE_URL =
# ���صĻ�������
DOWNLOAD_URL = 'http://kns.cnki.net/kns/'
# �л�ҳ���������
CHANGE_PAGE_URL = 'http://kns.cnki.net/kns/brief/brief.aspx'

# �����ȫ��session
session = requests.Session()
# ���ֻỰ
session.get('http://kns.cnki.net/kns/brief/result.aspx', headers=HEADER)
cookie_path = os.path.join(os.getcwd(), 'article-cnki-cookie.txt')


def login():
    # �ಽ��½��ȡ����cookie
    session.cookies.clear()
    session.cookies.save()
    session.get(
        'http://kns.cnki.net/kns/brief/result.aspx?dbprefix=SCDB&crossDbcodes=CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',
        headers=HEADER)
    # cookie����SID_klogin
    session.get('http://kns.cnki.net/KLogin/Request/GetKFooter.ashx', headers=HEADER)
    r = session.get('http://login.cnki.net/TopLogin/api/loginapi/Login?isAutoLogin=true&'
                    + urllib.parse.urlencode(data) + '&_=' + str(int(time.time() * 1000)))
    user_info = json.loads(r.text[1: -1])
    if user_info.get('IsSuccess'):
        print('��½�ɹ� ... ' + json.dumps(user_info))
    else:
        print('��½ʧ�� ... ' + json.dumps(user_info))


def get_total(key):
    static_post_data = {
        'action': '',
        'NaviCode': '*',
        'ua': '1.21',
        'isinEn': '1',
        'PageName': 'ASP.brief_default_result_aspx',
        'DbPrefix': 'SCDB',
        'DbCatalog': '�й�ѧ���ڿ���������ܿ�',
        'ConfigFile': 'CJFQ.xml',
        'db_opt': 'CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',  # �������CNKI�Ҳ�ģ�
        'db_value': '�й�ѧ���ڿ���������ܿ�',
        'year_type': 'echar',
        'his': '0',
        'db_cjfqview': '�й�ѧ���ڿ���������ܿ�,WWJD',
        'db_cflqview': '�й�ѧ���ڿ���������ܿ�',
        '__': time.asctime(time.localtime()) + ' GMT+0800 (�й���׼ʱ��)',
        'expertvalue': key,
        'publishdate_from': '2018-12-24'
    }

    # ���̶��ֶ����Զ����ֶ����
    post_data = static_post_data
    # �����е�һ�����󣬷������ʾ������û���û�
    first_post_res = session.post(
        SEARCH_HANDLE_URL, data=post_data, headers=HEADER)
    # get��������Ҫ�����һ������������ֵ
    get_result_url = 'http://kns.cnki.net/kns/brief/brief.aspx?pagename=' + first_post_res.text + '&t=1544249384932&keyValue=&S=1&sorttype='
    # ��������ĵ�һ��ҳ��
    second_get_res = session.get(get_result_url, headers=HEADER)
    change_page_pattern_compile = re.compile(r'.*?pagerTitleCell.*?<a href="(.*?)".*')
    change_page_url = re.search(change_page_pattern_compile, second_get_res.text).group(1)
    parse_page(
        self.pre_parse_page(second_get_res.text), second_get_res.text)







    # ���ò�ѯ����������һ��
    total_url = 'http://kns.cnki.net/kns/request/SearchHandler.ashx'
    r_param = session.post(total_url, data=s_handle_data, headers=headers)
    param_dict = dict(parse.parse_qsl("pagename=" + r_param.text))
    print(param_dict)

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
    print("�ҵ� {} ����������� {} ҳ".format(result_count, page_count))

    # ��ʼ��ҳ����
    for page_num in range(2):
        get_list(key, page_num + 1, param_dict)
        time.sleep(2)
    print(">>>>>>>>>>����ִ����� .................")


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
        tr_author = ""
        authors_a = tds[2].select('a')
        for author_a in authors_a:
            tr_author = tr_author + "_" + author_a.text

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
            print("�ļ�����δ֪��ԭ������{}".format(type))

        # �������б�
        print(tr_order, tr_title, tr_author, tr_file_type, tr_time.strip(), tr_db.strip())
        # �ļ��ظ�ȥ��
        file_will_write = os.path.join(file_dir, tr_title + tr_author + tr_file_type)
        if os.path.exists(file_will_write):
            print('\t�ļ��Ѵ��� ... {}'.format(file_will_write))
            continue
        else:
            print('\t�ļ������ڣ���ʼ���� ... {}'.format(file_will_write))
            print('\t�������� ... {}'.format('http://kns.cnki.net/kns' + tr_down_url[2:]))
            download(file_will_write, 'http://kns.cnki.net/kns' + tr_down_url[2:])
            time.sleep(2)
            print('\t�ļ������ĳ�')


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

    # ��һ����֤�Ƿ���֧�������δ֧�����ò����򷵻ص���ҳ�棬û��location
    if loc_pubdownload:
        # print(session.cookies)
        r_pubdownload = session.get(loc_pubdownload, headers=down_headers, allow_redirects=False)
        r_pubdownload.encoding = 'utf-8'
        # print(r_pubdownload.status_code)
        # print(r_pubdownload.text)
        print(r_pubdownload.headers)
        print(r_pubdownload.text)

        if r_pubdownload.status_code == 200:
            # ���ص���ҳ��
            print('����δ֧����֧���� ...')
            time.sleep(2)
            pay_data = {
                'pid': 'cjfq',
                'uid': requests.utils.dict_from_cookiejar(session.cookies).get('LID')
            }
            r_pay = session.post(loc_pubdownload, data=pay_data, headers=down_headers, allow_redirects=False)
            r_pay.encoding = 'utf-8'
            if r_pay.headers.get('Location', None):
                print('����֧����� ...{}'.format(r_pay.headers))
                # ���ص����ļ���
                down_headers['Host'] = get_host(r_pay.headers['Location'])['host']
                r_do = session.get(r_pay.headers['Location'], headers=down_headers, allow_redirects=False)
                down_headers['Host'] = get_host(r_do.headers['Location'])['host']
                r_new = session.get(r_do.headers['Location'], headers=down_headers, allow_redirects=False)

                save_file(file_name, r_new)
            else:
                print('����֧����Ч ...{}'.format(r_pay.headers))
                print('�������� ...{}'.format('http://kns.cnki.net/kns' + down_url[2:]))
                # print(r_pay.text)
                exit(1)
        else:
            # ���ص����ļ���
            print('���²���Ҫ֧����ֱ������ ...')
            down_headers['Host'] = get_host(r_pubdownload.headers['Location'])['host']
            r_do = session.get(r_pubdownload.headers['Location'], headers=down_headers, allow_redirects=False)
            down_headers['Host'] = get_host(r_do.headers['Location'])['host']
            r_new = session.get(r_do.headers['Location'], headers=down_headers, allow_redirects=False)

            save_file(file_name, r_new)
    else:
        print('��������������Ч��{}'.format(loc_pubdownload))


# ��ȡ����url����
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
        print('\t�ļ��Ѵ��� ... {}'.format(file2write))
    else:
        # ��������
        with open(file2write, "wb") as code:
            code.write(response.content)
        print('\t�ļ�������� ... {}'.format(file2write))


login()
get_total("FT=���п��� OR FT=������ OR FT=�����Ҿ� OR FT=����˹ OR FT=��ɳ̹ OR FT=��ɳ̹ OR FT=��ɳ̹ OR FT=������ OR FT=��������� OR FT=���������� OR FT=������ OR FT=��ɳ̹��������� OR FT=������ OR FT=�������� OR FT=�������� OR FT=����֮ OR FT=�����۰� OR FT=����˾�� OR FT=�����ް� OR FT=����ֹ OR FT=�����۰� OR FT=����˾�� OR FT=�����ް� OR FT=������ OR FT=�������� OR FT=�������� OR FT=���������� OR FT=������ OR FT=����˫��� OR FT=Ϣ�� OR FT=��³˾�� OR FT=��³˹�� OR FT=˳���� OR FT=˳���� OR FT=�ǰ����� OR FT=�ǰ����� OR FT=̩�� OR FT=������͡ OR FT=�·���͡ OR FT=�潵֮ OR FT=�潵֬ OR FT=������Τ OR FT=������ OR FT=23�۷�������������� OR FT=ŦĪ�� OR FT=���͸����������(�˶�����ϸ��) OR FT=�˶�������͸���������� OR FT=ά���� OR FT=������͡ OR FT=������͡ OR FT=��ŵά OR FT=������͡����˫�� OR FT=������͡����˫�� OR FT=��ŵ�� OR FT=������ OR FT=�����ױ� OR FT=���ʴ� OR FT=���������άD3 OR FT=������ OR FT=������ OR FT=����ƥ̹ OR FT=������̹ OR FT=���� OR FT=���������� OR FT=����˼")
# download("���ڽ���ԭ��̬�����ˮ��������ơ�����ԭ�ᡤ��ˮ�������Ϊ��.pdf",
#          "http://kns.cnki.net/kns/download.aspx?filename=s9Ge4EVaSNXewMFT3p2Z2RjdSBnW5Q2L5cVS4p2UIZTb6Flcp92dnJGepBTSGZUZthWQWpXYkFVY5x2QzoWWjZ2ZEF3QSNlduRjS6NlZXdkMmhDWFB1Y4kma0MmUGhGd4MUMnFXNnB1an9maxMGMVN3ZIljbqdUT&tablename=CJFDPREP")
# download("������͡Ƭ�����ܳ�һ�������۷����Ľ���_��־Ԩ_л��_Ԭ��.caj",
#          "http://nvsm.cnki.net/kns/download.aspx?filename=4RFd1sGcB9Ub3gWbCJjYHNTYM92TaRkZvd3U6pVZVF0bLZVZaNEUU9SVnlWVLFERvQnRhdlWYNkQS5mQJpEb3siUM1EeE9kVhJVcnRGZ5l0dwwkMwUVV210NtRHa6FnTNdFdIl0MG1mWJVVTZRGULRUQrdlbDZHR&tablename=CAPJDAY")
