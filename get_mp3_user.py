import pymysql
import sys

pymysql.install_as_MySQLdb()

conn = pymysql.connect(host='182.92.3.69',
                       user='lytian',
                       passwd="test123456",
                       db='pexels_video')
cur = conn.cursor()

user_num = sys.argv[1]

cur.execute(
    "SELECT user_id, url from mp3_user where is_scrapy = 0 order by id desc limit %s"
    % (user_num))

user_ids = []
urls = []
for r in cur:
    user_ids.append(f"'{r[0]}'")
    urls.append(r[1])

user_info = ','.join(urls) + '|' + ','.join(user_ids)

cur.close()
conn.close()

print(user_info)
