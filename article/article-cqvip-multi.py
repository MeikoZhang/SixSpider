# coding=gbk

import requests
from bs4 import BeautifulSoup
import time
import os
import sys
import re
import http.cookiejar as HC
import random
import traceback
import hashlib
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
log_file_handler = TimedRotatingFileHandler(filename=os.path.join(base_path, r"article\cqvip_run.log"), when="D", interval=1, backupCount=7)
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
    'Accept': 'text/html, */*; q=0.01'
    , 'Accept-Encoding': 'gzip, deflate'
    , 'Accept-Language': 'zh-CN,zh;q=0.9'
    , 'Connection': 'keep-alive'
    , 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    ,
    'Cookie': 'ASP.NET_SessionId=ns5dkfsbstg53y2tltklz1uf;LIBUSERCOOKIE=Oosn4ui+3LIAcpa/+sCLSLumqrc/XpZlqdxCkoqLXe888frrRhvRzCOVrla0ToPKV6Luj9NWHzwzKC24fAeMx7orTNZjIy9oG5qEoA8nJ4PkLiFK9YMoaeMPT//0+cTP5j3Qyzup711HZRD2teAHC/GYoETE1+D7xlFQ6TytIcsHTyOcxdjlMPZHEJ/nr8eZBxiYxUmkIJvCaCtUKeqiKrzERq/MVLncFbNsmiFRV1LsCaK1a1KMoiSryztwcIm+AyQfGjJ4mccXlSmCk+xuunS/ymN0rANZXV8QEWHWVIhEhSJwhULonh/8ujtw7dCRUchYjtu/N9Q0ks49AX7X6MwH+uvZnyjjx6Qoup6VkLMYn24qH6HN2g==;LIBUSERIDCOOKIE=19028277;LIBUSERNAMECOOKIE=447229719@qq.com;search_isEnable=1;skybug=ea4aa775b9af539f55ca5843428f034b;user_behavior_flag=2bb3cccf-1c24-4c40-805d-9f5082b35071;'
    , 'Host': 'qikan.cqvip.com'
    , 'Origin': 'http://qikan.cqvip.com'
    , 'Referer': 'http://qikan.cqvip.com/Qikan/Search/Advance?from=index'
    ,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    , 'X-Requested-With': 'XMLHttpRequest'
}


# ��½��Ϣ
data = {
    'Username': '447229719@qq.com',
    'Password': '33530912'
}

# md5ת������
m2 = hashlib.md5()
m2.update(data['Password'].encode('utf-8'))
data['Password'] = m2.hexdigest()

# �����ļ��洢Ŀ¼
# file_dir = os.path.join(base_path, "ά����")
cur_day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
if cur_day > '2019-03-01':
    log.info("��Ȩ�ѹ���")
    exit()

file_dir = os.path.join(base_path, "ά����", cur_day)
if os.path.exists(file_dir):
    print("Ŀ¼{}�Ѵ��ڣ������ļ���...".format(file_dir))
else:
    print("Ŀ¼{}�����ڣ�������Ŀ¼...".format(file_dir))
    os.mkdir(file_dir)

# �������ļ��б�-Ŀ¼��ʽ������/����_������/�ļ�Ŀ¼
file_m = os.path.join(base_path, "ά����Ŀ¼.txt")
# ����վĿ¼�б� - ����_������ ����
files_m = []


# ����Ŀ¼�б� - ���� ����
other_list = []


# �����ȫ��session
session = requests.Session()
cookie_path = os.path.join(base_path, r"article\article-cqvip-cookie.txt")
# print(cookie_path)


def load_list():
    # �����Լ�Ŀ¼
    files_m.clear()
    for f_file in open(file_m, "r", encoding='utf-8'):
        if len(f_file.split("|*|")) < 2:
            continue
        files_m.append(f_file.split("|*|")[1])

    # ��������Ŀ¼
    other_list.clear()
    files = os.listdir(base_path)
    for file in files:
        if file.find("Ŀ¼") > 0 and file != "ά����Ŀ¼.txt":
            for f_file in open(os.path.join(base_path, file), "r", encoding='utf-8'):
                if len(f_file.split("|*|")) < 2:
                    continue
                other_list.append(f_file.split("|*|")[0])


def login():
    session.cookies = HC.MozillaCookieJar(filename=cookie_path)
    # session.cookies.save()
    #  �������cookies�ļ�������أ��������������ʾ
    try:
        session.cookies.load(ignore_discard=True, ignore_expires=True)

        session.get('http://qikan.cqvip.com/', headers=headers)
        session.cookies.save(ignore_discard=True, ignore_expires=True)

        session.get('http://qikan.cqvip.com/Qikan/WebControl/IsViewObject', headers=headers)
        session.cookies.save(ignore_discard=True, ignore_expires=True)

        cookie_str = ""
        for cookie in session.cookies:
            # print(cookie.name, cookie.value)
            cookie_str = cookie_str + cookie.name + "=" + cookie.value + ";"
        # log.info(cookie_str)
        headers['Cookie'] = cookie_str

        r1 = session.get('http://qikan.cqvip.com/RegistLogin/CheckUserIslogin?'+str(random.random())
                         , headers=headers)
        # print(r1.json())
        # ��½��֤
        is_login = r1.json().get('isLogined')
        if is_login:
            log.info('�ѵ�¼ ...cookie��Ч')
            return
        else:
            log.info('δ��¼ ...���Ե�½...')
    except Exception as e:
        log.info('δ�ҵ�cookies�ļ�')
        log.info(traceback.format_exc())

    # ��½�ӿ�
    login_data = {
        'LoginUserName': data['Username'],
        'LoginUserPassword': data['Password'],
        'LoginType': 'normallogin'
    }
    login_r = session.post('http://qikan.cqvip.com/RegistLogin/Login', data=login_data, headers=headers)
    # print(login_r.json())
    # for cookie_l in login_r.cookies:
    #     print(cookie_l.name, cookie_l.value)
    session.cookies.save(ignore_discard=True, ignore_expires=True)
    log.info('��½�ɹ� ...����cookie')


def get_total(key=None):
    if not key:
        log.info('û�����ùؼ��ʣ�����')
        return

    load_list()
    # ��ȡ�����б�
    url = 'http://qikan.cqvip.com/Search/SearchList'
    list_data = {
        'searchParamModel': '{"ObjectType":1,"SearchKeyList":[],"SearchExpression":"'+key+'","BeginYear":"2019","EndYear":"2019","JournalRange":"","DomainRange":"","PageSize":"0","PageNum":"1","Sort":"0","ClusterFilter":"","SType":"","StrIds":"","UpdateTimeType":"","ClusterUseType":"Article","IsNoteHistory":1,"AdvShowTitle":"'+key+'","ObjectId":"","ObjectSearchType":"0","ChineseEnglishExtend":"0","SynonymExtend":"0","ShowTotalCount":"0","AdvTabGuid":"9a2c2edb-4c06-8fa0-631c-a1745ab6e81c"}'
    }
    r = session.post(url, data=list_data, headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'lxml', from_encoding='utf-8')
    # alinks = soup.find_all(attrs={'target': '_blank'})

    result = soup.select('.search-top .search-result span input')
    # print(result)
    total_str = result[0].attrs['value']
    if total_str:
        log.info("==���ҵ�{}ƪ����=========".format(total_str))
        total = int(total_str)
    else:
        log.info("����������û�в��ҵ���������".format(total_str))
        exit(0)
    page_size = 20
    page_total = int((total + page_size - 1)/page_size)
    log.info("==ÿҳ��¼20����{}ҳ=========".format(page_total))
    for page in range(page_total):
        log.info("��ʼ��ȡ��{}ҳ....".format(page + 1))
        get_list(key, str(page + 1))
    log.info("������� ...")


# ��ȡ�����б�
def get_list(key=None, page="1"):
    if not key:
        print('û�����ùؼ��ʣ�����')
        return

    # ��ȡ�����б�������������
    # ��� BeginYear : "2018", EndYear: "2019"
    # ����ʱ�� UpdateTimeType �� 1/1������ 2/�������� 3/������ 4/һ���� 5/������
    url = 'http://qikan.cqvip.com/Search/SearchList'
    list_data = {
        'searchParamModel': '{"ObjectType":1,"SearchKeyList":[],"SearchExpression":"'+key+'","BeginYear":"2019","EndYear":"2019","JournalRange":"","DomainRange":"","PageSize":"0","PageNum":"'+page+'","Sort":"0","ClusterFilter":"","SType":"","StrIds":"","UpdateTimeType":"","ClusterUseType":"Article","IsNoteHistory":1,"AdvShowTitle":"'+key+'","ObjectId":"","ObjectSearchType":"0","ChineseEnglishExtend":"0","SynonymExtend":"0","ShowTotalCount":"0","AdvTabGuid":"9a2c2edb-4c06-8fa0-631c-a1745ab6e81c"}'
    }
    r = session.post(url, data=list_data, headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'lxml', from_encoding='utf-8')
    alinks = soup.select('#remark dl')
    if alinks:
        i = 0
        for alink in alinks:
            i = i+1
            # ��ȡ��������title
            title = alink.select('dt a[target=_blank]')[0].get_text()
            author = alink.select('dd .author a')[0].get_text()
            article_a = alink.select('.article-source a')
            log.info("{},{},{},{}".format(i, title, author, article_a))

            # ȥ�������ؼ��ֵ���Ŀ
            if_down = True
            key_ignore = ["��Ŀ��", "����", "��Ŀ¼"]
            for key_i in key_ignore:
                if key_i in title:
                    log.info('\t��ǰ���±�������ؼ��� {} ���Ѻ�������'.format(key_i))
                    if_down = False
                    break

            if not if_down:
                continue

            # ��ͬ��վ�ļ��ظ�ȥ��-������������
            if title+"_"+author in files_m:
                log.info('\t�ļ��Ѵ��ڵ�ǰ��վĿ¼�б� ... {}'.format(os.path.join(file_dir, title)))
                continue
            # ��ͬ��վ�ظ�ȥ��-���ݱ���
            if title in other_list:
                log.info('\t�ļ��Ѵ���������վĿ¼�б� ... {}'.format(os.path.join(file_dir, title)))
                continue

            # �ļ������ڣ���ʼ����
            log.info('\t�ļ������ڿ�ʼ���� ... {}'.format(os.path.join(file_dir, title)))
            if len(article_a) > 1:
                time.sleep(3)

                article_click = article_a[1].attrs['onclick']
                split = article_click.split('\'')
                # ��ȡ���±�ʶ
                article_id = split[1]
                article_sg = split[3]
                # print(article_id, article_sg)

                # ��ȡ�����Ƿ�֧��
                r2 = session.post('http://qikan.cqvip.com/Qikan/Article/GetArticleRight',
                                  data={
                                      'articleId': article_id
                                  },
                                  headers=headers)
                # print(r2.json())

                if r2.json()['RetValue']:
                    log.info('\t������֧��')
                else:
                    time.sleep(2)
                    log.info('\t����δ֧������ʼ֧������')
                    r_pay = session.post('http://qikan.cqvip.com/Qikan/UserPay/BalancePayment',
                                         data={
                                             'id': article_id
                                         },
                                         headers=headers)
                    log.info(r_pay.text)
                    if r_pay.json().get("PromptMsg") != "֧���ɹ�":
                        log.info('\t����֧��ʧ��!!!!!!!!!!!!!!!!!!!!!!!!')
                        # ֹͣ����
                        break

                # ��ȡ������������
                r3 = session.post('http://qikan.cqvip.com/Qikan/Article/ArticleDown',
                                  data={
                                      'id': article_id,
                                      'info': article_sg,
                                      'ts': int(time.time() * 1000)
                                  },
                                  headers=headers)
                # print(r3.json())

                download_url = r3.json()['url']
                if download_url:
                    log.info('\t������������ {}'.format(download_url))
                    download(title, author, download_url)
            else:
                log.info('\t�ļ��������ӻ�ȡʧ�� ... {}'.format(article_a))


def download(title, author, download_url):
    file_name = download_url.split('FileName=')[1]
    if file_name:
        file2write = os.path.join(file_dir, file_name)
        if os.path.exists(file2write):
            log.info('\t�ļ��Ѵ��� ... {}'.format(file2write))
            # ����Ŀ¼
            with open(file_m, "a", encoding='utf-8') as fm:
                fm.write("{}|*|{}|*|{}\n".format(title, title+"_"+author, file2write))
        else:
            f = session.get(download_url)
            # ������, ��ȡheader�����ļ���
            # file_name_str = str(bytes(f.headers['Content-Disposition'], encoding="iso-8859-1"), encoding="GB2312")
            # fileName = file_name_str.split('filename=')[1]
            # fileName = fileName.replace('"', '').replace("'", "")
            with open(file2write, "wb") as code:
                code.write(f.content)
                # ����Ŀ¼
            log.info('\t�ļ�������� ... {}'.format(file2write))
            with open(file_m, "a", encoding='utf-8') as fm:
                fm.write("{}|*|{}|*|{}\n".format(title, title+"_"+author, file2write))


# get_list('U=���п��� OR U=������')
login()
get_total("U=���п��� OR U=������  OR U=���п��� OR U=������ OR U=�����Ҿ� OR U=����˹ OR U=��ɳ̹ OR U=��ɳ̹ OR U=��ɳ̹ OR U=������ OR U=��������� OR U=���������� OR U=������ OR U=��ɳ̹��������� OR U=������ OR U=�������� OR U=�������� OR U=����֮ OR U=�����۰� OR U=����˾�� OR U=�����ް� OR U=����ֹ OR U=�����۰� OR U=����˾�� OR U=�����ް� OR U=������ OR U=�������� OR U=�������� OR U=���������� OR U=������ OR U=����˫��� OR U=Ϣ�� OR U=��³˾�� OR U=��³˹�� OR U=˳���� OR U=˳���� OR U=�ǰ����� OR U=�ǰ����� OR U=̩�� OR U=������͡ OR U=�·���͡ OR U=�潵֮ OR U=�潵֬ OR U=������Τ OR U=������ OR U=23�۷�������������� OR U=ŦĪ�� OR U=���͸���������� OR U=�˶�������͸���������� OR U=ά���� OR U=������͡ OR U=������͡ OR U=��ŵά OR U=������͡����˫�� OR U=������͡����˫�� OR U=��ŵ��  OR U=������ OR U=�����ױ� OR U=���ʴ� OR U=���������άD3 OR U=������ OR U=������ OR U=����ƥ̹ OR U=������̹ OR U=���� OR U=���������� OR U=����˼ OR U=����Ī���� OR U=������ OR U=������������ OR U=�ñ��� OR U=����������ئ� OR U=������ OR U=������������͡ OR U=�����ױ�������͡ OR U=������ OR U=�����˸����ئ�-2b OR U=������ OR U=���Ҷ��������ئ�-2b OR U=������ OR U=��Ī�� OR U=̩�� OR U=ȥ����ϩȲ�ƴ� OR U=�踻¡ OR U=ȥ����ϩȲ�ƴ� OR U=������ OR U=�沪�� OR U=�沪¡ OR U=��ά�� OR U=ʮһ��غͪ OR U=���ض� OR U=�޿���� OR U=������ OR U=���ɼ���� OR U=�׵�ƽ OR U=����¡ OR U=������ϩ OR U=����ٯ OR U=��ɳ���� OR U=ŵ�Ʒ� OR U=������� OR U=Ź���� OR U=����ù�� OR U=�˱��� OR U=��������� OR U=����ͤ OR U=�ļ�����ͷ���������� OR U=�Ѵ��� OR U=���������״�������������� OR U=�ֶ��� OR U=�ż�����ͷ���������� OR U=�Ѵ��� OR U=����˾Τ������Τ OR U=������Τ/����˾Τ OR U=��ش� OR U=������ϩȲ�ƴ������� OR U=���� OR U=�������鵥�� OR U=����")
