# Lvec / Rvec / arm1 / arm2 

#!/usr/bin/python3
import socket

""" ros lib """
import rospy
import time
import numpy as np
from std_msgs.msg import Int16MultiArray

""" servo lib"""
# import RPi.GPIO as GPIO
# import sys
# import tty
# import termios

""" socket init"""
# this pc/RasPi ip & port
my_ip   = '172.20.10.7'
my_port = 8080
my_addr = (my_ip,my_port)

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
servo motor func/class
"""
def set_motor_value(l_vel,r_vel):
    msg = Int16MultiArray()
    msg.data.append(l_vel)
    msg.data.append(r_vel)
    return msg

def publish_motor_spd(pub, l_spd,r_spd):
    pub.publish( set_motor_value(l_spd,r_spd) )

def main():
    global my_addr
    # setting udp
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(my_addr)

    rospy.init_node("bringup_controller")
    motor_vel_pub = rospy.Publisher("/motor_vel", Int16MultiArray, queue_size=2)
    buff = 2**16
    
    while not rospy.is_shutdown():
        str, addr = udp.recvfrom(buff)
        message = str.decode()
        lm,rm,arm1,arm2= message.split(',',4) 
        move_arm(arm1,arm2)
        publish_motor_spd(motor_vel_pub, lm, rm)
        rospy.loginfo(f"motor_spd : {lm} {rm}")
        time.sleep(0.01)
    

if __name__ == "__main__":
    main()
