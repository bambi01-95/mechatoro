import socket
import rospy
import sys,tty
from std_msgs.msg import Float32MultiArray

import numpy as np # add 2023/06/14       #check



#-----------------------------------------------------------------
    # コントローラ(PC / iPhone)からデータを受け取り、ROSにデータを上げるコード
#-----------------------------------------------------------------

# this pc/RasPi ip & port
#   mls:
# katu2:
#    my:
recive_ip   = '172.20.10.7'
recive_port = 8080
to_recive_addr = (recive_ip,recive_port)



# ROSのデータ更新
def publish_motor_spd(pub, spd):                            #----
    pub.publish( set_motor_value(spd) )
def set_motor_value(motor_vel):                         #---
    msg = Float32MultiArray()
    msg.data.append(motor_vel)
    return msg                              # check!!!!


# 自分が受け取る
def receive():
    global to_recive_addr
    # setting udp
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(to_recive_addr)

    # setting rospy
    rospy.init_node("bringup_controller")                     #----
    # ROS 値の初期化                                                 #----  queue_size データのストック like push and
    l_motor_vel_pub = rospy.Publisher("/set_setpoint_left_motor", Float32MultiArray, queue_size=10)
    r_motor_vel_pub = rospy.Publisher("/set_setpoint_right_motor", Float32MultiArray, queue_size=10)
    l_motor_spd = 0
    r_motor_spd = 0
    # 受け取れる最大のデータ量
    buff = 1024 * 64
    while not rospy.is_shutdown():
        # データの受け取り
        str, addr = udp.recvfrom(buff)
        message = str.decode()
        # spliting message by ','. :https://note.nkmk.me/python-split-rsplit-splitlines-re/
        lm,rm,other = message.split(',',2)          # change!!!
        l_motor_spd = float(lm)
        r_motor_spd = float(rm)
        # sabo    = float(message[6:8])
        # rosにデータを上げる（更新）
        publish_motor_spd(l_motor_vel_pub, l_motor_spd)
        publish_motor_spd(r_motor_vel_pub, r_motor_spd) 
        rospy.loginfo(f" Left_motor_spd : {l_motor_spd}")
        rospy.loginfo(f"Right_motor_spd : {r_motor_spd}")
    udp.close()





#-----------------------------------------------------------------
if __name__ == '__main__':
    receive()
    print("end of the code\n")