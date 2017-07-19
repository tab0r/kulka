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

def roll_until_stuck(kulka, direction = None, speed = 50):
    if direction == None: direction = randint(0, 359)
    kulka.roll(speed, direction)
    kulka.read_locator()
    data = kulka.data_poll()
    output = parse_locator(data)
    speed_reading = output['sog']
    while speed_reading >= speed/20:
        kulka.roll(speed, direction)
        kulka.read_locator()
        data = kulka.data_poll()
        output = parse_locator(data)
        speed_reading = output['sog']
        distance = (output['xpos']**2 + output['ypos']**2)**0.5
        print(speed_reading, distance, output['xpos'], output['ypos'])
        time.sleep(3/20)

def distance_from_point(kulka, point = (0, 0)):
	kulka.read_locator()
	data = kulka.data_poll()
	output = parse_locator(data)
	distance = ((output['xpos'] - point[0])**2 +\
				(output['ypos'] - point[1])**2)**0.5
	return distance

def taxicab_homing(kulka, threshold = 10, speed = 20):
	# find our way home using the right hand rule
	kulka.read_locator()
	data = kulka.data_poll()
	output = parse_locator(data)
	speed_reading = output['sog']
	distance = (output['xpos']**2 + output['ypos']**2)**0.5
	while distance > threshold:
		if output['xpos'] > threshold**0.5:
			direction = 270
		elif output['xpos'] < -threshold**0.5:
			direction = 90
		elif output['ypos'] > threshold**0.5:
			direction = 180
		elif output['ypos'] < -threshold**0.5:
			direction = 0
		else:
			speed = 0
			direction = 0
		kulka.roll(speed, direction)
		kulka.read_locator()
		data = kulka.data_poll()
		output = parse_locator(data)
		distance = (output['xpos']**2 + output['ypos']**2)**0.5
	print("In range of home")

def roll_to_home_bad(kulka, threshold = 10, speed = 50):
    # find our way home using the right hand rule
    kulka.read_locator()
    data = kulka.data_poll()
    # print("Raw output:\n", data[2])
    output = parse_locator(data)
    speed_reading = output['sog']
    distance = (output['xpos']**2 + output['ypos']**2)**0.5
    direction = (180 + int(np.arctan(output['ypos']/output['xpos'] * np.pi/180))) % 360
    while distance > threshold:
        # kulka.roll(speed, (direction + 90)%360)
        # roll_until_stuck(kulka, direction, speed)
        kulka.roll(speed, direction)
        kulka.read_locator()
        data = kulka.data_poll()
        output = parse_locator(data)
        distance = (output['xpos']**2 + output['ypos']**2)**0.5
        direction = (180 + int(np.arctan2(output['ypos'], output['xpos']) * np.pi/180)) % 360
    print("In range of home")
    
def main(i = 0, limit = 10, max_distance = 100, speed = 50):
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
		print("Moving to random position")
		direction = randint(0, 359)
		# roll_until_stuck(kulka, direction)
		kulka.roll(speed, direction)
		while ((t1 - t0) < limit * 60):
			steps += 1
			time.sleep(0.1)
			distance = distance_from_point(kulka)
			print(steps, distance)
			if distance > 100: 
				print("outside range, rolling home")
				taxicab_homing(kulka)
				break
			t1 = time.time()
	kulka.close()

if __name__ == '__main__':
    main()
