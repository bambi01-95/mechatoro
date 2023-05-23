# UDP communication for streaming :https://www.aipacommander.com/entry/2017/12/27/155711

import socket
import numpy as np
import cv2
import time
from multiprocessing import Process

def send():
    # UDPなどのパケット？ソケット？を設定
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 送信先のIPアドレスとポート番号
    to_send_addr = ('192.168.0.31', 8080)
    cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FPS,10)
    fps15 = 0
    start = time.perf_counter()
    while True:
        ret, img = cap.read()
        if not ret:
            break
        # 画像処理などをここに挿入↓
        # print(cap.get(cv2.CAP_PROP_FPS))
        if fps15%2:
            # 画像をリサイズする
            frame = cv2.resize(img, (640,480))
            # フレームをJPEG形式にエンコード
            _, img_encode = cv2.imencode('.jpg', frame)
            # 画像を分割する
            for i in np.array_split(img_encode, 20):
                # 画像の送信
                udp.sendto(i.tobytes(), to_send_addr)
            # 画像の区切りとして__end__を送信
            udp.sendto(b'__end__', to_send_addr)
            # pc 側で知りたいメッセージを送信（QRコードとか）
            # message_byte = message.encode()
            # udp.sendto(message_byte,to_send_addr)
            if fps15>30*60*5:
                fps15 = 0
        fps15+=1
    # リソースを解放
    cap.release()
    udp.close()

def recive():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(('192.168.0.31', 8008))
    buff = 1024 * 64
    p_count = 0
    while True:
        p_count+=1
        jpg_str, addr = udp.recvfrom(buff)
        message = jpg_str.decode()
        if p_count>30:
            print(message)
            p_count = 0

if __name__ == '__main__':
    data_send = Process(target=send)
    data_reci = Process(target=recive)

    data_send.start()
    data_reci.start()

    data_send.join()
    data_reci.join()
    print("end_of_THE_code")

