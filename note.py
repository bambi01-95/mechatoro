import pygame
import sys
import cv2
import socket
import numpy as np
import time


L_motor = 10
R_motor = 10
step = 2


black_img = np.zeros((400,400,3), np.uint8)  

# 2.kuas@123 '00.00.00.00'
#   mls:
# katu2:
#    my:
send_ip     = '192.168.0.31'
send_port   = 8008#8008

# 1.this pc
recive_ip   = '192.168.0.31'#192.168.50.250'
recive_port = 8080


def recive(udp):
    buff = 1024 * 64
    while True:
        recive_data = bytes()
        count = 0
        # 写真データの受け取り
        
        while True:
            # 送られてくるデータが大きいので一度に受け取るデータ量を大きく設定
            jpg_str, addr = udp.recvfrom(buff)
            is_len = len(jpg_str) == 7
            is_end = jpg_str == b'__end__'
            if is_len and is_end: 
                break
            count += 1
            recive_data += jpg_str
        # 受け取ったデータがなかった時、whileをやり直す
        if len(recive_data) == 0: continue

        # string型からnumpyを用いuint8に戻す
        narray = np.frombuffer(recive_data, dtype='uint8')

        # uint8のデータを画像データに戻す
        img = cv2.imdecode(narray, 1)
        yield img,count




# キーボード入力を読み取り、エンコードして、相手にデータを送る
def send_key_input(key,udp,addr):
    global L_motor,R_motor,step
    # key[???] ??? -> https://www.pygame.org/docs/ref/key.html
    if key[pygame.K_a] == 1:
        L_motor = L_motor - 2
        if L_motor < 0:
            L_motor = 0
    if key[pygame.K_d] == 1:
        R_motor = R_motor - 2
        if R_motor < 0:
            R_motor = 0

    if key[pygame.K_q] == 1:
        L_motor = 5
        R_motor = 30
    if key[pygame.K_e] == 1:
        L_motor = 30
        R_motor = 5

    if key[pygame.K_w] == 1:
        if(L_motor==R_motor):
            L_motor = L_motor + step
            R_motor = R_motor + step
            if L_motor > 40:
                L_motor = 40
            if R_motor > 40:
                R_motor = 40
        elif(R_motor>L_motor):
            L_motor = L_motor + step
        else:
            R_motor = R_motor + step


    if key[pygame.K_s] == 1:
        if(L_motor==R_motor):
            L_motor = L_motor - step
            R_motor = R_motor - step
            if L_motor < 0:
                L_motor = 0
            if R_motor < 0:
                R_motor = 0
        elif(R_motor>L_motor):
            R_motor = R_motor - step
        else:
            L_motor = L_motor - step


    if key[pygame.K_f] == 1:
        R_motor = 10
        L_motor = 10
    if key[pygame.K_j] == 1:
        exit(1)
    # 送るデータの形
    # Lmotor Rmotor
    message = str(L_motor) +","+ str(R_motor)                   #check
    text    = "L motor: " + str(L_motor) + " R motor: " + str(R_motor)
    print(message)
    message_byte = message.encode()
    udp.sendto(message_byte,addr)
    return text

# https://stackoverflow.com/questions/19306211/opencv-cv2-image-to-pygame-image
# openCV配列からpygame配列へ変換する
def cvimage_to_pygame(image):
    """Convert cvimage into a pygame image"""
    return pygame.image.frombuffer(image.tostring(), image.shape[1::-1],"BGR")

# speedなどのデータを画像に書き込む
def print_text(message):
    img = np.zeros((100,400,3), np.uint8)                                   #check
    cv2.putText(img,message,(50,50),0,0.5,(0,255,0),1,cv2.LINE_4)
    return img

def main():
    global bg_y,send_ip,send_port,recive_port,recive_ip

    pygame.init()
    pygame.display.set_caption("RASPI_CAMERA")
    screen = pygame.display.set_mode((400,500))                            #check
    clock = pygame.time.Clock()

    udp_recive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_recive.bind((recive_ip,recive_port))

    udp_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    to_send_addr = (send_ip,send_port)

    # 画像を取り続ける
    for img,count in recive(udp_recive):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # キーボード入力受け取りとsend
        key     = pygame.key.get_pressed()
        message = send_key_input(key,udp_send,to_send_addr)
        time.sleep(0.03)

        # # PC上に写す用の写真作成
        try:
            if(count==16):                                                  # check
                frame = cv2.resize(img,(400,400))                           # check
                data_img = print_text(message)
                dip_img = cv2.vconcat([frame,data_img]) #https://note.nkmk.me/python-opencv-hconcat-vconcat-np-tile/
                img = cvimage_to_pygame(dip_img)
                screen.blit(img,(0,0))
                pygame.display.update()
            else:
                print("img has noize\n")
        except cv2.error:
            data_img = print_text(message)
            dip_img = cv2.vconcat([black_img,data_img]) #https://note.nkmk.me/python-opencv-hconcat-vconcat-np-tile/
            img = cvimage_to_pygame(dip_img)
            screen.blit(img,(0,0))
            pygame.display.update()
            print("img empty\n")

        clock.tick()
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        
if __name__ == "__main__":
    main()

