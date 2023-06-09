import socket
import time 

def main():
    # UDPなどのパケット？ソケット？を設定
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 送信先のIPアドレスとポート番号
    to_send_addr = ('192.168.0.23', 8080)
    e_message = "second message"
    i = 0
    s = 0
    while True:
        time.sleep(0.03)
        message = str(s) + e_message
        message_byte = message.encode()
        udp.sendto(message_byte,to_send_addr)
        if(i==30):
            s += 1
            print(s," second")
            i = 0
        i += 1
    udp.close()


if __name__ == '__main__':
    main()