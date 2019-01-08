#python urlencode
##1、对多个参数进行转换
data={'username':'02蔡彩虹', 'password':'ddddd?'}
s=urllib.parse.urlenscode(data)
##2、对一个字符串进行urlencode转换
s=urllib.parse.quote('长春')

#python urldecode
当urlencode之后的字符串传递过来之后，接受完毕就要解码了——urldecode
urllib提供了unquote()这个函数，可没有urldecode()
s=urllib.parse.unquote('%E5%B9%BF%E5%B7%9E')

#Beautiful Soup - 解析xml及html工具
https://cuiqingcai.com/1319.html

#Beautiful Soup 中文文档
https://blog.csdn.net/huazi_715/article/details/80907415

#python 常用 time, datetime处理
http://www.cnblogs.com/snow-backup/p/5063665.html
>>> time.time()
1450681042.751
int(time.time())可以获取整数部分

