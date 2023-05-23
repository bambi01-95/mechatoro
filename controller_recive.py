import socket


# フレーム生成・返却する処理
def main():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(('00.00.00.00', 8008))
    buff = 1024 * 64

    while True:
        jpg_str, addr = udp.recvfrom(buff)
        message = jpg_str.decode()
        left  = message[0:2]
        right = message[2:4]
        arm   = message[6:8]




if __name__ == '__main__':
    main()