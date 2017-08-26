import os, sys, time
import tabors

sys.path.append(os.path.abspath("../"))
from kulka import Kulka
from random import randint

def main(addr):
    with Kulka(addr) as kulka:
        print("Connected to Sphero ", addr)
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
    main(tabors.kulkas[0])
