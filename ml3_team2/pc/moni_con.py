#--------------------------------------------------------
    # monitorとcontroller用のコード
    # bambi01-95 m058
#--------------------------------------------------------
# opencv画像からpygame画像への変換 :https://stackoverflow.com/questions/19306211/opencv-cv2-image-to-pygame-image
# pygameの指定キーの名前一覧       :https://www.pygame.org/docs/ref/key.html
# 画像結合                       :#https://note.nkmk.me/python-opencv-hconcat-vconcat-np-tile/
# *1 1枚の画像が送り終わった目印として、__end__を送っている。そして、その長さと文字列の確認を行なっている。

import pygame
import sys
import cv2
import socket
import numpy as np
import time
# Raspi(to)
sendToIp   = '172.16.0.31'
sendToPort = 8008#8008

# this pc(from)
my_ip      = '172.68.0.31'
my_port    = 8080

FrameSize = 800
DataSplitNum = 16

L_motor_spd = 10
R_motor_spd = 10

black_img = np.zeros((FrameSize,FrameSize,3), np.uint8)  





def recive(udp):
    buff = 1024 * 64
    while True:
        recive_data = bytes()
        count = 0
        # 画像データの受け取り
        while True:
            jpg_str, addr = udp.recvfrom(buff)
            is_len = len(jpg_str) == 7
            is_end = jpg_str == b'__end__' 
            if is_len and is_end: #　*1
                break
            count += 1
            recive_data += jpg_str
        if len(recive_data) == 0: continue

        # string型からnumpyを用いuint8に戻す
        narray = np.frombuffer(recive_data, dtype='uint8')

        # uint8のデータを画像データに戻す
        img = cv2.imdecode(narray, 1)
        yield img,count



# キーボード入力を読み取り->相手にデータを送る->表示テキスト作成
def send_key_input(key,udp,addr):
    global L_motor_spd,R_motor_spd
    L_out = 0
    R_out = 0

    if key[pygame.K_w] == 1:
        L_out = L_motor_spd
        R_out = R_motor_spd

    if key[pygame.K_a] == 1:
        R_out = R_motor_spd
        if L_out != 0:
            L_out = int(L_out/2)

    if key[pygame.K_d] == 1:
        L_out = L_motor_spd
        if R_out != 0:
            R_out = int(R_out / 2)
        
    if key[pygame.K_s] == 1:
        L_motor_spd *= -1
        R_motor_spd *= -1

    if (key[pygame.K_c] == 1) & (key[pygame.K_LCTRL] == 1):
        print("C + cotrol: FINISH!")
        exit(0)
    
    if (key[pygame.K_i] == 1):
        L_motor_spd += 10
        R_motor_spd += 10
        if 50 < L_motor_spd:
            L_motor_spd = 50
            R_motor_spd = 50

    if (key[pygame.K_j] == 1):
        L_motor_spd -= 10
        R_motor_spd -= 10
        if L_motor_spd < 0:
            L_motor_spd = 0
            R_motor_spd = 0
    # データの送信
    message = str(L_out) +","+ str(R_out)        
    message_byte = message.encode()
    udp.sendto(message_byte,addr)
    # 表示用テキストの作成
    settext  = "setting L motor: " + str(L_motor_spd) + " R motor: " + str(R_motor_spd) 
    outtext  = "output  L motor: " + str(L_out)   + " R motor: " + str(R_out) 
    return settext,outtext


# speedなどのデータを画像に書き込む
def print_text(settext,outtext):
    img = np.zeros((100,FrameSize,3), np.uint8)                                   
    cv2.putText(img,settext,(50,50),0,0.6,(0,255,0),1,cv2.LINE_4)
    cv2.putText(img,outtext,(50,75),0,0.6,(0,255,0),1,cv2.LINE_4)
    return img


# 画像type変換
def cvimage_to_pygame(image):
    """Convert cvimage into a pygame image"""
    return pygame.image.frombuffer(image.tostring(), image.shape[1::-1],"BGR")



def main():
    global bg_y,sendToIp,sendToPort
    #pygameの初期設定
    pygame.init()
    pygame.display.set_caption("RASPI_CAMERA")
    screen = pygame.display.set_mode((FrameSize,FrameSize+100))                           
    clock = pygame.time.Clock()
    #udpの設定
    udp_recive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_recive.bind((my_ip,my_port))

    udp_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    to_send_addr = (sendToIp,sendToPort)


    
    # 画像を取り続ける
    for img,count in recive(udp_recive):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # キーボード入力受け取りとsend
        key     = pygame.key.get_pressed()
        settext,outtext = send_key_input(key,udp_send,to_send_addr)


        # # PC上に写す用の写真作成
        data_img = print_text(settext,outtext)
        try:
            if(count==DataSplitNum):                                                 
                frame = cv2.resize(img,(FrameSize,FrameSize))                   
                v_img = cv2.vconcat([frame,data_img]) 
            else:
                print("data count != %d\n",DataSplitNum)
        except cv2.error:
            print("img empty\n")
            v_img = cv2.vconcat([black_img,data_img])

        v_img = cv2.resize(v_img,(FrameSize,FrameSize+100))
        img = cvimage_to_pygame(v_img)
        screen.blit(img,(0,0))
        pygame.display.update()

        clock.tick()

        if cv2.waitKey(25) & 0xFF == ord('n'):
            break
        
if __name__ == "__main__":
    main()