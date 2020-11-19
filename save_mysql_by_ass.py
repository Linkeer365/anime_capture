import cv2
import os

import mysql.connector

import pymysql


# video_path=r"D:\AllDowns\Madoka\[Madoka][01].mp4"
#
# capture_dir=r"D:\AllDowns\Madoka"
#
# capture_time_in_millisecond=20000

# global variables

video_dir=r"D:\AllDowns\Madoka"

anime_name="Madoka"
video_suffix="mp4"

assert anime_name in video_dir
zimu_dir=r"D:\AllDowns\Madoka\Madoka_zimu"


# db create

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


def colon2millisecond(colon_time):
    assert "." in colon_time
    assert ":" in colon_time
    int_part,decimal_part=colon_time.split(".")
    _,minute,second=int_part.split(":")

    secs=60*int(minute)+int(second)+0.01*int(decimal_part)

    return secs*1000

def millisecond2hyphen(millisecond):
    secs=millisecond//1000
    assert secs<=3600

    minute,second=divmod(secs,60)

    return f"{minute}-{second}"


def capture_at(vidcap,capture_dir,colon_start_time,colon_end_time):

    # return hyphen_capture_time

    start_time_in_millisecond=colon2millisecond(colon_start_time)
    end_time_in_millisecond=colon2millisecond(colon_end_time)

    mid_time_in_millisecond=int((start_time_in_millisecond+end_time_in_millisecond)//2)

    # print("start time:",start_time_in_millisecond)

    # https://stackoverflow.com/questions/27481993/extracting-image-from-video-at-a-given-time-using-opencv

    vidcap.set(cv2.CAP_PROP_POS_MSEC,mid_time_in_millisecond)

    print("mid time:",mid_time_in_millisecond)

    # vidcap.set(cv2.CAP_PROP_POS_MSEC,mid_time_in_millisecond)      # just cue to 20 sec. position
    success,image = vidcap.read()

    if success:
        hyphen_capture_time=millisecond2hyphen(mid_time_in_millisecond)

        image_path=f"{capture_dir}{os.sep}{hyphen_capture_time}.jpg"

        cv2.imwrite(image_path, image)     # save frame as JPEG file
        # cv2.imshow("20sec",image)
        cv2.waitKey()
        print("one cap done.")
        return hyphen_capture_time,image_path
    else:
        print("one cap failed!")
        return None,None

def main():

    # get time texts(zimu = 字幕)

    packs=[]

    for zimu in os.listdir(zimu_dir):
        assert zimu.endswith(".ass")
        zimu_path=f"{zimu_dir}{os.sep}{zimu}"

        episode_num=zimu.split(" ")[0]

        with open(zimu_path,"r",encoding="utf-8") as f:
            zimu_lines=f.readlines()

        print("zimu lines:",zimu_lines)

        cn_packs=[]

        # raw_ep01 format
        # '0:11:04.51'$\t'0:11:06.75'$\t'ねえ まどか あの子知り合い'

        zimu_raw_path = f"{zimu_dir}{os.sep}raw_ep{episode_num}.txt"

        for line in zimu_lines:
            if line.startswith("Dialogue:") and line.split(",")[3]=="CNsub":
                # 'Dialogue: 0', '0:11:04.51', '0:11:06.75', 'JPsub', 'NTP', '0', '0', '0', '', 'ねえ まどか あの子知り合い'
                items=line.split(",")
                colon_start_time,colon_end_time=items[1:3]
                text=items[-1].strip("\n")
                cn_pack=(colon_start_time,colon_end_time,text)
                cn_packs.append(cn_pack)

        print("cn pack:",cn_packs)

        video_name=f"[{anime_name}][{episode_num}]"
        video_path=f"{video_dir}{os.sep}{video_name}.{video_suffix}"
        capture_dir=f"{video_dir}{os.sep}{video_name}"

        os.makedirs (capture_dir, exist_ok=True)
        vidcap = cv2.VideoCapture (video_path)

        print("video path:",video_path)
        print("vidcap:",vidcap)

        new_cn_packs=[]

        for cn_pack in cn_packs:
            colon_start_time,colon_end_time,text=cn_pack
            hyphen_time,img_path=capture_at(vidcap,capture_dir,colon_start_time,colon_end_time)
            new_cn_pack=(anime_name,episode_num,hyphen_time,img_path,text)
            new_cn_packs.append(new_cn_pack)

            new_cn_pack_s="$\t".join(new_cn_pack)

            with open(zimu_raw_path,"a",encoding="utf-8") as f:
                f.write("\n")
                f.write(new_cn_pack_s)
                f.write("\n")

        packs.extend(new_cn_packs)

    print("packs",packs[0])
    table_name="Madoka"
    create_fields_comm=f"CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, anime_name VARCHAR(255), episode_num VARCHAR(255), capture_time VARCHAR(255), img LONGBLOB NOT NULL, text VARCHAR(255))"
    # create table with fields
    cursor2.execute(create_fields_comm)
    # 注意id是不能insert的
    insert_statement=f"INSERT INTO {table_name} (anime_name,episode_num,capture_time,img,text) VALUES (%s,%s,%s,%s,%s)"
    cursor2.executemany(insert_statement,packs)
    db2.commit()
    print(cursor2.rowcount,"插入成功")

if __name__ == '__main__':
    main()





















