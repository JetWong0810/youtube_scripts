import pymysql
import sys

pymysql.install_as_MySQLdb()

conn = pymysql.connect(host='182.92.3.69',
                       user='lytian',
                       passwd="test123456",
                       db='pexels_video')
cur = conn.cursor()

video_num = sys.argv[1]

cur.execute(
    "SELECT video_id, file_path, title, tags, keyword from video_info where is_download = 1 and is_use = 0 and is_del = 0 limit %s"
    % video_num)

video_list = []
for r in cur:
    video_list.append(r[0])

mp4_str = ','.join(str(i) for i in video_list)

cur.close()
conn.close()

print(mp4_str)
