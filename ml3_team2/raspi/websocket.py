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


MAX_MOTOR_SPD = 90
MIN_MOTOR_SPD = 10

l_set_spd = 0
r_set_spd = 0

l_out_spd = 0
r_out_spd = 0

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
        self.server.send_message(client, "L_s" + l_set_spd + "R_s" +r_set_spd +"L_o"+l_out_spd+"R_o"+r_out_spd )
        self.rcvData.append(message)

    def runServer(self):
        self.server.set_fn_new_client(self.newClient)    # Client接続時
        self.server.set_fn_client_left(self.clientLeft)    # Client切断時
        self.server.set_fn_message_received(self.messageReceived)     # Clientからの受信時
        self.server.run_forever()


wsServer = WsServer(HOST, PORT)


def wsStart():
    wsServer.runServer()

def main():
    # Start receiving data from client
    recvThread = threading.Thread(target=wsStart)
    recvThread.daemon = True    # 修了時にハングアップしない
    recvThread.start()
    print("Threading Start")
    rospy.init_node("bringup_controller")
    motor_vel_pub = rospy.Publisher("/motor_vel", Int16MultiArray, queue_size=2)


    try:
        while True:
            time.sleep(0.1)
            if len(wsServer.rcvData):    # Receive data from Client PC
                wsServer.rcvData.pop(0)    # Pop Top data
                wad,s,i,j = wsServer.rcvData[0].split(",")
                wad = int(wad)
                if(wad==100):
                    l_out_spd = l_set_spd
                    r_out_spd = r_set_spd
                elif(wad==110):
                    l_out_spd = l_set_spd
                    r_out_spd = r_set_spd / 2
                elif(wad==10):
                    l_out_spd = l_set_spd
                    r_out_spd = 0
                elif(wad==101):
                    l_out_spd = l_set_spd / 2
                    r_out_spd = r_set_spd 
                elif(wad==1):
                    l_out_spd = l_set_spd
                    r_out_spd = 0
                else:
                    l_out_spd = 0
                    r_out_spd = 0

                if(s=="1"):
                    l_set_spd *= -1
                    r_set_spd *= -1
                if(i=="1"):
                    l_set_spd += 10
                    r_set_spd += 10
                    if(l_set_spd>100):
                        l_set_spd = 100
                        r_set_spd = 100

                if(j=="1"):
                    l_set_spd -= 10
                    r_set_spd -= 10
                    if(l_set_spd<0):
                        l_set_spd = 0
                        r_set_spd = 0
                print("Receive data = ", wad,"s",s,"j",j,"i",i)
                print("Lset",l_set_spd,"Rset",r_set_spd)
                print("Lout",l_out_spd,"Rout",r_out_spd)
                publish_motor_spd(motor_vel_pub, l_out_spd, r_out_spd)

                    
    except KeyboardInterrupt:
        print("Keyboard Interrupt")

    print("Loop terminated")


if __name__ == "__main__":
    main()