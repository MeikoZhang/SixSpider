#解决InsecureRequestWarning警告
https://blog.csdn.net/zahuopuboss/article/details/52964809

#python爬虫 爬取今日头条信息
https://blog.csdn.net/yunfeiyang520/article/details/81674872

#python爬虫爬取今日头条APP数据（无需破解as ,cp，_cp_signature参数）
https://blog.csdn.net/weixin_39416561/article/details/84672104

#今日头条数据包分析
今日头条app数据包分析
<br/>
https://www.aliyun.com/zixun/wenji/1257913.html
<br/>
github内容
<br/>
https://github.com/jokermonn/-Api/blob/master/Todaynews.md

#App评论获取
http://is.snssdk.com/article/v3/tab_comments/?group_id=6647477440304120327&item_id=6647477440304120327&aggr_type=1&count=20&offset=0&device_id=61976341484
<br/>
group_id,item_id    内容相同，都为新闻唯一标识
<br/>
aggr_type   聚合方式，评论楼层格式。目前设为1不用改
<br/>
count,offset    分页属性
<br/>
device_id   设备id，可以固定值，如61976341484
<br/>
headers={
	"Accept-Encoding":"gzip",
	"User-Agent":"Dalvik/2.1.0 (Linux; U; Android 5.1.1; DUK-AL20 Build/LMY48Z) NewsArticle/6.8.2 okhttp/3.10.0.1",
	"Host":"is.snssdk.com",
	"Connection":"Keep-Alive"
}