from django.shortcuts import render
from django.http import HttpResponse
# Create your views here

import cv2
from django.http import StreamingHttpResponse
from django.views import View

import time
import numpy as np

import socket
def homeView(request):
    return render(request, 'app/home.html')

"""
    for normarl view
"""
# スマホ用のページストリーミング
class IndexView(View):
    def get(self, request):
        return render(request, 'app/index.html', {})
    

    
# 前カメラの映像出力
def video_feed_view_f():
    return lambda _: StreamingHttpResponse(generate_frame_forward(), content_type='multipart/x-mixed-replace; boundary=frame')

def recive(udp,number):
    global getimg
    if(number == 0):
        buff = 1024 * 64
        while True:
            recive_data = bytes()
            count = 0
            # 画像データの受け取り
            while True:
                jpg_str, addr = udp.recvfrom(buff)
                is_len = len(jpg_str) == 7
                is_end = jpg_str == b'__end__' 
                if is_len and is_end: #　*1
                    break
                count += 1
                recive_data += jpg_str
            if len(recive_data) == 0: continue

            # string型からnumpyを用いuint8に戻す
            narray = np.frombuffer(recive_data, dtype='uint8')

            # uint8のデータを画像データに戻す
            getimg = cv2.imdecode(narray, 1)
            yield getimg,1
    else:
        while True:
            yield getimg,0

number = 0
udp_recive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_recive.bind(('172.31.33.254',8080))

# 前かめらの映像取得
def generate_frame_forward():
    global number,udp_recive,count
    DataSplitNum = 36
    id = number
    number += 1
    check = count
    for img,i in recive(udp_recive,id):
        try:         
            # フレーム画像バイナリに変換
            ret, jpeg = cv2.imencode('.jpg', img)
            byte_frame = jpeg.tobytes()
            # フレーム画像のバイナリデータをユーザーに送付する
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + byte_frame + b'\r\n\r\n')
        except cv2.error:
            print("img empty\n")

        

 
# web app用のページストリーミング
class webView(View):
    def get(self, request):
        return render(request, 'app/indexback.html', {})

# 後ろカメラの映像出力
def video_feed_view_b():
    return lambda _: StreamingHttpResponse(generate_frame_back(), content_type='multipart/x-mixed-replace; boundary=frame')

def capread(id):
    global capimg
    if(id==0):
        capture = cv2.VideoCapture(1)  # USBカメラから
        if not capture.isOpened():
            print("Capture is not opened.")
        while True:
            ret, frame = capture.read()
            capimg = frame
            yield capimg
    else:
        while True:
            time.sleep(0.03)
            yield capimg
    print("disconnect")
    capture.release()



backnumber = 0

# 後ろカメラの映像取得
def generate_frame_back():
    global backnumber
    id = backnumber
    backnumber += 1
    for frame in capread(id):
            # フレーム画像バイナリに変換
        ret, jpeg = cv2.imencode('.jpg', frame)
        byte_frame = jpeg.tobytes()
        # フレーム画像のバイナリデータをユーザーに送付する
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + byte_frame + b'\r\n\r\n')
    



"""
    for VR
"""
# ストリーミング画像・映像を表示するview
class VRView(View):
    def get(self, request):
        return render(request, 'app/vr.html', {})

# ストリーミング画像を定期的に返却するview
def video_feed_vr():
    return lambda _: StreamingHttpResponse(vr_frame(), content_type='multipart/x-mixed-replace; boundary=frame')

# フレーム生成・返却する処理
def vr_frame():
# カメラの初期設定など
    capture = cv2.VideoCapture(0)  # USBカメラから
    count = 0
    if not capture.isOpened():
        print("Capture is not opened.")
    ret, frame = capture.read()
    h,w = frame.shape[:2]
    print("h=",h,", w=",w)    
    count = 0
    mid_w = int(w/2)
    mid_h = int(h/2)

# VR用に映像を歪ませるために必要な変数を設定
    # カメラパラメータを設定
    fx = h
    fy = h
    Cx = h / 2
    Cy = h / 2
    mtx = np.array([[fx, 0, Cx],[0, fy, Cy],[0, 0, 1]])

    # 歪係数を設定
    k1 = 5  #5
    k2 = 5#0.3
    p1 = 0
    p2 = 0
    k3 = 5#0.3
    dist = np.array([[k1, k2, p1, p2, k3]])
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (h,h), 1, (h,h))


# LOGのカメラだと映像が暗いので、少し明るくする
    # ガンマ変換用の数値準備 1
    gamma     = 1.7                               # γ値を指定
    img2gamma = np.zeros((256,1),dtype=np.uint8)  # ガンマ変換初期値

    # 公式適用
    for i in range(256):
        img2gamma[i][0] = 255 * (float(i)/255) ** (1.0 /gamma)

    global backnumber
    id = backnumber
    backnumber += 1
    for img in capread(id):
        count += 1
        # カメラからフレーム画像を取得

        text = "speed 123 m/s"
    # 映像を明るく
        img = cv2.LUT(img,img2gamma) 
    # 映像にテキストを入力（速度など）
        img = cv2.putText(img,text,(mid_w-mid_h + 302 ,mid_h),cv2.FONT_HERSHEY_TRIPLEX,0.5,(30,30,30),1,cv2.LINE_AA)
        img = cv2.putText(img,text,(mid_w-mid_h + 300 ,mid_h),cv2.FONT_HERSHEY_TRIPLEX,0.5,(255,255,255),1,cv2.LINE_AA)
        
    # 左と右の映像に分ける
        imgL= img[:h, mid_w-mid_h -75: mid_w+mid_h -75]
        imgR= img[:h, mid_w-mid_h +75: mid_w+mid_h +75]
        
    #　画像を歪ませる
        distL = cv2.undistort(imgL, mtx, dist, None, newcameramtx)
        distR = cv2.undistort(imgR, mtx, dist, None, newcameramtx)
        
    # 画像の結合
        distframe = cv2.hconcat([distL,distR])
        
    # 画像をリサイズする
        frame = cv2.resize(distframe, (800,400))

        if(count % 1 == 0):
        # フレーム画像バイナリに変換
            ret, jpeg = cv2.imencode('.jpg', frame)
            byte_frame = jpeg.tobytes()
        # フレーム画像のバイナリデータをユーザーに送付する
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + byte_frame + b'\r\n\r\n')
    capture.release()