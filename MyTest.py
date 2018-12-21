
import time
import execjs
import os
import selenium
import json
import db.MysqlUtil as mu
import db.PgUtil as pu
import requests
from selenium import webdriver

t1=time.time()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"')
driver = webdriver.Chrome(chrome_options=chrome_options)

t2=time.time()
# 打开百度首页，可以更换引号内的网址实现打开任一网址
driver.get('https://m.toutiaoimg.cn/i6580854257686154499/#mid=1574175703010317')
# 在编辑器的终端可以看到网站的标题打印出来
# print(driver.page_source)
print(driver.find_element_by_id('xigua-video-player').find_element_by_tag_name('source').get_attribute('src'))
# 关闭Chrome浏览器，如果不写这句话浏览器就会停留在百度首页在后台运行不会关闭浏览器
t3=time.time()

driver.quit()

t4=time.time()
print(t1, t2, t3, t4)
