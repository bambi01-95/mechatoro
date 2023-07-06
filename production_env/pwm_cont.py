#-----------------------------------------------------------------
    # コントローラ(PC / iPhone)からデータを受け取り、ROSにデータを上げるコード
    # bambi01-95 m058　
#-----------------------------------------------------------------
# split ::https://note.nkmk.me/python-split-rsplit-splitlines-re/

import socket
import rospy
from std_msgs.msg import Float32MultiArray
import numpy as np 

# this pc/RasPi ip & port
my_ip   = '172.20.10.7'
my_port = 8080
my_addr = (my_ip,my_port)



# ROSのデータ更新
def publish_motor_spd(pub, spd):                   
    pub.publish( set_motor_value(spd) )
def set_motor_value(motor_vel_l,motor_vel_r):                     
    msg = Float32MultiArray()
    msg.data.append(motor_vel_l)
    msg.data.append(motor_vel_r)
    return msg


# 自分が受け取る
def receive():
    global my_addr
    # setting udp
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(my_addr)

    # setting rospy
    rospy.init_node("bringup_controller")                    
    # ROS 値の初期化                     (rosのアクセス名, publishするdata-type, データのストックできる数)
    l_motor_vel_pub = rospy.Publisher("/motor_vel", Float32MultiArray, queue_size=1)
    l_motor_spd = 0
    r_motor_spd = 0
    # 受け取れる最大のデータ量
    buff = 1024 * 64
    while not rospy.is_shutdown():
        # 受信データ処理
        str, addr = udp.recvfrom(buff)
        message = str.decode()
        lm,rm,other = message.split(',',2)    
        l_motor_spd = float(lm)
        r_motor_spd = float(rm)
        # rosにデータを上げる（更新）
        publish_motor_spd(l_motor_vel_pub, l_motor_spd,r_motor_spd)
        rospy.loginfo(f" Left_motor_spd : {l_motor_spd}")
        rospy.loginfo(f"Right_motor_spd : {r_motor_spd}")
    udp.close()





#-----------------------------------------------------------------
if __name__ == '__main__':
    receive()
    print("end of the code\n")