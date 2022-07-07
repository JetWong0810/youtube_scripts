import pymysql
import sys

pymysql.install_as_MySQLdb()

conn = pymysql.connect(host='182.92.3.69',
                       user='lytian',
                       passwd="test123456",
                       db='pexels_video')
cur = conn.cursor()

mp3_num = sys.argv[1]
license_like = 'cc-by'

cur.execute(
    "SELECT audio_id, filename, title, genre, tags from mp3_info where is_download = 1 & is_use = 0 and is_del = 0 and license like '%s' order by likes_count limit %s"
    % ('%' + license_like + '%', mp3_num))

mp3_list = []
for r in cur:
    mp3_list.append(r[0])

mp3_str = ','.join(str(i) for i in mp3_list)

cur.close()
conn.close()

print(mp3_str)
