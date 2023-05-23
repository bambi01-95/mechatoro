import socket


def main():
    # UDPなどのパケット？ソケット？を設定
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 送信先のIPアドレスとポート番号
    to_send_addr = ('00.00.00.00', 8008)
    message = "00:00:00:00"

    while True:
        
        message_byte = message.encode()
        udp.sendto(message_byte,to_send_addr)

    udp.close()


if __name__ == '__main__':
    main()
