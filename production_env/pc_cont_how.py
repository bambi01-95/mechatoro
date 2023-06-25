#--------------------------------------------------------
    # ストリーミングなし、説明書とコントローラの値を送る
    # bambi01-95 m058
#--------------------------------------------------------
# opencv画像からpygame画像への変換 :https://stackoverflow.com/questions/19306211/opencv-cv2-image-to-pygame-image
# pygameの指定キーの名前一覧       :https://www.pygame.org/docs/ref/key.html
# 画像結合                       :#https://note.nkmk.me/python-opencv-hconcat-vconcat-np-tile/


import pygame
import sys
import cv2
import socket
import numpy as np
import time

L_motor_spd = 10
R_motor_spd = 10

frame_size = 800

black_img = np.zeros((frame_size,frame_size,3), np.uint8)  

sendToIp     = '192.168.0.31'
sendToPort   = 8008#8008


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
    print(message)
    message_byte = message.encode()
    udp.sendto(message_byte,addr)
    #　表示用テキストの作成
    settext  = "setting L motor: " + str(L_motor_spd) + " R motor: " + str(R_motor_spd) 
    outtext  = "output  L motor: " + str(L_out)   + " R motor: " + str(R_out) 
    return settext,outtext


# openCV配列からpygame配列へ変換する
def cvimage_to_pygame(image):
    """Convert cvimage into a pygame image"""
    return pygame.image.frombuffer(image.tostring(), image.shape[1::-1],"BGR")

# speedなどのデータを画像に書き込む
def print_text(settext,outtext):
    img = np.zeros((100,frame_size,3), np.uint8)                                
    cv2.putText(img,settext,(50,50),0,0.6,(0,255,0),1,cv2.LINE_4)
    cv2.putText(img,outtext,(50,75),0,0.6,(0,255,0),1,cv2.LINE_4)
    return img

def main():
    global bg_y,sendToIp,sendToPort
    # pygameの初期設定
    pygame.init()
    pygame.display.set_caption("RASPI_CAMERA")
    screen = pygame.display.set_mode((frame_size + frame_size,frame_size+100))                   
    clock = pygame.time.Clock()

    # udpの設定
    udp_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    to_send_addr = (sendToIp,sendToPort)

    # 説明書の読み込み（同じディレクトリにないとダメ）
    test = cv2.imread('inst1.png')
    nstruction = cv2.resize(test,(frame_size,frame_size+100))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # キーボード入力処理とデータの送信
        key     = pygame.key.get_pressed()
        settext,outtext = send_key_input(key,udp_send,to_send_addr)

        # 表示画像の作成
        data_img = print_text(settext,outtext)
        v_img = cv2.vconcat([black_img,data_img]) 
        v_img = cv2.resize(v_img,(frame_size,frame_size+100))
        h_img = cv2.hconcat([v_img,nstruction])

        #表示
        img = cvimage_to_pygame(h_img)
        screen.blit(img,(0,0))
        pygame.display.update()
        time.sleep(0.05)
        clock.tick()

        if cv2.waitKey(25) & 0xFF == ord('n'):
            break
        
if __name__ == "__main__":
    main()