#!/usr/bin/python3
import rospy
import select, termios
import sys, tty
import time
import numpy as np
from std_msgs.msg import Int16MultiArray
import socket

# this pc/RasPi ip & port
my_ip   = '172.20.10.7'
my_port = 8080
my_addr = (my_ip,my_port)


MAX_MOTOR_SPD = 90
MIN_MOTOR_SPD = 10


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
        lm,rm= message.split(',',2) 
        publish_motor_spd(motor_vel_pub, lm, rm)

        rospy.loginfo(f"motor_spd : {lm} {rm}")
        time.sleep(0.01)

if __name__ == "__main__":
    main()
