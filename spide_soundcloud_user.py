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

proxies = {'http': 'http://127.0.0.1:8118', 'https': 'http://127.0.0.1:8118'}

url = 'https://api-v2.soundcloud.com/users/1119855181/followings?client_id=Q3TqwxKP5NC07Tk7ORBDLjc981jtRBGS&limit=200&offset=0&linked_partitioning=1&app_version=1656488185&app_locale=en'

r = requests.get(url, proxies=proxies, headers=headers)

r.encoding = 'UTF-8'

user_list = json.loads(r.text)

print(user_list)

for u in user_list['collection']:
    user = u
    user['username'] = pymysql.converters.escape_string(str(user['username']))
    insert_item = (user['id'], user['username'], user['followers_count'],
                   user['city'], user['country_code'], user['permalink_url'])

    cur.execute("SELECT user_id from mp3_user where user_id = %s", user['id'])

    if cur.rowcount > 0:
        print(user['id'])
        continue

    cur.execute(
        "INSERT INTO mp3_user(user_id, username, followers_count, city, country_code, url) VALUES('%s', '%s', '%s', '%s', '%s', '%s')"
        % insert_item)

conn.commit()

cur.close()
conn.close()
