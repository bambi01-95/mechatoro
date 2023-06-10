# 2023/06/09
# 2023/06/13のモータテストに使用できる
# nucleo <- raspi <-> PC の通信
    # while -> with に書き換えた方が良い
    # 送る用と受け取る用の二つのファイルにしても良い

import time
from multiprocessing import Process

import socket
import numpy as np
import cv2

import rospy
import sys,tty
from std_msgs.msg import Float32MultiArray

# kuas@123
# 相手側
send_ip     = '172.20.10.6'
send_port   = 8008
to_send_addr = (send_ip,send_port)

# this pc/RasPi ip & port
recive_ip   = '172.20.10.7'
recive_port = 8080
to_recive_addr = (recive_ip,recive_port)

#-----------------------------------------------------------------
    # 画像を送る用のコード
#-----------------------------------------------------------------
# 相手に送る　
def send():
    global to_send_addr
    # UDPなどのパケット？ソケット？を設定
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 送信先のIPアドレスとポート番号
    cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FPS,10)
    fps15 = 0
    start = time.perf_counter()
    while True:
        ret, img = cap.read()
        if not ret:
            print("cannot get ret, img")
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

#-----------------------------------------------------------------
    # コントローラからデータを受け取り、ROSにデータを上げるコード
#-----------------------------------------------------------------
MAX_MOTOR_SPD = 50.0
MIN_MOTOR_SPD = 10.0

# スピード制限
def limit_vel(vel):
    vel = vel if abs(vel) < MAX_MOTOR_SPD else np.sign(vel) * MAX_MOTOR_SPD
    return vel

# ROSのデータ更新
def publish_motor_spd(pub, spd):                            #----
    pub.publish( set_motor_value(spd) )
def set_motor_value(motor_vel):                         #---
    msg = Float32MultiArray()
    msg.data.append(motor_vel)
    return msg


# 自分が受け取る
def recive():
    global to_recive_addr
    # setting udp
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(to_recive_addr)

    # setting rospy
    rospy.init_node("bringup_controller")                     #----
    # ROS 値の初期化                                                 #----
    l_motor_vel_pub = rospy.Publisher("/set_setpoint_motor_l", Float32MultiArray, queue_size=10)
    r_motor_vel_pub = rospy.Publisher("/set_setpoint_motor_r", Float32MultiArray, queue_size=10)

    spd = 4
    spd_step = 2  
    # 受け取れる最大のデータ量
    buff = 1024 * 64
    p_count = 0
    while not rospy.is_shutdown():
        # データの受け取り
        str, addr = udp.recvfrom(buff)
        message = str.decode()
        #00,00,00,00
        #01234567890
        l_motor = float(message[0:2])
        r_motor = float(message[3:5])
        sabo    = float(message[6:8])
        # rosにデータを上げる（更新）
        publish_motor_spd(l_motor_vel_pub, l_motor)
        publish_motor_spd(r_motor_vel_pub, r_motor) 
        


    udp.close()





#-----------------------------------------------------------------
if __name__ == '__main__':
    data_send = Process(target=send)
    data_reci = Process(target=recive)

    data_send.start()
    data_reci.start()

    data_send.join()
    data_reci.join()
    print("end_of_THE_code")