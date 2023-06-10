import pygame
import sys
import cv2
import socket
import numpy as np

bg_y = 0
px = 320
py = 240

# kuas@123 '00.00.00.00'
send_ip     = '00.00.00.00'
send_port   = 8008

# this pc
recive_ip   = '00.00.00.00'
recive_port = 8008

def recive(udp):
    buff = 1024 * 64
    while True:
        recive_data = bytes()
        # 写真データの受け取り
        
        while True:
            # 送られてくるデータが大きいので一度に受け取るデータ量を大きく設定
            jpg_str, addr = udp.recvfrom(buff)
            is_len = len(jpg_str) == 7
            is_end = jpg_str == b'__end__'
            if is_len and is_end: 
                break
            recive_data += jpg_str
        # 受け取ったデータがなかった時、whileをやり直す
        if len(recive_data) == 0: continue

        # メッセージを受け取る
        # jpg_str, addr = udp.recvfrom(buff)
        # message = jpg_str.decode()

        # string型からnumpyを用いuint8に戻す
        narray = np.frombuffer(recive_data, dtype='uint8')

        # uint8のデータを画像データに戻す
        img = cv2.imdecode(narray, 1)
        yield img




# キーボード入力を読み取り、エンコードして、相手にデータを送る
def send_key_input(key,udp,addr):
    global px,py
    if key[pygame.K_UP] == 1:
        py = py - 5
        if py < 20:
            py = 20
    if key[pygame.K_DOWN] == 1:
        py = py + 5
        if py > 460:
            py = 460
    if key[pygame.K_LEFT] == 1:
        px = px - 5
        if px < 20:
            px = 20
    if key[pygame.K_RIGHT] == 1:
        px = px + 5
        if px > 620:
            px = 620
    # 送るデータの形
    # massage =  "-"+ str(px) +"-"+ str(py)
    # -> = "-00-00"のようになる
    message = "-"+ str(px) +"-"+ str(py)
    message_byte = message.encode()
    udp.sendto(message_byte,addr)
    return message

# https://stackoverflow.com/questions/19306211/opencv-cv2-image-to-pygame-image
# openCV配列からpygame配列へ変換する
def cvimage_to_pygame(image):
    """Convert cvimage into a pygame image"""
    return pygame.image.frombuffer(image.tostring(), image.shape[1::-1],"BGR")

# speedなどのデータを画像に書き込む
def print_text(message):
    img = np.zeros((100,640,3), np.uint8)
    cv2.putText(img,message,(50,50),0,0.5,(0,255,0),1,cv2.LINE_4)
    return img

def main():
    global bg_y,send_ip,send_port,recive_port,recive_ip

    pygame.init()
    pygame.display.set_caption("RASPI_CAMERA")
    screen = pygame.display.set_mode((640,580))
    clock = pygame.time.Clock()

    udp_recive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_recive.bind((recive_ip,recive_port))

    udp_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    to_send_addr = (send_ip,send_port)


    # 画像を取り続ける
    for img in recive(udp_recive):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # キーボード入力受け取りとsend
        key     = pygame.key.get_pressed()
        message = send_key_input(key,udp_send,to_send_addr)

        # PC上に写す用の写真作成
        try:
            frame = cv2.resize(img,(640,480))
            data_img = print_text(message)
            dip_img = cv2.vconcat([frame,data_img]) #https://note.nkmk.me/python-opencv-hconcat-vconcat-np-tile/
            img = cvimage_to_pygame(dip_img)
            screen.blit(img,(0,0))
            pygame.display.update()
        except cv2.error:
            print("img empty\n")
        
        clock.tick()
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        
if __name__ == "__main__":
    main()