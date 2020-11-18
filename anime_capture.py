import cv2
import os

# 使用cv2进行逐帧截图
# https://blog.csdn.net/qq_41192383/article/details/86559337

video_dir=input("Dir name:")

alldown_dir=r"D:\AllDowns"

if os.sep in video_dir:
    pass
else:
    video_dir=alldown_dir+os.sep+video_dir

print("Video dir: ",video_dir)

def main():
    for video in os.listdir(video_dir):
        video_path=f"{video_dir}{os.sep}{video}"
        if os.path.isfile(video_path):
            video_name=video.split(".")[0]
            video_pic_dir=f"{video_dir}{os.sep}{video_name}"
            os.makedirs(video_pic_dir,exist_ok=True)

            vc=cv2.VideoCapture(video_path)
            c=0

            rval=vc.isOpened()

            frame_rate=48

            while rval:  # 循环读取视频帧
                p = c//frame_rate+1
                c = c + 1
                rval, frame = vc.read ()
                pic_path = f"{video_pic_dir}{os.sep}{video_name}_{str(p)}.jpg"
                if rval:
                    if c%frame_rate==1:
                        cv2.imwrite (pic_path, frame)  # 存储为图像,保存名为 文件夹名_数字（第几个文件）.jpg
                        cv2.waitKey (1)
                    else:
                        continue
                else:
                    break

            vc.release ()
            print ('one done.')

if __name__ == '__main__':
    main()