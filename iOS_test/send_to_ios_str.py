import socket
import time 

def main():
    # UDPなどのパケット？ソケット？を設定
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 送信先のIPアドレスとポート番号
    to_send_addr1 = ('192.168.50.178', 8000)
    to_send_addr2 = ('192.168.50.195', 8000)
    e_message = ""
    i = 0
    s = 0
    while True:
        time.sleep(0.03)
        message = str(s)
        message_byte = message.encode()
        udp.sendto(message_byte,to_send_addr1)
        udp.sendto(message_byte,to_send_addr2)
        if(i==30):
            s += 2
            print(s," second")
            i = 0
        i += 1
        if(s>=20):
            s = -20
    udp.close()


if __name__ == '__main__':
    main()