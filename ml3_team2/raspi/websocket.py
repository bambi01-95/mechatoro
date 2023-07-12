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
import socket


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
    wad = int(wad,2)
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
        wad = wad ^ 0b011  # if back

    # set l and r _out_spd
    if(wad&0b111)|(wad&0b100):
        l_out_spd = l_set_spd
        r_out_spd = r_set_spd
    elif(wad&0b110):
        l_out_spd = l_set_spd
        r_out_spd = int(r_set_spd / 2)
    elif(wad&0b010):
        l_out_spd = l_set_spd
        r_out_spd = 0
    elif(wad&0b101):
        l_out_spd = int(l_set_spd / 2)
        r_out_spd = r_set_spd 
    elif(wad&0b001):
        l_out_spd = 0
        r_out_spd = r_set_spd
    else:
        l_out_spd = 0
        r_out_spd = 0

    print("Receive data = ", wad,"s",s,"j",j,"i",i)
    print("Lset",l_set_spd,"Rset",r_set_spd)
    print("Lout",l_out_spd,"Rout",r_out_spd)

    return l_out_spd,r_out_spd



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