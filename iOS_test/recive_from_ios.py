import socket

# フレーム生成・返却する処理
def main():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(('192.168.0.31', 8008))
    buff = 1024 * 64
    count = 0
    message = "1,1"
    while True:
        if(count<1):
            print("wait a message now\n")
        str, addr = udp.recvfrom(buff)
        message = str.decode()
        a,b = message.split(',',2)
        print(count,") L: ",a," R: ",b)
        count+=1

if __name__ == '__main__':
    main()