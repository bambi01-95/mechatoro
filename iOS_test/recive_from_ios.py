import socket

# フレーム生成・返却する処理
def main():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(('', 8080))
    buff = 1024 * 64
    count = 0
    while True:
        if(count<1):
            print("wait a message now\n")
        str, addr = udp.recvfrom(buff)
        message = str.decode()
        print(count,": ",message)
        count+=1

if __name__ == '__main__':
    main()