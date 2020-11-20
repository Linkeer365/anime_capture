# prompt for missings

import cv2

import pymysql
import mysql.connector

import os

def is_missing(img_path):

    img=cv2.imread(img_path)

    cv2.namedWindow('kk',cv2.WINDOW_AUTOSIZE)

    cv2.moveWindow('kk',100,100)

    # width=12
    #
    # height=8

    width=128
    height=int((4/9)*width)
    scale=5

    cube=(width*scale,height*scale)

    img=cv2.resize (img, cube, interpolation=cv2.INTER_CUBIC)

    # cv2.resizeWindow (img_path, int (width * (height - 80) / height), height - 80);

    cnt=0

    res_fst=cv2.waitKey(1)

    while res_fst==-1:
        cv2.imshow('kk',img)

        # esc -> 27
        # \r -> enter -> 13

        # missing 对应 esc
        # good 对应 enter

        esc_ord=27
        enter_ord=13
        small_c_ord=99

        res=cv2.waitKey(5000)

        print(res)

        if res==-1:
            print("wait too long!")
            continue
        elif res==esc_ord:
            print("missing!")
            return 1
        elif res==enter_ord:
            return 0
        elif res==small_c_ord:
            # c for change
            # 自己到时候手动改周边
            return 99




    # raise TimeoutError

# is_missing(r"D:\crop_animes\Madoka\crop_12\0-0.jpg")

# db connect

anime_dir=r"D:\AllDowns"

db_name="DB_Animes"
db=pymysql.connect("localhost","root","cc",db_name)
cursor=db.cursor()

anime_name="Madoka"

def get_missing_field(anime_name):

    anime_path=f"{anime_dir}{os.sep}{anime_name}"

    missing_res_path = f"{anime_path}{os.sep}missing_res.txt"

    try:
        add_table_statement=f"ALTER TABLE {anime_name} ADD is_missing TINYINT(1)"
        cursor.execute(add_table_statement)
    except pymysql.err.OperationalError:
        pass

    select_path_statement=f"SELECT img FROM {anime_name}"
    cursor.execute(select_path_statement)

    img_paths=[each[0] for each in cursor.fetchall()]


    if os.path.exists(missing_res_path):
        with open(missing_res_path,"r",encoding="utf-8") as f:
            already_len=len([each for each in f.readlines() if os.sep in each])
    else:
        already_len=0

    print("img_paths:",len(img_paths))
    print("already len:",already_len)



    for img_path in img_paths[already_len:]:

        if img_path==None:
            continue

        print("img path:",img_path)

        res=is_missing(img_path)

        with open(missing_res_path,"a",encoding="utf-8") as f:
            f.write("\n")
            res_s=str(res)
            f.write(f"{img_path}\t{res_s}")
            f.write("\n")
            # print("one done")

    # missings=()

    with open(missing_res_path,"r",encoding="utf-8") as f:
        missings=[int(each.split("\t")[-1].strip("\n")) for each in f.readlines() if each!='\n']

    with open(missing_res_path,"r",encoding="utf-8") as f:
        img_paths = [each.split ("\t")[0] for each in f.readlines () if each != '\n']


    print(missings)
    print(img_paths)

    missings=list(zip(missings,img_paths))
    print(missings[0])



    insert_statement=f"UPDATE {anime_name} SET is_missing=%s WHERE img=%s"
    # print("gg.")
    cursor.executemany(insert_statement,missings)

    db.commit()

    print(cursor.rowcount,"done.")


def main():
    anime_names=["Madoka","Katanagatari"]

    for anime_name in anime_names:
        get_missing_field(anime_name)

if __name__ == '__main__':
    main()


