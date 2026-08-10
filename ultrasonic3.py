import RPi.GPIO as GPIO
import time
import sys
import csv
from datetime import datetime

trig_pin = 15                           # GPIO 15
echo_pin = 14                           # GPIO 14
speed_of_sound = 34370                  # 20℃での音速(cm/s)

GPIO.setmode(GPIO.BCM)                  # GPIOをBCMモードで使用
GPIO.setwarnings(False)                 # BPIO警告無効化
GPIO.setup(trig_pin, GPIO.OUT)          # Trigピン出力モード設定
GPIO.setup(echo_pin, GPIO.IN)           # Echoピン入力モード設定

def get_distance():
    #Trigピンを10μsだけHIGHにして超音波の発信開始
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.000010)
    GPIO.output(trig_pin, GPIO.LOW)

    while not GPIO.input(echo_pin):
        pass
    t1 = time.time() # 超音波発信時刻（EchoピンがHIGHになった時刻）格納

    while GPIO.input(echo_pin):
        pass
    t2 = time.time() # 超音波受信時刻（EchoピンがLOWになった時刻）格納

    return (t2 - t1) * speed_of_sound / 2 # 時間差から対象物までの距離計算


MAX_COUNT = 720
INTERVAL = 1 / 6

ans = input('計測を開始しますか？ [Y/n]: ')
if ans.strip().upper() != 'Y':
    print('キャンセルしました。')
    GPIO.cleanup()
    sys.exit()

with open('distance_log.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp', 'distance_cm'])

    print(f'計測開始（{MAX_COUNT}回、{INTERVAL}秒間隔）')
    count = 0
    buffer = []
    try:
        while count < MAX_COUNT:
            distance = get_distance()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            writer.writerow([timestamp, '{:.2f}'.format(distance)])
            f.flush()
            count += 1
            buffer.append(f'{distance:.2f}')
            if len(buffer) == 6:
                print(f'[{count:>3}/{MAX_COUNT}] {" | ".join(buffer)} cm')
                buffer = []
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        pass

    finally:
        GPIO.cleanup()
        print(f'計測終了（{count}回記録）')
