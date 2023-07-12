#--------------------------------------------------------
    # コントローラーの値だけを送る。
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
# raspi
send_ip     = '192.168.0.31'
send_port   = 8008#8008

L_motor_spd = 10
R_motor_spd = 10 

FrameSize = 800

black_img = np.zeros((FrameSize,FrameSize - 100,3), np.uint8)  




# キーボード入力を読み取り、エンコードして、相手にデータを送る
def send_key_input(key,udp,addr):
    global L_motor_spd,R_motor_spd
    L_out = 0
    R_out = 0
    wad = str(key[pygame.K_w]) + str(key[pygame.K_a]) + str(key[pygame.K_d])
    wad = int(wad,2)
    if key[pygame.K_s] == 1:
        L_motor_spd *= -1
        R_motor_spd *= -1
        wad = wad ^ 0b011

    if(wad==0b111)|(wad==0b100):
        L_out = L_motor_spd
        R_out = R_motor_spd
    elif(wad==0b110):
        L_out = L_motor_spd
        R_out = R_motor_spd / 2
    elif(wad==0b010):
        L_out = L_motor_spd
        R_out = 0
    elif(wad==0b101):
        L_out = L_motor_spd / 2
        R_out = R_motor_spd 
    elif(wad==0b001):
        L_out = 0
        R_out = R_motor_spd
    else:
        L_out = 0
        R_out = 0

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
    message = str(L_out) +","+ str(R_out)                  
    print(message)
    message_byte = message.encode()
    udp.sendto(message_byte,addr)

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
    global send_ip,send_port
    # pygameの起動と設定
    pygame.init()
    pygame.display.set_caption("RASPI_CAMERA")
    screen = pygame.display.set_mode((FrameSize,FrameSize+100))                         
    clock = pygame.time.Clock()

    # udpの設定
    udp_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    to_send_addr = (send_ip,send_port)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # キーボード入力受け取りとsend
        key     = pygame.key.get_pressed()
        settext,outtext = send_key_input(key,udp_send,to_send_addr)

        data_img = print_text(settext,outtext)
        v_img = cv2.vconcat([black_img,data_img]) 
        img = cvimage_to_pygame(v_img)
        screen.blit(img,(0,0))
        pygame.display.update()
        time.sleep(0.05)
        clock.tick()

        if cv2.waitKey(25) & 0xFF == ord('n'):
            break
        
if __name__ == "__main__":
    main()