import os
import pytesseract
import sys

import pymysql

import numpy as np

from matplotlib import pyplot as plt

import cv2

# 首先要知道绝对坐标是多少
# 详见： http://breakthrusoftware.com/html/onlinedocs/kb/installkb/ScreenCoordTool.html

# 就硬试，知道了绝对坐标其实不算太难...upper_left_pt=(288,543) (288,643) (288,593) (278,678)



crop_animes_dir=r"d:/crop_animes"

os.makedirs(crop_animes_dir,exist_ok=True)

# upper_left_pt = (289,638)
# upper_left_pt = (458,618)
# width = 525
# height = 58
# origin_upper_left_pt = (288,183)

def test(image_path):

    image=cv2.imread(image_path)

    # cv2.imshow('kk',image)
    # cv2.waitKey(0)

    upper_left_pt = (458,618)
    width = 525
    height = 58
    origin_upper_left_pt = (288,183)

    x1,y1=upper_left_pt
    x2,y2=x1+width,y1+height

    x0,y0=origin_upper_left_pt

    x1-=x0
    y1-=y0

    x2-=x0
    y2-=y0

    img=image[y1:y2,x1:x2]

    cv2.imshow('kk',img)
    cv2.waitKey(0)

# test(r"D:\AllDowns\Katanagatari\[Katanagatari][01]\0-2.jpg")
# sys.exit(0)


class Anime:
    def __init__(self,anime_name,anime_dict):
        self.anime_name=anime_name
        self.anime_dict = anime_dict
        self.upper_left_pt=self.anime_dict['upper_left_pt']
        self.width=self.anime_dict['width']
        self.height=self.anime_dict['height']
        self.origin_upper_left_pt=self.anime_dict['origin_upper_left_pt']

    def crop_img(self,image):
        upper_left_pt = self.upper_left_pt
        width = self.width
        height = self.height
        origin_upper_left_pt = self.origin_upper_left_pt

        # print(upper_left_pt)
        # print(width)
        # print(height)
        # print(origin_upper_left_pt)

        x1, y1 = upper_left_pt
        x2, y2 = x1 + width, y1 + height

        x0, y0 = origin_upper_left_pt

        x1 -= x0
        y1 -= y0

        x2 -= x0
        y2 -= y0

        img = image[y1:y2, x1:x2]

        # cv2.imshow('kk',img)

        return img

    def image_ocr(self, image_path, crop_dir):
        anime_dict = self.anime_dict

        image = cv2.imread (image_path)

        image_file = image_path.rsplit (os.sep, maxsplit=1)[-1]

        # resize https://www.cnblogs.com/lfri/p/10596530.html

        # 之所以会有tile-cannot-extend-outside-image，是因为在这里缩小了

        # image=cv2.resize(image,None,fx=0.6,fy=0.6,interpolation=cv2.INTER_AREA)

        # cv2.imshow('k',image)
        # cv2.waitKey(0)

        gray_img = cv2.cvtColor (image, cv2.COLOR_BGR2GRAY)

        # gray_img=image

        upper_left_pt = anime_dict['upper_left_pt']
        width = anime_dict['width']
        height = anime_dict['height']
        origin_upper_left_pt = anime_dict['origin_upper_left_pt']

        # print("gg.")
        # ok

        gray_img = self.crop_img (image)

        # print(type(gray_img))

        # print("gg.")

        # grey1=cv2.threshold(GrayImage,127,255,cv2.THRESH_BINARY)

        # cv2.imshow ('kk',image)
        # cv2.waitKey(0)
        # sys.exit (0)

        # ret, thresh1 = cv2.threshold (GrayImage, 127, 255, cv2.THRESH_BINARY)
        # ret, thresh2 = cv2.threshold (GrayImage, 127, 255, cv2.THRESH_BINARY_INV)
        # ret, thresh3 = cv2.threshold (GrayImage, 127, 255, cv2.THRESH_TRUNC)
        # ret, thresh4 = cv2.threshold (GrayImage, 127, 255, cv2.THRESH_TOZERO)
        # ret, thresh5 = cv2.threshold (GrayImage, 127, 255, cv2.THRESH_TOZERO_INV)
        # titles = ['Gray Image', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
        # images = [GrayImage, thresh1, thresh2, thresh3, thresh4, thresh5]
        # for i in range (6):
        #     plt.subplot (2, 3, i + 1), plt.imshow (images[i], 'gray')
        #     plt.title (titles[i])
        #     plt.xticks ([]), plt.yticks ([])
        # plt.show ()

        # sys.exit(0)

        # img=crop_img(gray_img,upper_left_pt,width,height,origin_upper_left_pt)

        code = pytesseract.image_to_string (gray_img, lang='chi_sim', config='-psm 6')

        # print("gg.")

        print ("code:", code)

        os.makedirs (crop_dir, exist_ok=True)

        img_path = f"{crop_dir}{os.sep}{image_file}"

        cv2.imwrite (img_path, gray_img)

        code_path = f"{crop_dir}{os.sep}results.txt"

        # os.makedirs(code_path,exist_ok=True)

        with open (code_path, "a", encoding="utf-8") as f:
            f.write ("\n")
            f.write (f"pic: {img_path}\n")
            f.write (f"code: {code}\n")
            f.write ("\n")

        # cv2.imshow("kk",grey_img)

        print ("one done.")

    def get_crops(self):
        select_paths_statement = f"SELECT episode_num,img FROM {self.anime_name}"
        cursor.execute (select_paths_statement)
        results = cursor.fetchall ()

        for episode_num, img_path in results:
            print ("episode num:", episode_num)
            print ("img path:", img_path)

            crop_dir = f"{crop_animes_dir}{os.sep}{self.anime_name}{os.sep}crop_{episode_num}"

            print ("crop dir:", crop_dir)
            os.makedirs (crop_dir, exist_ok=True)
            self.image_ocr(img_path, crop_dir)




db_name="DB_Animes"
db=pymysql.connect("localhost","root","cc",db_name)
cursor=db.cursor()

def main():

    madoka_dict = dict (
        origin_upper_left_pt=(278, 78),
        upper_left_pt=(664, 648),
        width=387,
        height=120,
    )

    madoka = Anime (anime_name="Madoka",
                    anime_dict=madoka_dict
                    )

    # upper_left_pt = (458,618)
    # width = 525
    # height = 58
    # origin_upper_left_pt = (288,183)

    # 待定
    katanagatari_dict=dict(
        upper_left_pt = (458,618),
        width = 525,
        height = 58,
        origin_upper_left_pt = (288,183),
    )

    katanagatari=Anime(anime_name="katanagatari",
                       anime_dict=katanagatari_dict
                       )

    madoka.get_crops()
    katanagatari.get_crops()


if __name__ == '__main__':
    main()




# image_dir=r"D:\AllDowns\Madoka\[Madoka][01]"
#
#
# for pic in os.listdir(image_dir):
#     image_path=f"{image_dir}{os.sep}{pic}"
#     image_ocr(image_path)