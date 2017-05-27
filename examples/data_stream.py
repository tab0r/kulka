import os
import sys
import time

sys.path.append(os.path.abspath("../"))

from kulka import Kulka
from random import randint

def main():
    addr = '68:86:E7:06:FD:1D'
    with Kulka(addr) as kulka:
        kulka.set_inactivity_timeout(3600)

        for _ in range(10):
            kulka.set_rgb(0, 0xFF, 0)
            time.sleep(0.1)
            kulka.set_rgb(0, 0, 0)
            time.sleep(0.1)
            kulka.roll(10, 0)
            kulka.read_locator()
            data_list = []
            for kbyte in kulka.data_stream()[2]:
                data_list.append(kbyte)
                #print(int.from_bytes(kbyte, byteorder='big'))
            print(data_list)
        kulka.sleep()


if __name__ == '__main__':
    main()
