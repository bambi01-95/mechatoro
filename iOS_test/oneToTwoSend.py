import sys
import os

import cv2
import numpy as np
import os
import glob
import socket
import time
'''
    2023/07/01 bambi01-95 m058
    oneToTwoSend.py
    一つのカメラを左右に分けて出力し、擬似的にVR作成

    ->大画面スクリーンで、動画を見れいるだけ、って感じ、見た目だけ
'''
# simulator : https://kamino410.github.io/cv-snippets/camera_distortion_simulator/
# open cv site : http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_calib3d/py_calibration/py_calibration.html
# code reference : https://miyashinblog.com/opencv-undistort/ 

def undistort():
    cap = cv2.VideoCapture(0)
    ret, img = cap.read()
    if not ret:
        print("no img get\n")
    h,w = img.shape[:2]
    print(h,"hw",w)

    dist = [-0.1, -0.1,  0, 0 ,-0.1]
    mtx = [[480,0,240],
        [0,0,180],
        [0,0,1]]

    # チェスボード画像から算出したカメラパラメータを設定
    fx = h
    fy = h
    Cx = h / 2
    Cy = h / 2
    mtx = np.array([[fx, 0, Cx],[0, fy, Cy],[0, 0, 1]])

    # チェスボード画像から算出した歪係数を設定
    k1 = 0.4
    k2 = 0.3
    p1 = 0
    p2 = 0
    k3 = 0.3
    dist = np.array([[k1, k2, p1, p2, k3]])
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (h,h), 1, (h,h))

        # UDPなどのパケット？ソケット？を設定
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 送信先のIPアドレスとポート番号
    to_send_addr = ('192.168.0.23', 8080)
    cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FPS,10)
    count = 0
    sec30 = 0
    min = 0
    fps = 0
    start = time.perf_counter()
    diff = 120
    while True:
        ret, img = cap.read()
        if not ret:
            break
        h,w = img.shape[:2]

        imgL= img[:h,:h]
        imgR= img[:h,diff:h+diff]

        distL = cv2.undistort(imgL, mtx, dist, None, newcameramtx)
        distR = cv2.undistort(imgR, mtx, dist, None, newcameramtx)

        distframe = cv2.hconcat([distL,distR])
        # cv2.imshow("vr",distframe)

        if count%1==0:
            # 画像をリサイズする
            frame = cv2.resize(distframe, (400,200))
            cv2.imshow("vr",frame)
            # フレームをJPEG形式にエンコード
            _, img_encode = cv2.imencode('.jpg', frame)

            #画像を分割
            for i in np.array_split(img_encode, 8):
                # 画像の送信
                udp.sendto(i.tobytes(), to_send_addr)
                time.sleep(0.002)#0.005はだめだった0.005/0.14くらいを超えたらノイズが現れにくくなった
            # 画像の区切りとして__end__を送信
            time.sleep(0.002)
            udp.sendto(b'__end__', to_send_addr)
            fps +=1

        count +=1
        sec30 +=1
        now = time.perf_counter()
        if(now-start>1.0):
            start = now
            if sec30>1800:
                sec30 = 0
                min +=1
            print(min,":",sec30,":",fps)
            fps = 0

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    cap.release()
    udp.close()

if __name__ == '__main__':
    undistort()