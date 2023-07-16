# -*- coding: utf-8 -*-
# WebSocketServer.py
# sudo pip3 install websocket-server
from websocket_server import WebsocketServer
import threading
import time
import rospy
import time
import numpy as np
from std_msgs.msg import Int16MultiArray
import RPi.GPIO as GPIO

# raspi 
HOST = "172.31.33.254" # IPアドレスopen
PORT = 5000 # ポートを指定


MAX_MOTOR_SPD = 100
MIN_MOTOR_SPD = 0

l_set_spd = 0
r_set_spd = 0

class WsServer():
    def __init__(self, host, port):
        self.server = WebsocketServer(host, port)
        self.rcvData = []
        self.user = 0

    def newClient(self, client, server):
        print("Connected client : ", client['address'])
        self.user += 1
        self.server.send_message(client, "OK! Connected")

    def clientLeft(self, client, server):
        self.user =- 1
        print("Disconnected : ", client['address'])

    def messageReceived(self, client, server, message):
        print(self.user)
        self.server.send_message(client, "L" + str(l_set_spd) + "R" + str(r_set_spd) )
        self.rcvData.append(message)

    def runServer(self):
        self.server.set_fn_new_client(self.newClient)    # Client接続時
        self.server.set_fn_client_left(self.clientLeft)    # Client切断時
        self.server.set_fn_message_received(self.messageReceived)     # Clientからの受信時
        self.server.run_forever()

wsServer = WsServer(HOST, PORT)

def wsStart():
    wsServer.runServer()

"""
    for servo motor
""" 
# サーボモータ1の制御に使用するGPIOピン番号
servo1_pin = 18
 
# サーボモータ2の制御に使用するGPIOピン番号
servo2_pin = 19
 
# サーボモータの最小角度と最大角度（調整が必要な場合は適宜変更してください）
min_angle = 40
max_angle = 180
 
# サーボモータの初期角度
initial_angle1 = 110
initial_angle2 = 110

# サーボモータの増減角度
step_angle = 0.5
 
# 初期化
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)
 
# PWMインスタンスを作成
pwm1 = GPIO.PWM(servo1_pin, 50)  # サーボモータ1のPWM周波数を50Hzに設定
pwm2 = GPIO.PWM(servo2_pin, 50)  # サーボモータ2のPWM周波数を50Hzに設定
pwm1.start(0)  # PWM出力を開始
pwm2.start(0)  # PWM出力を開始
 
# サーボモータ1を指定した角度に移動する関数
def move_servo1(angle):
    angle = max(min(angle, max_angle), min_angle)  # 角度を上限と下限の範囲内に制限
    duty_cycle = (angle / 18) + 2  # デューティ比を計算
    pwm1.ChangeDutyCycle(duty_cycle)
 
# サーボモータ2を指定した角度に移動する関数
def move_servo2(angle):
    angle = max(min(angle, max_angle), min_angle)  # 角度を上限と下限の範囲内に制限
    duty_cycle = (angle / 18) + 2  # デューティ比を計算
    pwm2.ChangeDutyCycle(duty_cycle)


"""
    for motor driver
"""
def set_motor_value(l_vel,r_vel):
    msg = Int16MultiArray()
    msg.data.append(l_vel)
    msg.data.append(r_vel)
    return msg

def limit_vel(vel):
    vel = vel if abs(vel) < MAX_MOTOR_SPD else np.sign(vel) * MAX_MOTOR_SPD
    return vel


def publish_motor_spd(pub, l_spd,r_spd):
    pub.publish( set_motor_value(l_spd,r_spd) )

def key_to_spd(data):
    global l_set_spd,r_set_spd
    wad,s,i,j = data.split(",")

    # chagnge l and r _set_spd
    if(i=="1"):
        l_set_spd += 10
        r_set_spd += 10
        l_set_spd = limit_vel(l_set_spd)
        r_set_spd = limit_vel(r_set_spd)
        
    if(j=="1"):
        l_set_spd -= 10
        r_set_spd -= 10
        l_set_spd = limit_vel(l_set_spd)
        r_set_spd = limit_vel(r_set_spd)

    if(s=="1"):
        l_set_spd *= -1
        r_set_spd *= -1
        wad = int(wad,2)
        wad = '{0:03b}'.format(wad ^ 0b011)

    # set l and r _out_spd
    if(wad=="111")|(wad=="100"):
        l_out_spd = l_set_spd
        r_out_spd = r_set_spd
    elif(wad=="110"):
        l_out_spd = l_set_spd
        r_out_spd = int(r_set_spd / 2)
    elif(wad=="010"):
        l_out_spd = l_set_spd
        r_out_spd = 0
    elif(wad=="101"):
        l_out_spd = int(l_set_spd / 2)
        r_out_spd = r_set_spd 
    elif(wad=="001"):
        l_out_spd = 0
        r_out_spd = r_set_spd
    else:
        l_out_spd = 0
        r_out_spd = 0

    if command == 'a':  # aキー
            initial_angle1 = min(initial_angle1 + step_angle, max_angle)
            move_servo1(initial_angle1)
    elif command == 'd':  # dキー
            initial_angle1 = max(initial_angle1 - step_angle, min_angle)
            move_servo1(initial_angle1)
            
    elif command == 'j':  # jキー
            initial_angle2 = min(initial_angle2 + step_angle, max_angle)
            move_servo2(initial_angle2)
    elif command == 'l':  # lキー
            initial_angle2 = max(initial_angle2 - step_angle, min_angle)
            move_servo2(initial_angle2)

    print("Receive data = ", wad,"s",s,"j",j,"i",i)
    print("Lset",l_set_spd,"Rset",r_set_spd)
    print("Lout",l_out_spd,"Rout",r_out_spd)

    return l_out_spd,r_out_spd

# result = [(ord(a) ^ ord(b)) for a, b in zip(string1, string2)]

def main():
    rospy.init_node("bringup_controller")
    motor_vel_pub = rospy.Publisher("/motor_vel", Int16MultiArray, queue_size=2)

    # Start receiving data from client
    recvThread = threading.Thread(target=wsStart)
    recvThread.daemon = True    # 修了時にハングアップしない
    recvThread.start()
    print("Threading Start")

    try:
        while True:
            if len(wsServer.rcvData):    # Receive data from Client PC
                data = wsServer.rcvData[0]

                l_out_spd,r_out_spd = key_to_spd(data)

                publish_motor_spd(motor_vel_pub, l_out_spd, r_out_spd)

                wsServer.rcvData.pop(0)    # Pop Top data
            time.sleep(0.005)

    except KeyboardInterrupt:
        print("Keyboard Interrupt")

    print("Loop terminated")


if __name__ == "__main__":
    main()