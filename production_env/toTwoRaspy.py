#--------------------------------------------------------
    # 説明書と画像のストリーミングなし、コントローラーの値だけを送る。
    # bambi01-95 m058
#--------------------------------------------------------
# opencv画像からpygame画像への変換 :https://stackoverflow.com/questions/19306211/opencv-cv2-image-to-pygame-image
# pygameの指定キーの名前一覧       :https://www.pygame.org/docs/ref/key.html

import pygame #for multi-keyboard input
import sys
import cv2
import socket
import numpy as np
import time


L_motor_spd = 10
R_motor_spd = 10 

FrameSize = 800

black_img = np.zeros((FrameSize,FrameSize,3), np.uint8)  

# 2.kuas@123 '00.00.00.00'
send_ip1     = '172.20.10.11'
send_port1   = 8000#8008

# 2.kuas@123 '00.00.00.00'
send_ip2     = '172.20.10.13'
send_port2   = 8000#8008

# udpの設定
udp_send1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
to_send_addr1 = (send_ip1,send_port1)

udp_send2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
to_send_addr2 = (send_ip2,send_port2)

# キーボード入力を読み取り、エンコードして、相手にデータを送る
def send_key_input(key):
    global L_motor_spd,R_motor_spd,udp_send1,udp_send2,to_send_addr1,to_send_addr2
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

    # 送るデータの形
    # Lmotor Rmotor
    message1 = str(L_out)               
    message2 = str(R_out)
    print(message1,":",message2)
    message_byte1 = message1.encode()
    message_byte2 = message2.encode()
    udp_send1.sendto(message_byte1,to_send_addr1)
    udp_send2.sendto(message_byte2,to_send_addr2)

    settext  = "setting L motor speed: " + str(L_motor_spd) + " R motor speed: " + str(R_motor_spd) 
    outtext  = "control L motor speed: " + str(L_out)       + " R motor speed: " + str(R_out) 
    return settext,outtext


# openCV配列からpygame配列へ変換する
def cvimage_to_pygame(image):
    """Convert cvimage into a pygame image"""
    return pygame.image.frombuffer(image.tostring(), image.shape[1::-1],"BGR")

# speedなどのデータを画像に書き込む
def print_text(settext,outtext):
    img = np.zeros((100,FrameSize,3), np.uint8)                                  
    cv2.putText(img,settext,(50,50),0,0.6,(0,255,0),1,cv2.LINE_4)
    cv2.putText(img,outtext,(50,75),0,0.6,(0,255,0),1,cv2.LINE_4)
    return img

def main():

    # pygameの起動と設定
    pygame.init()
    pygame.display.set_caption("RASPI_CAMERA")
    screen = pygame.display.set_mode((FrameSize,FrameSize+100))                         
    clock = pygame.time.Clock()



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # キーボード入力受け取りとsend
        key     = pygame.key.get_pressed()
        settext,outtext = send_key_input(key)

        data_img = print_text(settext,outtext)
        v_img = cv2.vconcat([black_img,data_img]) 
        v_img = cv2.resize(v_img,(FrameSize,FrameSize+100))
        img = cvimage_to_pygame(v_img)#if you need
        screen.blit(img,(0,0))
        pygame.display.update()
        time.sleep(0.05)
        clock.tick()

        if cv2.waitKey(25) & 0xFF == ord('n'):
            break
        
if __name__ == "__main__":
    main()