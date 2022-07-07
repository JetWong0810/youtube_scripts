import pymysql
import sys

pymysql.install_as_MySQLdb()

conn = pymysql.connect(host='182.92.3.69',
                       user='lytian',
                       passwd="test123456",
                       db='pexels_video')
cur = conn.cursor()

audio_id = sys.argv[1]

cur.execute(
    "UPDATE mp3_info SET is_use = 1 where audio_id = '%s'"
    % audio_id)

conn.commit()
cur.close()
conn.close()
