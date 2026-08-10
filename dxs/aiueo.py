import random
import time

moji = ['あ', 'い', 'う', 'え', 'お', 'か', 'き', 'く'
, 'け', 'こ']

def select_moji(mojilist):
    return random.choice(mojilist)

while True:
    result = select_moji(moji)
    print(result)
    time.sleep(3)
