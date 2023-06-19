import time
import socket
import numpy as np
import cv2

# kuas@123
# 相手側
#   mls:
# katu2:
#    my:
send_ip     = '192.168.0.31'
send_port   = 8080
to_send_addr = (send_ip,send_port)

#-----------------------------------------------------------------
    # 画像を(PC / iPhone)に送る用のコード + QRコードの読み取り（ROSには上げていない)
#-----------------------------------------------------------------
# 相手に送る　
def send():
    global to_send_addr
    # UDPなどのパケット/ソケットを設定
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #カメラ起動　(ERROR...indexなら、0,1,2と値を変える)
    cap = cv2.VideoCapture(0)

    # QRコード読み取り用の関数設定
    detector = cv2.QRCodeDetector()
    # fps設定
    cap.set(cv2.CAP_PROP_FPS,30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 400) # カメラ画像の横幅を1280に設定
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,400) # カメラ画像の縦幅を720に設定
    div_fps = 1 # %2->15fps %3->10fps %4
    real_fps = 0
    send_fps = 0
    # 送信画像サイズと分割サイズ
    hw = 400
    fSize = (hw,hw)
    splitNum = (hw/100) ** 2
    print(f'div_fps:{30/div_fps}, frame size:{fSize},split number:{splitNum}')

    start = time.perf_counter()
    while True:
        ret, img = cap.read()
        if not ret:
            print("cannot get ret, img")
            time.sleep(1/30/div_fps)
            continue
        # QRコード読み取り
        data, bbox, straight_qrcode = detector.detectAndDecode(img)
        if len(data) > 0:
            print("QR: ",data)

        # 画像を送る処理
        if real_fps%div_fps == 0: 
            # 画像をリサイズする
            frame = cv2.resize(img, fSize)
            # フレームをJPEG形式にエンコード
            _, img_encode = cv2.imencode('.jpg', frame)
            # 画像を分割する
            for i in np.array_split(img_encode,splitNum):
                # 画像の送信
                udp.sendto(i.tobytes(), to_send_addr)
                time.sleep(0.0008)# 0.0008以上の値にすること
            # 画像の区切りとして__end__を送信
            udp.sendto(b'__end__', to_send_addr)

    # FPS テスト
            send_fps+=1
        real_fps += 1
        now = time.perf_counter()
        if(now-start>1.0):
            print(f'cv2. fps:{cap.get(cv2.CAP_PROP_FPS)}\nreal fps:{real_fps}\nsend fps:{send_fps}\n')
            if(real_fps>3600):
                real_fps = 0
                send_fps = 0
            start = now
    # リソースを解放
    cap.release()
    udp.close()

#-----------------------------------------------------------------
if __name__ == '__main__':
    send()
    print("end of the code\n")