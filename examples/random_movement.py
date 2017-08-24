import os, sys, time

sys.path.append(os.path.abspath("../"))
from kulka import Kulka
from random import randint

def main(i = 0):
    addrs = [
    '68:86:E7:06:FD:1D',
    '68:86:E7:07:07:6B',
    '68:86:E7:08:0E:DF']
    with Kulka(addrs[i]) as kulka:
        print("Connected to Sphero ", i)
        kulka.set_inactivity_timeout(300)
        for _ in range(6):
            speed = randint(30, 100)
            direction = randint(0, 359)
            print("Rolling")
            print(speed, direction)
            kulka.roll(speed, direction)
            time.sleep(5)
        kulka.sleep()

if __name__ == '__main__':
    main(i = 1)
