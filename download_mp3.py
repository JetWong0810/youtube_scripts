import pymysql
import sys
import os

pymysql.install_as_MySQLdb()

conn = pymysql.connect(host='182.92.3.69',
                       user='lytian',
                       passwd="test123456",
                       db='pexels_video')
cur = conn.cursor()

# download_num = sys.argv[1]
license_like = 'cc-by'

cur.execute(
    "SELECT audio_id, url from mp3_info where is_download = 0 and is_use = 0 and is_del = 0 and license like '%s' limit 20"
    % ('%' + license_like + '%'))

cur.close()
conn.close()

mp3_index = 1
for r in cur:
    print(f"开始下载第{mp3_index}个音频:{r[0]}")
    mp3_path = os.getenv('YOUTUBE_FILE_PATH') + '/mp3/'
    os.system(f"scdl -l {r[1]} -t -c --path {mp3_path}")
    mp3_index = mp3_index + 1
