#-----------------------------------------------------------------
    # 画像を(PC / iPhone)に送る用のコード + QRコードの読み取り（ROSには上げていない)
    # bambi01-95 m058　
#-----------------------------------------------------------------

import time
import socket
import numpy as np
import cv2

# kuas@123
# 相手側
sendToIp     = '172.31.33.254'
sendToPort   = 8080
to_send_addr = (sendToIp,sendToPort)

Hsize = 400
Vsize = 400
printBool = 1

# 相手に送る　
def send():
    # UDPなどのパケット/ソケットを設定
    global to_send_addr,Hsize,Vsize
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # ERROR...indexなら、0,1,2と値を変える
    cap = cv2.VideoCapture(0)
    

    # QRコード読み取り用の関数設定
    detector = cv2.QRCodeDetector()

    # opencvによるカメラの設定
    cap.set(cv2.CAP_PROP_FPS,30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, Hsize)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,Vsize) 
    opencv_fps_count = 0
    # 手動によるカメラの設定 & 送信画像サイズと分割サイズ
    manual_fps = 1  # %2->15fps %3->10fps %4
    manual_fps_count = 0

    fSize = (Hsize,Vsize)
    # DataSplitNum = int((Hsize * Vsize) / 100) + 1
    DataSplitNum = 16
    print(f'div_fps:{30/manual_fps}, frame size:{fSize},data split number:{DataSplitNum}')

    # 処理開始
    start_sec = time.perf_counter()
    while True:
        ret, img = cap.read()
        if not ret:
            print("cannot get ret, img")
            time.sleep(1/30/manual_fps)
            continue

        # QRコード読み取り
        # data, bbox, straight_qrcode = detector.detectAndDecode(img)
        # if len(data) > 0:
        #     print("QR: ",data)
        #     n_lines = len(bbox)
        #     for i in range(n_lines):
        #         # draw all lines
        #         point1 = tuple(bbox[i][0])
        #         point2 = tuple(bbox[(i+1) % n_lines][0])
        #         cv2.polylines(frame, np.int32([bbox]), True, (255, 0, 0), 2)

        # 画像を送る処理
        if opencv_fps_count % manual_fps == 0: 
            frame = cv2.resize(img, fSize)
            _, img_encode = cv2.imencode('.jpg', frame)
            # 画像の分割送信　
            for i in np.array_split(img_encode,DataSplitNum):
                udp.sendto(i.tobytes(), to_send_addr)
                time.sleep(0.0008)# READ: 0.0008以上の間隔を空けないとswiftは受け取れない
            udp.sendto(b'__end__', to_send_addr)
            manual_fps_count+=1

        opencv_fps_count += 1
        if(printBool == 1):
            now_sec = time.perf_counter()
            if(now_sec-start_sec>1.0):
                print(f'cv2. fps:{cap.get(cv2.CAP_PROP_FPS)}\nreal fps:{opencv_fps_count}\nsend fps:{manual_fps_count}\n')
                if(opencv_fps_count>3600):
                    opencv_fps_count = 0
                    manual_fps_count = 0
                start_sec = now_sec
    # リソースを解放
    cap.release()
    udp.close()

#-----------------------------------------------------------------
if __name__ == '__main__':
    send()
    print("end of the code\n")