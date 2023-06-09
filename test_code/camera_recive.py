import cv2
import socket
import numpy as np
import time
def recive(udp):
    buff = 1024 * 64
    while True:
        recive_data = bytes()
        # 写真データの受け取り
        
        while True:
            # 送られてくるデータが大きいので一度に受け取るデータ量を大きく設定
            jpg_str, addr = udp.recvfrom(buff)
            is_len = len(jpg_str) == 7
            is_end = jpg_str == b'__end__'
            if is_len and is_end: 
                break
            recive_data += jpg_str
        # 受け取ったデータがなかった時、whileをやり直す
        if len(recive_data) == 0: continue

        # メッセージを受け取る
        # jpg_str, addr = udp.recvfrom(buff)
        # message = jpg_str.decode()

        # string型からnumpyを用いuint8に戻す
        narray = np.frombuffer(recive_data, dtype='uint8')

        # uint8のデータを画像データに戻す
        img = cv2.imdecode(narray, 1)

        yield img
    


# フレーム生成・返却する処理
def main():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(('00.00.00.00',8080))
    start = time.perf_counter()
    count = 0.000
    # 画像を取り続ける
    for img in recive(udp):
        h,w = img.shape[:2]
        if (h>200)&(w>200):
            cv2.imshow("FROM_RSPI_CAMERA",img)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        # count +=1
        now = time.perf_counter()
        start = now
        print(now-start)
        # if(now-start>1.0):
        #     start = now
        #     print(count)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()