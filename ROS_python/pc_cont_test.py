import pygame
import sys
import cv2
import socket
import numpy as np
import time

bg_y = 0
L_motor = 10
R_motor = 10
step = 2

frame_size = 800

black_img = np.zeros((frame_size,frame_size,3), np.uint8)  


# cv2.imshow("this",nstruction)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# exit(1)
# 2.kuas@123 '00.00.00.00'
#   mls:
# katu2:
#    my:
send_ip     = '192.168.0.31'
send_port   = 8008#8008


# キーボード入力を読み取り、エンコードして、相手にデータを送る
def send_key_input(key,udp,addr):
    global L_motor,R_motor,step
    L_out = 0
    R_out = 0
    # key[???] ??? -> https://www.pygame.org/docs/ref/key.html
    if key[pygame.K_w] == 1:
        L_out = L_motor
        R_out = R_motor

    if key[pygame.K_a] == 1:
        R_out = R_motor
        if L_out != 0:
            L_out = int(L_out/2)

    if key[pygame.K_d] == 1:
        L_out = L_motor
        if R_out != 0:
            R_out = int(R_out / 2)
        
    if key[pygame.K_s] == 1:
        L_motor *= -1
        R_motor *= -1

    if (key[pygame.K_c] == 1) & (key[pygame.K_LCTRL] == 1):
        print("C + cotrol: FINISH!")
        exit(0)
    
    if (key[pygame.K_i] == 1):
        L_motor += 10
        R_motor += 10
        if 50 < L_motor:
            L_motor = 50
            R_motor = 50

    if (key[pygame.K_j] == 1):
        L_motor -= 10
        R_motor -= 10
        if L_motor < 0:
            L_motor = 0
            R_motor = 0

    # 送るデータの形
    # Lmotor Rmotor
    message = str(L_out) +","+ str(R_out)                   #check

    settext  = "setting L motor: " + str(L_motor) + " R motor: " + str(R_motor) 
    outtext  = "output  L motor: " + str(L_out)   + " R motor: " + str(R_out) 
    print(message)
    message_byte = message.encode()
    udp.sendto(message_byte,addr)
    return settext,outtext

# https://stackoverflow.com/questions/19306211/opencv-cv2-image-to-pygame-image
# openCV配列からpygame配列へ変換する
def cvimage_to_pygame(image):
    """Convert cvimage into a pygame image"""
    return pygame.image.frombuffer(image.tostring(), image.shape[1::-1],"BGR")

# speedなどのデータを画像に書き込む
def print_text(settext,outtext):
    img = np.zeros((100,frame_size,3), np.uint8)                                   #check
    cv2.putText(img,settext,(50,50),0,0.6,(0,255,0),1,cv2.LINE_4)
    cv2.putText(img,outtext,(50,75),0,0.6,(0,255,0),1,cv2.LINE_4)
    return img

def main():
    global bg_y,send_ip,send_port

    pygame.init()
    pygame.display.set_caption("RASPI_CAMERA")
    screen = pygame.display.set_mode((frame_size,frame_size+100))                            #check
    clock = pygame.time.Clock()

    udp_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    to_send_addr = (send_ip,send_port)

    
    # 画像を取り続ける
    # for img,count in recive(udp_recive):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # キーボード入力受け取りとsend
        key     = pygame.key.get_pressed()
        settext,outtext = send_key_input(key,udp_send,to_send_addr)

        data_img = print_text(settext,outtext)
        v_img = cv2.vconcat([black_img,data_img]) #https://note.nkmk.me/python-opencv-hconcat-vconcat-np-tile/
        v_img = cv2.resize(v_img,(frame_size,frame_size+100))
        img = cvimage_to_pygame(v_img)#if you need
        screen.blit(img,(0,0))
        pygame.display.update()
        time.sleep(0.05)
        clock.tick()

        if cv2.waitKey(25) & 0xFF == ord('n'):
            break
        
if __name__ == "__main__":
    main()