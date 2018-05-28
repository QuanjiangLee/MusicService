#!/usr/bin/env python

import json
import sqlite3
import requests
dataList = None
with open('song.txt', 'r') as f:
    dataList = json.loads(f.read())
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
cursor.execute("DELETE FROM serviceApp_songsInf;")
print("删除：", cursor.rowcount)
sql = "insert into serviceApp_songsInf(song_name, song_author, song_url,song_lyric) values (?, ?, ?, ?);"
for data in dataList:
    values = (data["songAttr"]["所属专辑"],data["songAttr"]["演唱者"],data["url"],data["songWord"].replace("\'",chr(39)))
    cursor.execute(sql, values)
    print("添加：", cursor.rowcount)
cursor.close()
conn.commit()
conn.close()
