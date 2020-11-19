import mysql.connector

import pymysql

import os

import time

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def get_packs(video_dir):

    packs=[]

    for root,dir,piclist in os.walk(video_dir):
        if not dir:
            anime_episode=root.rsplit(os.sep,maxsplit=1)[-1]

            anime_fst=find_nth(anime_episode,"[",1)+1
            anime_last=find_nth(anime_episode,"]",1)

            episode_fst=find_nth(anime_episode,"[",2)+1
            episode_last=find_nth(anime_episode,"]",2)


            anime_name=anime_episode[anime_fst:anime_last]
            episode_num=anime_episode[episode_fst:episode_last]

            for pic in piclist:
                capture_time=pic.split(".")[0].rsplit("_",maxsplit=1)[-1]
                img_path=f"{root}{os.sep}{pic}"

                # with open(img_path,"rb") as f:
                #     img=f.read()

                text="NN"

                pack=(anime_name,episode_num,capture_time,img_path,text)
                packs.append(pack)

                print("Pack Add:",pack[0:3])

    return packs

# madoka_dir=r"D:\AllDowns\Madoka"



db_name="DB_Animes"

db1 = mysql.connector.connect(
    host="localhost",       # 数据库主机地址
    user="root",    # 数据库用户名
    passwd="cc",   # 数据库密码
    auth_plugin="mysql_native_password" # 8.0以上的版本需要使用插件！
)

print(db1)

cursor1=db1.cursor()

# create db
try:
    cursor1.execute(f"CREATE DATABASE {db_name}")
except mysql.connector.errors.DatabaseError:
    cursor1.execute(f"DROP DATABASE {db_name}")
    cursor1.execute(f"CREATE DATABASE {db_name}")

db1.close()



db2 = pymysql.connect("localhost","root","cc",db_name)
print(db2)

cursor2 = db2.cursor ()

def add_table(table_name,anime_dir):
    table_name="Madoka"
    create_fields_comm=f"CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, anime_name VARCHAR(255), episode_num VARCHAR(255), capture_time VARCHAR(255), img_path VARCHAR(255), text VARCHAR(255))"
    # create table with fields
    cursor2.execute(create_fields_comm)
    # 注意id是不能insert的
    insert_statement=f"INSERT INTO {table_name} (anime_name,episode_num,capture_time,img_path,text) VALUES (%s,%s,%s,%s,%s)"
    packs=get_packs(anime_dir)
    cursor2.executemany(insert_statement,packs)
    db2.commit()
    print(cursor2.rowcount,"插入成功")

names_dirs={"Madoka":"D:\AllDowns\Madoka",
            "Katanagatari":"D:\AllDowns\Katanagatari"}

for name,dir in names_dirs.items():
    startAt=time.time()
    add_table(name,dir)
    endAt=time.time()
    print("one done.")
    print("Time Cost:",endAt-startAt)
    break

print("all done.")


# insert lines






