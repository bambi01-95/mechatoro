import sys
import os

import cv2
import numpy as np
import os
import glob
'''
    2023/07/01 bambi01-95 m058
    1つのカメラでVR動画を作成できるかを実験する
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
    while True:
        ret, img = cap.read()
        if not ret:
            break
        h,w = img.shape[:2]
        # img[height,width]
        imgL= img[:h,:h]
        imgR= img[:h,150:h+150]
        # cv2.imshow("left", imgL)
        # cv2.imshow("right", imgR)

        # frame = cv2.hconcat([imgL,imgR])
        # cv2.imshow("vr",frame)
        distL = cv2.undistort(imgL, mtx, dist, None, newcameramtx)
        distR = cv2.undistort(imgR, mtx, dist, None, newcameramtx)
        distframe = cv2.hconcat([distL,distR])
        cv2.imshow("vr",distframe)


        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    cap.release()

if __name__ == '__main__':
    undistort()