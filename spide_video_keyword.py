from urllib import request
import json
import pymysql
from http import cookiejar
import ssl

pymysql.install_as_MySQLdb()

conn = pymysql.connect(host='182.92.3.69',
                       user='lytian',
                       passwd="test123456",
                       db='pexels_video')
cur = conn.cursor()

headers = {
    'Host': 'www.pexels.com',
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language':
    'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Cache-Control': 'max-age=0'
}

url = 'https://www.pexels.com/_next/data/tAjyqdrj8ZyfF6ruiZstA/en-US/popular-searches.json'

cookie = cookiejar.MozillaCookieJar("cookie.txt")

context = ssl._create_unverified_context()

cookie_handler = request.HTTPCookieProcessor(cookie)
http_handler = request.HTTPHandler()
https_handler = request.HTTPSHandler(context=context)

opener = request.build_opener(cookie_handler, http_handler, https_handler)

r = request.Request(url, headers=headers)

response = opener.open(r)

popular_categorys = json.loads(response.read().decode('utf-8'))

for video in popular_categorys['pageProps']['initialData']['data']:
    insert_item = (video['id'], video['id'])

    cur.execute("SELECT keyword from video_keyword where keyword = %s",
                video['id'])

    if cur.rowcount == 0:
        cur.execute("INSERT INTO video_keyword(keyword, category) VALUES('%s', '%s')" %
                    insert_item)
        print(f"关键词:{video['id']}抓取成功")

    print(f"{video['id']}已存在")

    child_url = f"https://www.pexels.com/_next/data/tAjyqdrj8ZyfF6ruiZstA/en-US/search/{video['id']}.json?query={video['id']}"

    print(f"抓取子类url:{child_url}")

    r = request.Request(child_url, headers=headers)

    response = opener.open(r)

    child_categorys = json.loads(response.read().decode('utf-8'))

    for item in child_categorys['pageProps']['initialData']['meta'][
            'related_searches']:
        insert_item = (item['term'], video['id'])

        cur.execute("SELECT keyword from video_keyword where keyword = %s",
                    item['term'])

        if cur.rowcount == 0:
            cur.execute("INSERT INTO video_keyword(keyword, category) VALUES('%s', '%s')" %
                        insert_item)
            print(f"子类关键词:{item['term']}抓取成功")

        print(f"{item['term']}已存在")

conn.commit()

cur.close()
conn.close()

print(f"本次视频关键词抓取完毕")
