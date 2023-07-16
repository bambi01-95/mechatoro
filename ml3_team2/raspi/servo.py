import RPi.GPIO as GPIO
import sys
import tty
import termios
 
# サーボモータ1の制御に使用するGPIOピン番号
servo1_pin = 18
 
# サーボモータ2の制御に使用するGPIOピン番号
servo2_pin = 19
 
# サーボモータの最小角度と最大角度（調整が必要な場合は適宜変更してください）
min_angle = 40
max_angle = 180
 
# サーボモータの初期角度
initial_angle1 = 110
initial_angle2 = 110

# サーボモータの増減角度
step_angle = 0.5
 
# 初期化
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)
 
# PWMインスタンスを作成
pwm1 = GPIO.PWM(servo1_pin, 50)  # サーボモータ1のPWM周波数を50Hzに設定
pwm2 = GPIO.PWM(servo2_pin, 50)  # サーボモータ2のPWM周波数を50Hzに設定
pwm1.start(0)  # PWM出力を開始
pwm2.start(0)  # PWM出力を開始
 
# サーボモータ1を指定した角度に移動する関数
def move_servo1(angle):
    angle = max(min(angle, max_angle), min_angle)  # 角度を上限と下限の範囲内に制限
    duty_cycle = (angle / 18) + 2  # デューティ比を計算
    pwm1.ChangeDutyCycle(duty_cycle)
 
# サーボモータ2を指定した角度に移動する関数
def move_servo2(angle):
    angle = max(min(angle, max_angle), min_angle)  # 角度を上限と下限の範囲内に制限
    duty_cycle = (angle / 18) + 2  # デューティ比を計算
    pwm2.ChangeDutyCycle(duty_cycle)
 
# キーボード入力の取得
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
 
try:
    # サーボモータの初期状態
    move_servo1(initial_angle1)
    move_servo2(initial_angle2)
    print("2つのサーボモータを個別に制御します。")
    print("a: サーボモータ1の角度を増やす")
    print("d: サーボモータ1の角度を減らす")
    print("j: サーボモータ2の角度を増やす")
    print("l: サーボモータ2の角度を減らす")
    print("q: 終了")
 
    while True:
        command = getch()
 
        if command == 'q':
            break
        elif command == 'a':  # aキー
            initial_angle1 = min(initial_angle1 + step_angle, max_angle)
            move_servo1(initial_angle1)
        elif command == 'd':  # dキー
            initial_angle1 = max(initial_angle1 - step_angle, min_angle)
            move_servo1(initial_angle1)
            
        elif command == 'j':  # jキー
            initial_angle2 = min(initial_angle2 + step_angle, max_angle)
            move_servo2(initial_angle2)
        elif command == 'l':  # lキー
            initial_angle2 = max(initial_angle2 - step_angle, min_angle)
            move_servo2(initial_angle2)
 
except KeyboardInterrupt:
    pass
 
# プログラムの終了時にクリーンアップ
pwm1.stop()
pwm2.stop()
GPIO.cleanup()