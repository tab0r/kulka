import os
import sys
import time

sys.path.append(os.path.abspath("../"))


from kulka import Kulka
from itertools import repeat
from random import randint
import time


def main(i = 0):
    # with open('mykulka.txt') as file_:
    #     addr = file_.readline().strip()
    addrs = [
    '68:86:E7:07:07:6B',
    '68:86:E7:06:FD:1D',
    '68:86:E7:08:0E:DF']
    #
    with Kulka(addrs[i]) as kulka:
        kulka.set_inactivity_timeout(3600)
    
        for _ in repeat(None, 6):
            kulka.roll(randint(30, 100), randint(0, 359))
            time.sleep(5)
    
        kulka.sleep()


    # with Kulka(ADDR0) as kulka0:
    #     print("Sphero 0 online")
    #     with Kulka(ADDR1) as kulka1:
    #         print("Sphero 1 online")
    #         with Kulka(ADDR2) as kulka2:
    #             print("Sphero 2 online")
    #             kulka0.set_inactivity_timeout(3600)
    #             kulka1.set_inactivity_timeout(3600)
    #             kulka2.set_inactivity_timeout(3600)

    #             for _ in repeat(None, 600):
    #                 kulka0.roll(randint(30, 100), randint(0, 359))
    #                 kulka1.roll(randint(30, 100), randint(0, 359))
    #                 kulka2.roll(randint(30, 100), randint(0, 359))
    #                 time.sleep(1)

    #             kulka0.sleep()
    #             kulka1.sleep()
    #             kulka2.sleep()


if __name__ == '__main__':
    main()
