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


# this pc
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


# 画像type変換
def cvimage_to_pygame(image):
    """Convert cvimage into a pygame image"""
    return pygame.image.frombuffer(image.tostring(), image.shape[1::-1],"BGR")



def main():
    #pygameの初期設定
    pygame.init()
    pygame.display.set_caption("RASPI_CAMERA")
    screen = pygame.display.set_mode((FrameSize,FrameSize))                           
    clock = pygame.time.Clock()
    #udpの設定
    udp_recive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_recive.bind((my_ip,my_port))
    
    # 画像を取り続ける
    for img,count in recive(udp_recive):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # キーボード入力受け取りとsend
        try:
            if(count==DataSplitNum):                                                 
                frame = cv2.resize(img,(FrameSize,FrameSize))                   
            else:
                frame = black_img
                print("data count != %d\n",DataSplitNum)
        except cv2.error:
            frame = black_img
            print("img empty\n")

        img = cvimage_to_pygame(frame)
        screen.blit(img,(0,0))
        pygame.display.update()

        clock.tick()

        if cv2.waitKey(25) & 0xFF == ord('n'):
            break
        
if __name__ == "__main__":
    main()