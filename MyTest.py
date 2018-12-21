import execjs

import execjs
import os
import selenium
import json
import db.MysqlUtil as mu
import db.PgUtil as pu
import requests
from selenium import webdriver


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"')
driver = webdriver.Chrome(chrome_options=chrome_options)
# 打开百度首页，可以更换引号内的网址实现打开任一网址
driver.get('http://toutiao.com/group/6637083530188816904/')
# 在编辑器的终端可以看到网站的标题打印出来
print(driver.page_source)
# 关闭Chrome浏览器，如果不写这句话浏览器就会停留在百度首页在后台运行不会关闭浏览器
driver.quit()
