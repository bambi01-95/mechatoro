# -*- coding: utf-8 -*-
# WebSocketServer.py
# sudo pip3 install websocket-server
from websocket_server import WebsocketServer
import threading
import time

HOST = "172.31.33.254" # IPアドレスopen
PORT = 5000 # ポートを指定

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
        self.server.send_message(client, "OK, Received : " + str(self.user))
        self.rcvData.append(message)
    
    def runServer(self):
        self.server.set_fn_new_client(self.newClient)    # Client接続時
        self.server.set_fn_client_left(self.clientLeft)    # Client切断時
        self.server.set_fn_message_received(self.messageReceived)     # Clientからの受信時
        self.server.run_forever()

wsServer = WsServer(HOST, PORT)


def wsStart():
    wsServer.runServer()

# Start receiving data from client
recvThread = threading.Thread(target=wsStart)
recvThread.daemon = True    # 修了時にハングアップしない
recvThread.start()
print("Threading Start")

l_set_spd = 0
r_set_spd = 0

l_out_spd = 0
r_out_spd = 0

try:
    while True:
        time.sleep(0.1)
        if len(wsServer.rcvData):    # Receive data from Client PC
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
            print("---------------------------")
            wsServer.rcvData.pop(0)    # Pop Top data

                
except KeyboardInterrupt:
    print("Keyboard Interrupt")

print("Loop terminated")