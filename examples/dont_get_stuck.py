'''
A simple script to keep Sphero rolling
'''
import os, sys, time 
import numpy as np
import tabors
from random import randint

sys.path.append(os.path.abspath("../"))
from kulka import Kulka
from data_poll import parse_locator

def get_current_coords(kulka):
    kulka.read_locator()
    data = kulka.data_poll()
    output = parse_locator(data)
    coords = (output['xpos'], output['ypos'])
    return coords

def distance_from_point(kulka, point = (0, 0)):
    kulka.read_locator()
    data = kulka.data_poll()
    output = parse_locator(data)
    distance = ((output['xpos'] - point[0])**2 +\
                (output['ypos'] - point[1])**2)**0.5
    return distance

def roll_until_stuck(kulka, direction, speed = 50):
    point_i = get_current_coords(kulka)
    kulka.roll(speed, direction)
    time.sleep(2)
    distance_travelled = distance_from_point(kulka, point_i)
    while distance_travelled >= 10:
        point_i = get_current_coords(kulka)
        kulka.roll(speed, direction)
        time.sleep(2)
        distance_travelled = distance_from_point(kulka, point_i)
    
def main(addr, limit = 10, max_distance = 100, speed = 50):
    print("Connecting to Sphero at ", addr)
    with Kulka(addr) as kulka:
        kulka.set_inactivity_timeout(300)
        t0 = time.time()
        t1 = time.time()
        steps = 0
        direction = 0
        while (t1 - t0) < limit * 60:
            print("Step ", steps)
            steps += 1
            roll_until_stuck(kulka, direction)
            time.sleep(0.1)
            direction = randint(0, 359)
            t1 = time.time()
        kulka.close()

if __name__ == '__main__':
    main(tabors.kulkas[0])
