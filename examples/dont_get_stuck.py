'''
A simple script to keep Sphero rolling, and within a certain distance 
of the start point
'''

import os, sys, time 
import numpy as np
from random import randint

sys.path.append(os.path.abspath("../"))
from kulka import Kulka

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

def main(i = 0, limit = 0.5, max_distance = 100, speed = 50):
    # with open('mykulka.txt') as file_:
    #     addr = file_.readline().strip()
    addrs = [
    '68:86:E7:06:FD:1D',
    '68:86:E7:07:07:6B',
    '68:86:E7:08:0E:DF']
    #
    print("Connecting to Sphero", i)
    with Kulka(addrs[i]) as kulka:
        kulka.set_inactivity_timeout(300)
        t0 = time.time()
        t1 = time.time()
        steps = 0
        last_direction = 0
        homing = False
        while (t1 - t0) < limit * 60:
            print("-Step ", steps)
            steps += 1
            kulka.read_locator()
            data = kulka.data_poll()
            output = parse_locator(data)
            distance = (output['xpos']**2 + output['ypos']**2)**0.5
            if distance >= max_distance:
                print("Outside limit, homing")
                homing = True
            if homing == True:
                direction = (180 + int(np.arctan(output['ypos']/output['xpos']) * np.pi/180)) % 360
                if distance < 10:
                    print("In range of home, resuming exploration")
                    homing == False
            else:
                dir_base = randint(0, 5)
                direction = dir_base * 60
            last_direction = direction  
            kulka.roll(speed, direction)
            print(speed, direction)
            while speed >= 10:
                kulka.read_locator()
                data = kulka.data_poll()
                # print("Raw output:\n", data[2])
                output = parse_locator(data)
                speed_reading = output['sog']
                distance = (output['xpos']**2 + output['ypos']**2)**0.5
                # print(output)
                print("Current speed:", speed_reading)
                print("Current distance:", distance)
                time.sleep(3/20)
            t1 = time.time()
            time.sleep(0.1)
    
        kulka.close()

if __name__ == '__main__':
    main()
