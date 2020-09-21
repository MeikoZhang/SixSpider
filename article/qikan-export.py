# coding=gbk

import time
import os
import socket
import EasySqlite

socket.setdefaulttimeout(30)
# base_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
base_path = r"E:\文档"
# base_path = r'/Users/krison/Documents/文档'
cur_day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
# 导出因权限问题新增未下载的文件
export_preserve_start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# 连接目录表Sqlite
db = EasySqlite.EasySqlite(os.path.join(base_path, r"article/article.db"))

file_dir = os.path.join(base_path, "中国知网", cur_day)
if os.path.exists(file_dir):
    print("目录{}已存在，下载文件中...".format(file_dir))
else:
    print("目录{}不存在，创建该目录...".format(file_dir))
    os.mkdir(file_dir)


def export_preserve(export_dir, start_time):
    export_file_name = os.path.join(export_dir, '无权限文件.txt')

    export_results = db.execute("select title,author,authors,create_time from article_preserve where source='中国知网' and type='期刊' and create_time>='{}'".format(start_time))
    with open(export_file_name, 'w') as fp:
        ei = 1
        fp.truncate()
        if len(export_results) > 0:
            fp.write('序号 | 标题 | 首作者 | 作者\n')
            for result in export_results:
                fp.write('{} | {} | {} | {}\n'.format(ei, result['title'], result['author'], result['authors']))
                ei += 1
            print('导出文件完成。\n')
        else:
            fp.write('没有需要导出的文件。\n')


export_preserve(file_dir, '2020-09-21')
print(">>>>>>>>>>无权限文件导出完成 .................")
