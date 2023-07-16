# -*- coding: utf-8 -*-
# WebSocketServer.py
# sudo pip3 install websocket-server
from websocket_server import WebsocketServer
import threading
import time
""" ros lib """
# import rospy
# import time
# import numpy as np
# from std_msgs.msg import Int16MultiArray
# import socket
""" servo lib"""
# import RPi.GPIO as GPIO
# import sys
# import tty
# import termios
 

""" web socket init """
# raspi 
HOST = "127.0.0.1" # IPアドレスopen
PORT = 5000 # ポートを指定
""" servo motor init """
# # サーボモータ1の制御に使用するGPIOピン番号
# servo1_pin = 18
 
# # サーボモータ2の制御に使用するGPIOピン番号
# servo2_pin = 19
 
# # サーボモータの最小角度と最大角度（調整が必要な場合は適宜変更してください）
# min_angle = 40
# max_angle = 180
 
# # サーボモータの初期角度
# initial_angle1 = 110
# initial_angle2 = 110

# # サーボモータの増減角度
# step_angle = 0.5
 
# # 初期化
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(servo1_pin, GPIO.OUT)
# GPIO.setup(servo2_pin, GPIO.OUT)
 
# # PWMインスタンスを作成
# pwm1 = GPIO.PWM(servo1_pin, 50)  # サーボモータ1のPWM周波数を50Hzに設定
# pwm2 = GPIO.PWM(servo2_pin, 50)  # サーボモータ2のPWM周波数を50Hzに設定
# pwm1.start(0)  # PWM出力を開始
# pwm2.start(0)  # PWM出力を開始

""" motor drive init """
setting_spd = 0
l_out_spd = 0
r_out_spd = 0
MODE = False

"""
web socket func/class
"""
class WsServer():
    def __init__(self, host, port):
        self.server = WebsocketServer(host, port)
        self.rcvData = []

    def newClient(self, client, server):
        print("Connected client : ", client['address'])
        self.server.send_message(client, "OK! Connected")

    def clientLeft(self, client, server):
        print("Disconnected : ", client['address'])

    def messageReceived(self, client, server, message):
        c_type = "close"
        if(MODE==True):
            c_type = "open"
        self.server.send_message(client, "Setting speed: " + str(setting_spd) + ",L spd" + str(l_out_spd) + "R spd" + str(r_out_spd) +"," + c_type)
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
servo motor func/class
"""
 
# # サーボモータ1を指定した角度に移動する関数
# def move_servo1(angle):
#     angle = max(min(angle, max_angle), min_angle)  # 角度を上限と下限の範囲内に制限
#     duty_cycle = (angle / 18) + 2  # デューティ比を計算
#     pwm1.ChangeDutyCycle(duty_cycle)
 
# # サーボモータ2を指定した角度に移動する関数
# def move_servo2(angle):
#     angle = max(min(angle, max_angle), min_angle)  # 角度を上限と下限の範囲内に制限
#     duty_cycle = (angle / 18) + 2  # デューティ比を計算
#     pwm2.ChangeDutyCycle(duty_cycle)

def move_arm(arm1,arm2):
    print(arm1,arm2)
    if (arm1=="10"):  # fキー
        print("f")
    #     initial_angle1 = min(initial_angle1 + step_angle, max_angle)
    #     move_servo1(initial_angle1)
    elif (arm1=="01"):  # rキー
        print("r")
    #     initial_angle1 = max(initial_angle1 - step_angle, min_angle)
    #     move_servo1(initial_angle1)
        
    elif (arm2=="10"):  # iキー
        print("i")
    #     initial_angle2 = min(initial_angle2 + step_angle, max_angle)
    #     move_servo2(initial_angle2)
    elif (arm2=="01"):  # jキー
        print("j")
    #     initial_angle2 = max(initial_angle2 - step_angle, min_angle)
    #     move_servo2(initial_angle2)
    else:
        print("no")

"""
motor drive func/class
"""
# def set_motor_value(l_vel,r_vel):
#     msg = Int16MultiArray()
#     msg.data.append(l_vel)
#     msg.data.append(r_vel)
#     return msg

# def publish_motor_spd(pub, l_spd,r_spd):
#     pub.publish( set_motor_value(l_spd,r_spd) )


def key_to_spd(data):
    global setting_spd,MODE,l_out_spd,r_out_spd
    # print(data) # for test
    wad,s,spd,mode,arm1,arm2 = data.split(",")# in pc
    # wad,s,i,j,m,error = data.split(",")# raspi ver
    # chagnge l and r _set_spd
    setting_spd = int(spd) * 10
    move_arm(arm1,arm2)
    if(mode=="1"):
        if(MODE == True):
            MODE = False
        else:
            MODE = True
    
    # set l and r _out_spd
    if(s=="0"):
        if(wad=="111")|(wad=="100"):
            l_out_spd = setting_spd
            r_out_spd = setting_spd

        elif(wad=="110"):
            l_out_spd = int(setting_spd / 3)
            r_out_spd = setting_spd 
        elif(wad=="010"):
            l_out_spd = -setting_spd
            r_out_spd = setting_spd

        elif(wad=="101"):
            l_out_spd = setting_spd 
            r_out_spd = int(setting_spd / 3)
        elif(wad=="001"):
            l_out_spd = setting_spd 
            r_out_spd = -setting_spd

        else:
            l_out_spd = 0
            r_out_spd = 0
    else:
        if(wad=="010"):
            l_out_spd = int(-setting_spd / 3)
            r_out_spd = -setting_spd 
        elif(wad=="001"):
            l_out_spd = -setting_spd 
            r_out_spd = -int(setting_spd / 3)
        else:
            l_out_spd = -setting_spd
            r_out_spd = -setting_spd
    
    if(MODE == True):
        stock = l_out_spd
        l_out_spd = -1 * r_out_spd 
        r_out_spd = -1 * stock

    # print("Receive data = ", wad,"s",s,"j",j,"i",i)
    print("setting spd: ",setting_spd)
    print("Lout",l_out_spd,"Rout",r_out_spd,"\n\n")
    return l_out_spd,r_out_spd



def main():
    # rospy.init_node("bringup_controller")
    # motor_vel_pub = rospy.Publisher("/motor_vel", Int16MultiArray, queue_size=2)

    # Start receiving data from client
    recvThread = threading.Thread(target=wsStart)
    recvThread.daemon = True    
    recvThread.start()
    print("Threading Start")
    try:
        while True:
            if len(wsServer.rcvData):    
                data = wsServer.rcvData[0]

                l_out_spd,r_out_spd = key_to_spd(data)

                # publish_motor_spd(motor_vel_pub, l_out_spd, r_out_spd)

                wsServer.rcvData.pop(0)   
            time.sleep(0.005)

    except KeyboardInterrupt:
        print("Keyboard Interrupt")

    print("Loop terminated")


if __name__ == "__main__":
    main()