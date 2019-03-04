# -*- coding:utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup

# 进入浏览器设置
options = webdriver.ChromeOptions()
# 设置中文
# options.add_argument('lang=zh_CN.UTF-8')
# 更换头部
options.add_argument('--headless')
options.add_argument('user-agent="Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36"')
browser = webdriver.Chrome(executable_path="chromedriver", chrome_options=options)

url = "http://toutiao.com/group/6632271016603157006/"
browser.get(url)
ps = browser.page_source
# print(ps)

soup = BeautifulSoup(ps, "lxml")
print(soup.select('.article__content'))

browser.quit()
