# -*- coding: utf-8 -*-
# WebSocketServer.py
# sudo pip3 install websocket-server
from websocket_server import WebsocketServer
import threading
import time

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


HOST = "172.31.33.254" # IPアドレスopen
PORT = 5000 # ポートを指定
wsServer = WsServer(HOST, PORT)


def wsStart():
    wsServer.runServer()

# Start receiving data from client
recvThread = threading.Thread(target=wsStart)
recvThread.daemon = True    # 修了時にハングアップしない
recvThread.start()
print("Threading Start")



try:
    while True:
        time.sleep(0.1)
        if len(wsServer.rcvData):    # Receive data from Client PC
            pdata = wsServer.rcvData[0].split(",")
            print("Receive data = ", pdata)
            wsServer.rcvData.pop(0)    # Pop Top data

                
except KeyboardInterrupt:
    print("Keyboard Interrupt")

print("Loop terminated")