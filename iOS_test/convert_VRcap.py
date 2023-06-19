import sys
import os

import cv2
import numpy as np
import os
import glob

# simulator : https://kamino410.github.io/cv-snippets/camera_distortion_simulator/
# open cv site : http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_calib3d/py_calibration/py_calibration.html
# code reference : https://miyashinblog.com/opencv-undistort/ 

def undistort():
    cap = cv2.VideoCapture(0)
    ret, img = cap.read()
    if not ret:
        print("no img get\n")
    h,w = img.shape[:2]
    # チェスボード画像から算出したカメラパラメータを設定
    fx = w
    fy = h
    Cx = w / 2
    Cy = h / 2
    mtx = np.array([[fx, 0, Cx],[0, fy, Cy],[0, 0, 1]])

    # チェスボード画像から算出した歪係数を設定
    # do simulator or ...
    k1 = 0.3
    k2 = 0.1
    p1 = 0
    p2 = 0
    k3 = 0.1
    dist = np.array([[k1, k2, p1, p2, k3]])

    while True:
        ret, img = cap.read()
        if not ret:
            break
        h,w = img.shape[:2]
        # print(f"h:{h},w:{w}")
        # Refining the camera matrix using parameters obtained by calibration
        # ROI:Region Of Interest(対象領域)
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
        # Method 1 to undistort the image
        dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
        cv2.imshow("undistorted", dst)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    cap.release()

if __name__ == '__main__':
    undistort()