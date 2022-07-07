from fileinput import filename
from venv import create
import requests
import json
import pymysql

pymysql.install_as_MySQLdb()

conn = pymysql.connect(host='182.92.3.69',
                       user='lytian',
                       passwd="test123456",
                       db='pexels_video')
cur = conn.cursor()

headers = {
    'Authorization': 'OAuth 2-290059-1119855181-lePrTiefzfTOC',
    'Origin': 'https://soundcloud.com',
    'Host': 'api-v2.soundcloud.com',
    'Referer': 'https://soundcloud.com/',
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
    'sec-ch-ua':
    '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site'
}

# proxies = {'http': 'http://127.0.0.1:8118', 'https': 'http://127.0.0.1:8118'}
proxies = {}

duration_map = ['short', 'medium', 'long', 'epic']

keyword = 'piano'
license = 'to_use_commercially'
duration = duration_map[2]
offset = 0

cur.execute(
    "SELECT offset from mp3_search_params where keyword = '%s' and license = '%s' and duration = '%s' order by id desc limit 1"
    % (keyword, license, duration))

for r in cur:
    offset = r[0] + 20

url = f"https://api-v2.soundcloud.com/search/tracks?q={keyword}&sc_a_id=76070cf99f723dfc916b052cedcf146c3b2b1dc5&variant_ids=&filter.duration={duration}&filter.license={license}&facet=genre&user_id=131757-272304-653894-372073&client_id=Q3TqwxKP5NC07Tk7ORBDLjc981jtRBGS&limit=20&offset={offset}&linked_partitioning=1&app_version=1656488185&app_locale=en"

r = requests.get(url, proxies=proxies, headers=headers)

r.encoding = 'UTF-8'

mp3_list = json.loads(r.text)

for mp3 in mp3_list['collection']:
    mp3['title'] = pymysql.converters.escape_string(str(mp3['title']))
    mp3['genre'] = pymysql.converters.escape_string(str(mp3['genre']))
    mp3['tag_list'] = pymysql.converters.escape_string(str(mp3['tag_list']))
    insert_item = (mp3['id'], mp3['user']['id'], '', mp3['title'],
                   mp3['permalink_url'], mp3['duration'], mp3['genre'],
                   mp3['kind'], mp3['license'], int(mp3['likes_count'] or 0),
                   mp3['tag_list'])

    cur.execute("SELECT audio_id from mp3_info where audio_id = %s", mp3['id'])

    if cur.rowcount > 0:
        print(f"{mp3['id']}已存在")
        continue

    cur.execute(
        "INSERT INTO mp3_info(audio_id, user_id, filename, title, url, duration, genre, kind, license, likes_count, tags) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
        % insert_item)

    print(f"{mp3['id']}下载成功")

insert_search_params = (keyword, license, duration, '', offset)
cur.execute(
    "INSERT INTO mp3_search_params(keyword, license, duration, begin_time, offset) VALUES('%s', '%s', '%s', '%s', '%s')"
    % insert_search_params)

conn.commit()

cur.close()
conn.close()

print(f"本次音频信息抓取完毕")
