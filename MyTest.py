import execjs

import execjs

#参考https://blog.csdn.net/weixin_39416561/article/details/82111455
def get_js():
    f = open(r"D:\Github\SixSpider\signature.js", 'r', encoding='UTF-8')  ##打开JS文件
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    ctx = execjs.compile(htmlstr)
    return ctx.call('get_as_cp_signature')

get_js