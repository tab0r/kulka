import os
import sys
import time

sys.path.append(os.path.abspath("../"))

from kulka import Kulka
from random import randint

def main():
    addr = '68:86:E7:08:0E:DF'
    with Kulka(addr) as kulka:
        kulka.set_inactivity_timeout(300)
        kulka.set_streaming()
        for i in range(10):
            kulka.set_rgb(0, 0, 0xFF)
            time.sleep(0.1)
            kulka.set_rgb(0, 0, 0)
            time.sleep(0.1)
            kulka.set_rgb(0xFF, 0, 0)
            # kulka._connection.recv(1024)
            print(kulka._recv_buffer)

            time.sleep(1)

        kulka.sleep()


if __name__ == '__main__':
    main()
