from zlib import crc32
import binascii
from zlib import crc32
import random
import requests
import base64
import traceback

# for a in range(0, 9):
#     for b in range(0, 9):
#         for c in range(0, 9):
#             for d in range(0, 9):
#                 r1 = a * 1000 + b * 100 + c * 10 + d
#                 r2 = d * 1000 + c * 100 + b * 10 + a
#                 if r1 *4 == r2:
#                     print(a, b, c, d)
# print(crc32('/video/urls/v/1/toutiao/mp4/{}?r={}'.format('v02004a70000bfse56nk43al9tdodpc0', '0027263879638553').encode('utf-8')))
# v='/video/urls/v/1/toutiao/mp4/v02004040000bg31ot72gddgigkg7kvg?r=7805700526977788'
# v='/video/urls/v/1/toutiao/mp4/v020049b0000bfsf9ogckqbniar830v0?r=9635146186567141'
# print('0x%x' % (binascii.crc32(v.encode('utf-8')) & 0xffffffff))
# print(crc32(v.encode('utf-8')))


def get_real_url(video_id):
    r = ''
    for i in range(0, 16):
        r = r + str(random.randint(1, 9))
    crc = crc32('/video/urls/v/1/toutiao/mp4/{}?r={}'.format(video_id, str(r)).encode('utf-8'))
    print(r, crc)
    url = 'http://i.snssdk.com/video/urls/v/1/toutiao/mp4/{}?r={}&s={}'.format(video_id, r, crc)
    print(url)
    try:
        r = requests.get(url)
        r_json = r.json()
        video_list = r_json['data']['video_list']
        print(video_list)
        if video_list:
            video_1 = video_list.get('video_1', None)
            video_2 = video_list.get('video_2', None)
            video_3 = video_list.get('video_3', None)
            if video_3:
                video_url = video_3
            elif video_2:
                video_url = video_2
            elif video_1:
                video_url = video_1
            else:
                print("no video", video_id, url)
                return None
            if video_url:
                print(str(base64.b64decode(video_url['main_url'].encode('utf-8')), 'utf-8'))
                print(str(base64.b64decode(video_url['backup_url_1'].encode('utf-8')), 'utf-8'))
                return str(base64.b64decode(video_url['main_url'].encode('utf-8')), 'utf-8')
    except Exception as e:
        print("somethings error", video_id, url)
        print(traceback.format_exc())
        return None


get_real_url("v02004d00000bfsdtacpg6251d461kkg")