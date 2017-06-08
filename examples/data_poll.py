import os
import sys
import time

sys.path.append(os.path.abspath("../"))

from kulka import Kulka
from random import randint

def parse_locator(data):
    data_list = []
    for kbyte in data[2]:
        data_list.append(kbyte)
        # print(type(kbyte))
    output = dict()
    output['xpos'] = 256*data_list[0] + data_list[1]
    output['ypos'] = 256*data_list[2] + data_list[3]
    output['xvel'] = 256*data_list[4] + data_list[5]
    output['yvel'] = 256*data_list[6] + data_list[7]
    for i, k in enumerate(output):
        # print(k, output[k])
        if output[k] > 32767:
            output[k] -= 65536
    output['sog'] = data_list[8] + data_list[9]
    return output

def main():
    addr = '68:86:E7:06:FD:1D'
    with Kulka(addr) as kulka:
        kulka.set_inactivity_timeout(300)
        for i in range(5):
            kulka.set_rgb(0, 0, 0xFF)
            time.sleep(0.1)
            kulka.set_rgb(0, 0, 0)
            time.sleep(0.1)
            kulka.set_rgb(0xFF, 0, 0)
            direction = input('What direction?\n')
            if int(direction) == -1:
                break
            speed = input('What speed?\n')
            kulka.roll(int(speed), int(direction))
            for i in range(10):
                kulka.read_locator()
                data = kulka.data_poll()
                # print("Raw output:\n", data[2])
                output = parse_locator(data)
                print(output)
        kulka.sleep()


if __name__ == '__main__':
    main()
