from zlib import crc32
import random
import requests
import base64
import traceback
import pymysql
import time


conn = pymysql.connect(host="47.101.146.57", port=2018, user="root", password="Liuku!!!111", db="dm_report",
                     charset="utf8")
# db.autocommit(True)
cursor = conn.cursor(pymysql.cursors.SSCursor)
cursor.execute("select * from toutiao_video_latest where source_url_time < now() - interval 1 hour")
results = cursor.fetchall()
batch_sql=[]
if cursor:
    for row in results:
        id = row[0]
        source_site = row[1]
        video_id = row[3]
        source_url = row[10]

        # http://toutiao.com/group/
        if source_site.startswith('https://m.toutiao_video.com'):
            print("record id", id, time.strftime("%Y-%m-%d %H:%M:%S"))

            r = ''
            for i in range(0, 16):
                r = r + str(random.randint(1, 9))

            crc = crc32('/video/urls/v/1/toutiao/mp4/{}?r={}'.format(video_id, str(r)).encode('utf-8'))
            url = 'http://i.snssdk.com/video/urls/v/1/toutiao/mp4/{}?r={}&s={}'.format(video_id, r, crc)

            try:
                r = requests.get(url)
                r_json = r.json()
                video_list = r_json['data']['video_list']
                if video_list:
                    video_1 = video_list.get('video_1', None)
                    video_2 = video_list.get('video_2', None)
                    video_3 = video_list.get('video_3', None)
                    video_url = None
                    if video_3:
                        video_url = video_3
                    elif video_2:
                        video_url = video_2
                    elif video_1:
                        video_url = video_1
                    else:
                        print("no video", video_id, url)

                    if video_url:
                        if video_url.get('backup_url_1', None):
                            video_real_url = str(base64.b64decode(video_url['backup_url_1'].encode('utf-8')), 'utf-8')
                        else:
                            video_real_url = str(base64.b64decode(video_url['main_url'].encode('utf-8')), 'utf-8')
                        # print(video_real_url)
                        batch_sql.append((video_real_url, id))
            except Exception as e:
                print("somethings error", video_id, url)
                print(traceback.format_exc())

try:
    # cursor.execute("update toutiao_video_latest set source_url='{}',source_url_time=now() where id={}"
    #                .format(video_real_url, id))
    pre_sql = "update toutiao_video_latest set source_url=%s,source_url_time=now() where id=%s"
    update_count = cursor.executemany(pre_sql, batch_sql)
    conn.commit()
    print("execute batch sql over ,update count:", update_count, time.strftime("%Y-%m-%d %H:%M:%S"))
    cursor.close()
    conn.close()
except Exception as e:
    print("update sql error, batch sql :")
    print(batch_sql)
    print(traceback.format_exc())

