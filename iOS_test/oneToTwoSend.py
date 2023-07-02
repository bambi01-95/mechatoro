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

# contrast: https://tat-pytone.hatenablog.com/entry/2022/01/26/212650
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
    k1 = 5  #5
    k2 = 5#0.3
    p1 = 0
    p2 = 0
    k3 = 5#0.3
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
    mid_w = int(w/2)
    mid_h = int(h/2)

    # ガンマ変換用の数値準備 1
    gamma     = 1.7                               # γ値を指定
    img2gamma = np.zeros((256,1),dtype=np.uint8)  # ガンマ変換初期値

    # 公式適用
    for i in range(256):
        img2gamma[i][0] = 255 * (float(i)/255) ** (1.0 /gamma)


    # 変換用ルックアップテーブルの生成
    gamma = 1.5
    look_up_table = np.zeros((256, 1) ,dtype=np.uint8)
    for i in range(256):
        look_up_table[i][0] = (i/255)**(1.0/gamma)*255
    print(1/30/8)
    while True:
        ret, img = cap.read()
        if not ret:
            break
        h,w = img.shape[:2]
        text = "speed 123 m/s"

        img = cv2.LUT(img,img2gamma) #1
        # 色空間をBGR->HSVに変換
        # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)         

        # # チャンネルごとに分割
        # hh, ss, vv = cv2.split(hsv)  

        # # 明度(V)に対してルックアップテーブル適用
        # v_lut = cv2.LUT(vv, look_up_table)       
        
        # # 彩度(S)に対してルックアップテーブル適用
        # s_lut = cv2.LUT(ss, look_up_table)  
        
        # #  H,変換後S,変換後Vをマージ
        # merge = cv2.merge([hh, s_lut, v_lut])  
        
        # # HSV->BGR変換
        # img = cv2.cvtColor(merge, cv2.COLOR_HSV2BGR) 



        img = cv2.putText(img,text,(mid_w-mid_h + 302 ,mid_h),cv2.FONT_HERSHEY_TRIPLEX,0.5,(30,30,30),1,cv2.LINE_AA)
        img = cv2.putText(img,text,(mid_w-mid_h + 300 ,mid_h),cv2.FONT_HERSHEY_TRIPLEX,0.5,(255,255,255),1,cv2.LINE_AA)
        imgL= img[:h, mid_w-mid_h -75: mid_w+mid_h -75]
        imgR= img[:h, mid_w-mid_h +75: mid_w+mid_h +75]

        distL = cv2.undistort(imgL, mtx, dist, None, newcameramtx)
        distR = cv2.undistort(imgR, mtx, dist, None, newcameramtx)

        distframe = cv2.hconcat([distL,distR])
        # cv2.imshow("vr",distframe)


        # 画像をリサイズする
        frame = cv2.resize(distframe, (800,400))# これ以上はあんま変わらない。
        cv2.imshow("vr",frame)
        # フレームをJPEG形式にエンコード
        _, img_encode = cv2.imencode('.jpg', frame)

        #画像を分割
        for i in np.array_split(img_encode, 32):
            # 画像の送信
            udp.sendto(i.tobytes(), to_send_addr)
            time.sleep(0.0015)#0.005はだめだった0.005/0.14くらいを超えたらノイズが現れにくくなった
        # 画像の区切りとして__end__を送信
        time.sleep(0.0015)
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