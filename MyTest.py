import execjs

import execjs
from selenium import webdriver #先导入selenium模块，没安装的自行百度安装就好

#参考https://blog.csdn.net/weixin_39416561/article/details/82111455
def get_js():
    f = open(r"D:\GitHub\SixSpider\signature.js", 'r', encoding='UTF-8')  ##打开JS文件
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    ctx = execjs.compile(htmlstr)
    return ctx.call('get_as_cp_signature')




