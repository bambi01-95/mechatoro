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






def undistort():
    img = cv2.imread('./AG.png')
    h,w = img.shape[:2]
    # チェスボード画像から算出したカメラパラメータを設定
    fx = w
    fy = h
    Cx = w / 2
    Cy = h / 2
    mtx = np.array([[fx, 0, Cx],[0, fy, Cy],[0, 0, 1]])

    # チェスボード画像から算出した歪係数を設定
    k1 = 0.4
    k2 = 0.3
    p1 = 0
    p2 = 0
    k3 = 0.3
    dist = np.array([[k1, k2, p1, p2, k3]])
    print(f"h:{h},w:{w}")
    # Refining the camera matrix using parameters obtained by calibration
    # ROI:Region Of Interest(対象領域)
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
    # Method 1 to undistort the image
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    cv2.imshow("undistorted", dst)
    cv2.imwrite("AG_.jpg",dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    undistort()