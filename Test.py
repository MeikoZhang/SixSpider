from zlib import crc32
import binascii
from zlib import crc32

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
v='/video/urls/v/1/toutiao/mp4/v020049b0000bfsf9ogckqbniar830v0?r=9635146186567141'
# print('0x%x' % (binascii.crc32(v.encode('utf-8')) & 0xffffffff))
print(crc32(v.encode('utf-8')))