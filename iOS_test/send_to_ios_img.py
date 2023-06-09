# UDP communication for streaming :https://www.aipacommander.com/entry/2017/12/27/155711

import socket
import numpy as np
import cv2
import time

def main():
    # UDPなどのパケット？ソケット？を設定
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 送信先のIPアドレスとポート番号
    to_send_addr = ('', 8080)
    cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FPS,10)
    count = 0
    start = time.perf_counter()
    while True:
        ret, img = cap.read()
        if not ret:
            break
        # 画像処理などをここに挿入↓
        # print(cap.get(cv2.CAP_PROP_FPS))
        if count%2:
            # 画像をリサイズする
            frame = cv2.resize(img, (200,200))
            # フレームをJPEG形式にエンコード
            _, img_encode = cv2.imencode('.jpg', frame)
            # 画像を分割する
            for i in np.array_split(img_encode, 5):
                # 画像の送信
                udp.sendto(i.tobytes(), to_send_addr)
                time.sleep(0.001)
            # 画像の区切りとして__end__を送信
            udp.sendto(b'__end__', to_send_addr)
        count +=1
        now = time.perf_counter()
        if(now-start>1.0):
            start = now
            print(count)

    # リソースを解放
    cap.release()
    udp.close()



if __name__ == '__main__':
    main()