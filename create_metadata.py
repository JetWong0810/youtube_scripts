import pymysql
import sys
import json
import datetime
import spacy
import re
import enchant
import os

pymysql.install_as_MySQLdb()

conn = pymysql.connect(host='182.92.3.69',
                       user='lytian',
                       passwd="test123456",
                       db='pexels_video')
cur = conn.cursor()

en = spacy.load('en_core_web_sm')
sw_spacy = en.Defaults.stop_words

mp3_id = sys.argv[1]
mp4_id = sys.argv[2]
folder_index = f"{mp4_id}_{mp3_id}"

metadata_dict = {}
title = ''
tags = ''

cur.execute("SELECT title, keyword from video_info where video_id = %s" %
            mp4_id)

for r in cur:
    tags = r[0] + ' ' + r[1]
    title = r[0]

cur.execute("SELECT title, genre, tags from mp3_info where audio_id = %s" %
            mp3_id)

for r in cur:
    cop = re.compile("[^a-z^A-Z\s*]")
    mp3_title_str = cop.sub('', r[0])
    mp3_genre_str = cop.sub('', r[1])
    mp3_tags_str = cop.sub('', r[2])

    tags = tags + ' ' + mp3_title_str + ' ' + mp3_genre_str + ' ' + mp3_tags_str
    try:
        if len(r[1]) == 0:
            title = f"{title} | For Relax And Enjoy Yourself"
        else:
            title = f"{title} - {r[1]}"
    except Exception:
        title = f"{title} | For Relax And Enjoy Yourself"

    title = title.title()

tags_arr = tags.split(' ')
tags_filter_null = list(filter(None, tags_arr))
tags_filter_repeat = list(set(tags_filter_null))
words = [word for word in tags_filter_repeat if word.lower() not in sw_spacy]

significant_words = []
d = enchant.Dict("en_US")
for word in words:
    if d.check(word):
        significant_words.append(word)

description = f"{title}\n- Help us 1000 subscribes : https://www.youtube.com/channel/UCcDibumKywWD0eLSnKD8Zeg\nThanks for watching\nhealing music,soft guitar,relaxing guitar music,calming music,relaxing music,sleep music,calm music,healing music,study music,stress relief music,sleeping music,soothing music,peaceful music,sleep meditation,soft music,binaural beats,music for sleep,relaxing sleep music,deep sleep music,SoundCloud,SoundCloud music,calming music SoundCloud,relaxing music SoundCloud,sleep music SoundCloud,calm music SoundCloud,healing music SoundCloud,study music SoundCloud,pexels,pexels video,beautiful melody\nPlease follow and subscribe to our channel if you want more Relax Music. Don't forget to share our channel with your friends.\nThanks Fan so much for watching, sharing, commenting and Like !!!\nHave a nice day, we'll be back before you know!\nFollow SoundCloud Music: \nSubcribe: https://www.youtube.com/channel/UCcDibumKywWD0eLSnKD8Zeg\n{significant_words}"

meta_dict = {
    'title': title,
    'tags': significant_words,
    'description': description
}

today = datetime.date.today()
upload_dir = os.getenv('YOUTUBE_FILE_PATH') + '/upload'
meta_file_path = '%s/%s/%s/metadata.json' % (upload_dir, today, folder_index)
with open(meta_file_path, "w") as f:
    json.dump(meta_dict, f)

cur.close()
conn.close()
