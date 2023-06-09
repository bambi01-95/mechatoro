import socket
import time 

def main():
    # UDPなどのパケット？ソケット？を設定
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 送信先のIPアドレスとポート番号
    to_send_addr = ('172.20.10.8', 8080)
    message = "anata"
    i = 0
    while True:
        time.sleep(0.03)
        message_byte = message.encode()
        udp.sendto(message_byte,to_send_addr)
        if(i==30):
            print("sendndndndnnd")
            i = 0
        i += 1
    udp.close()


if __name__ == '__main__':
    main()
