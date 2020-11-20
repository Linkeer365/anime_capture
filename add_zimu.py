import cv2
import os
import sys

import textwrap

from PIL import ImageDraw,ImageFont,Image

import pymysql

# cv2写不了中文

# def writeText(img_path, text,img_path2,font_path):
#     # 加载背景图片
#     # img的类型是np.ndarray数组
#     img = cv2.imread(img_path)
#     # 在图片上添加文字信息
#     # 颜色参数值可用颜色拾取器获取（(255,255,255)为纯白色）
#
#     color_pack=(255,255,255)
#
#     # 最后一个参数bottomLeftOrigin如果设置为True，那么添加的文字是上下颠倒的
#     composite_img = cv2.putText(img, text, (100, 680), cv2.FONT_HERSHEY_DUPLEX,
#                                 2.0, color_pack, 5, cv2.LINE_4, False)
#     cv2.imwrite(img_path2, composite_img)

# 楷体字

font_path=r"C:\Windows\Fonts\STKAITI.TTF"

# 一个字大概占40像素

font_size=60

ori_upper_left_pt=(1920//4,0)

def add_border(img,upper_left_pt,shadowcolor,text):

    x,y=upper_left_pt
    font = ImageFont.truetype (font_path, size=font_size)
    draw = ImageDraw.Draw (img)

    # # thin border
    # draw.text ((x - 1, y), text, font=font, fill=shadowcolor)
    # draw.text ((x + 1, y), text, font=font, fill=shadowcolor)
    # draw.text ((x, y - 1), text, font=font, fill=shadowcolor)
    # draw.text ((x, y + 1), text, font=font, fill=shadowcolor)

    max_thick_scale=3

    # thicker border
    # draw.text ((x - thick_scale, y - thick_scale), text, font=font, fill=shadowcolor)
    # draw.text ((x + thick_scale, y - thick_scale), text, font=font, fill=shadowcolor)
    # draw.text ((x - thick_scale, y + thick_scale), text, font=font, fill=shadowcolor)
    # draw.text ((x + thick_scale, y + thick_scale), text, font=font, fill=shadowcolor)
    for thick_scale in range(1,max_thick_scale+1):
        draw.text ((x - thick_scale, y ), text, font=font, fill=shadowcolor)
        draw.text ((x + thick_scale, y ), text, font=font, fill=shadowcolor)
        draw.text ((x , y + thick_scale), text, font=font, fill=shadowcolor)
        draw.text ((x , y + thick_scale), text, font=font, fill=shadowcolor)

def get_color_pack(img):

    rgb_img = img.convert ("RGB")

    pixels = [(x, y) for x in range (480, 1440) for y in range (0, 60)]

    r_sum = 0
    g_sum = 0
    b_sum = 0
    pixel_cnt = len (pixels)

    for x, y in pixels:
        r, g, b = rgb_img.getpixel ((x, y))
        # print(f"r:{r} g:{g} b:{b}")
        r_sum += r
        g_sum += g
        b_sum += b

    r_conv = 256 - r_sum // pixel_cnt
    g_conv = 256 - g_sum // pixel_cnt
    b_conv = 256 - b_sum // pixel_cnt

    return (r_conv,g_conv,b_conv)

def get_conv_color(pack):
    return (256-pack[0],256-pack[1],256-pack[2])

def get_upper_left_pt(text_len):
    return ((1920-text_len*40)//2,0)

def writeText(text,img_path,img_path2):

    img=Image.open(img_path)
    draw=ImageDraw.Draw(img)

    font=ImageFont.truetype(font_path,size=font_size)

    # color_pack=(255,255,255)

    # 字幕颜色要随着背景色切换才好...

    # pick color-pack


    color_pack=get_color_pack(img)

    # color_pack2=get_conv_color(color_pack)

    color_pack2=(255,255,255)

    # color_pack=(16,53,24)

    upper_left_pt=get_upper_left_pt(len(text))

    add_border(img,upper_left_pt,color_pack2,text)

    draw.text(upper_left_pt,text,font=font,fill=color_pack)

    # img.show()

    img.save(img_path2)

# writeText("哈哈哈", \
#           r"D:\text_animes\3-41.jpg", \
#           r"D:\text_animes\3-41.jpg", \
#           r"C:\Windows\Fonts\STKAITI.TTF", \
#           65, \
#           (1920//4,0),
#           )
#
# sys.exit(0)



db_name="DB_Animes"
db=pymysql.connect("localhost","root","cc",db_name)
cursor=db.cursor()

# img_dir=r"D:\Alldowns"

# anime_name='Madoka'

def add_zimu(img_dir,anime_name,overwrite=False):

    select_stat=f"SELECT anime_name,episode_num, img,text FROM {anime_name} WHERE is_missing=1"

    cursor.execute(select_stat)

    res=cursor.fetchall()



    cnt=0

    for anime_name,episode_num,img_path, text in res:

        if overwrite:
            img_dir=img_path.rsplit(os.sep,maxsplit=1)[0]
            img_dir2=img_dir
        else:
            img_dir2 = f"{img_dir}{os.sep}{anime_name}{os.sep}{episode_num}"

        os.makedirs(img_dir2,exist_ok=True)
        if text!='':
            print("text:",text)
            img_name=img_path.rsplit(os.sep,maxsplit=1)[-1]
            img_path2=f"{img_dir2}{os.sep}{img_name}"
            writeText(text,img_path,img_path2)
            print("one done.")
            # if cnt>=11:
            #     break
            # cnt+=1

def main():
    anime_names=["Madoka","Katanagatari"]

    img_dir=r"D:\text_animes"

    for anime_name in anime_names:
        add_zimu(img_dir,anime_name,overwrite=True)

if __name__ == '__main__':
    main()