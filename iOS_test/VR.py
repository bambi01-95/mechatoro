# UDP communication for streaming :https://www.aipacommander.com/entry/2017/12/27/155711

# UDP communication for streaming :https://www.aipacommander.com/entry/2017/12/27/155711

import socket
import numpy as np
import cv2
import time

def main():
    # UDPなどのパケット？ソケット？を設定
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 送信先のIPアドレスとポート番号
    to_send_addr = ('172.20.10.8', 8080)
    cap1 = cv2.VideoCapture(0)
    cap2 = cv2.VideoCapture(1)
    # cap.set(cv2.CAP_PROP_FPS,10)
    count = 0
    sec30 = 0
    min = 0
    fps = 0
    start = time.perf_counter()
    while True:
        ret1, img1 = cap1.read()
        ret2, img2 = cap2.read()
        if not ret1:
            break
        if not ret2:
            break
        # 画像処理などをここに挿入↓
        # print(cap.get(cv2.CAP_PROP_FPS))
        if count%2==0:
            # 画像をリサイズする
            img1 = cv2.resize(img1, (300,300))
            img2 = cv2.resize(img2, (300,300))

            vrimg = cv2.hconcat([img1, img2])
            vr

            # フレームをJPEG形式にエンコード
            _, img_encode = cv2.imencode('.jpg', vrimg)

            # 画像を分割しない
            # udp.sendto(img_encode, to_send_addr)

            #画像を分割
            for i in np.array_split(img_encode, 18):
                # 画像の送信
                udp.sendto(i.tobytes(), to_send_addr)
                time.sleep(0.001)#0.005はだめだった0.005/0.14くらいを超えたらノイズが現れにくくなった
            # 画像の区切りとして__end__を送信
            udp.sendto(b'__end__', to_send_addr)
            time.sleep(0.001)
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
        cv2.imshow("VR IMAGE",vrimg)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    # リソースを解放
    cap1.release()
    cap2.release()
    udp.close()





if __name__ == '__main__':
    main()