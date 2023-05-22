# keyboardの同時複数入力を可能とする関数、kbhit pygame keyboard

# pygame: http://westplain.sakura.ne.jp/translate/pygame/Key.cgi#pygame.key.get_pressed

# import keyboard ?



# https://goodlucknetlife.com/python-pygame-player-move/

import pygame
import sys

# img_bg = pygame.image.load("bgimage.png")
# img_player = pygame.image.load("player1.png")
bg_y = 0
px = 320
py = 240

def move_player(screen,key):
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
    print("px: ",px,",py: ",py)

def main():
    global bg_y

    pygame.init()
    pygame.display.set_caption("シューティングゲーム")
    screen = pygame.display.set_mode((640,480))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        key = pygame.key.get_pressed()
        move_player(screen,key)
        pygame.display.update()
        clock.tick()
        
if __name__ == "__main__":
    main()

# # # # # # < pygame > # # # # # # 
# https://shizenkarasuzon.hatenablog.com/entry/2019/02/08/184932
# from pygame.locals import * # python3 -m pip install pygame
# import pygame
# import sys

# pygame.init()    # Pygameを初期化
# screen = pygame.display.set_mode((400, 330))    # 画面を作成
# pygame.display.set_caption("keyboard event")    # タイトルを作成


# while True:
#     screen.fill((0, 0, 0)) 
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#             sys.exit()
#         if event.type == KEYDOWN:  # キーを押したとき
#             # ESCキーならスクリプトを終了
#             if event.key == K_ESCAPE:
#                 pygame.quit()
#                 sys.exit()
            
#             else:
#                 print("押されたキー = " + pygame.key.name(event.key))
#         pygame.display.update()

# # # # # # < kbhit > # # # # # # 
# import select, termios
# import sys, tty
# import time
# from kbhit import *
# def main():
#     atexit.register(set_normal_term)
#     set_curses_term()
#     speed = 0
#     left = 0
#     right = 0
#     while True:
#         if kbhit():     # 何かキーが押されるのを待つ
#             key = getch() 
#         # input = select.select([sys.stdin], [], [], 0.1)[0]
#         # if input:
#         #     key = sys.stdin.read(1)
#             if key is not None:
#                 if key == 'w':
#                     speed += 1
#                 elif key == 's':
#                     speed -= 1
#                 elif key == 'a':
#                     left  = 1
#                 elif key == 'd':
#                     right = 1
#             print('{}m/s left{} right{}'.format(speed, left,right))
#         else:
#             left = 0
#             right = 0
#             print('{}m/s left{} right{}'.format(speed, left,right))
#         time.sleep(0.03)


# if __name__ == '__main__':
#     main()