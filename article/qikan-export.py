# coding=gbk

import time
import os
import socket
import EasySqlite

socket.setdefaulttimeout(30)
# base_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
base_path = r"E:\�ĵ�"
# base_path = r'/Users/krison/Documents/�ĵ�'
cur_day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
# ������Ȩ����������δ���ص��ļ�
export_preserve_start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# ����Ŀ¼��Sqlite
db = EasySqlite.EasySqlite(os.path.join(base_path, r"article/article.db"))

file_dir = os.path.join(base_path, "�й�֪��", cur_day)
if os.path.exists(file_dir):
    print("Ŀ¼{}�Ѵ��ڣ������ļ���...".format(file_dir))
else:
    print("Ŀ¼{}�����ڣ�������Ŀ¼...".format(file_dir))
    os.mkdir(file_dir)


def export_preserve(export_dir, start_time):
    export_file_name = os.path.join(export_dir, '��Ȩ���ļ�.txt')

    export_results = db.execute("select title,author,authors,create_time from article_preserve where source='�й�֪��' and type='�ڿ�' and create_time>='{}'".format(start_time))
    with open(export_file_name, 'w') as fp:
        ei = 1
        fp.truncate()
        if len(export_results) > 0:
            fp.write('��� | ���� | ������ | ����\n')
            for result in export_results:
                fp.write('{} | {} | {} | {}\n'.format(ei, result['title'], result['author'], result['authors']))
                ei += 1
            print('�����ļ���ɡ�\n')
        else:
            fp.write('û����Ҫ�������ļ���\n')


export_preserve(file_dir, '2020-09-21')
print(">>>>>>>>>>��Ȩ���ļ�������� .................")
