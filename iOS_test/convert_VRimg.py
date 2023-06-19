from pathlib import Path
import cv2
import numpy as np
import time

import numpy as np
import cv2
import sys
import os

import cv2
import numpy as np
import os
import glob

DIM=3
dist = [-0.1, -0.1,  0, 0 ,-0.1]
mtx = [[480,0,240],
       [0,0,180],
       [0,0,1]]

# チェスボード画像から算出したカメラパラメータを設定
fx = 250
fy = 250
Cx = 250 / 2
Cy = 250 / 2
mtx = np.array([[fx, 0, Cx],[0, fy, Cy],[0, 0, 1]])

# チェスボード画像から算出した歪係数を設定
k1 = 0.4
k2 = 0.3
p1 = 0
p2 = 0
k3 = 0.3
dist = np.array([[k1, k2, p1, p2, k3]])


def undistort():
    img = cv2.imread('./catVR.jpg')
    h,w = img.shape[:2]
    print(f"h:{h},w:{w}")
    # Refining the camera matrix using parameters obtained by calibration
    # ROI:Region Of Interest(対象領域)
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    # Method 1 to undistort the image
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    cv2.imshow("undistorted", dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    undistort()