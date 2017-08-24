'''
A simple script to keep Sphero rolling, and within a certain distance 
of the start point
'''

import os, sys, time 
import numpy as np
from random import randint

sys.path.append(os.path.abspath("../"))
from kulka import Kulka
from data_poll import parse_locator

def distance_from_point(kulka, point = (0, 0)):
	kulka.read_locator()
	data = kulka.data_poll()
	output = parse_locator(data)
	distance = ((output['xpos'] - point[0])**2 +\
				(output['ypos'] - point[1])**2)**0.5
	return distance

def taxicab_homing(kulka, threshold = 3):
	distance = distance_from_point(kulka)
	while distance > threshold:
		speed = 30
		kulka.read_locator()
		data = kulka.data_poll()
		output = parse_locator(data)
		print(output)
		if abs(output['xpos']) > abs(output['ypos']):
			if output['xpos'] > 0:
				direction = 270
			elif output['xpos'] < 0:
				direction = 90
		else:
			if output['ypos'] > 0:
				direction = 180
			elif output['ypos'] < 0:
				direction = 0
		kulka.roll(speed, direction)
		time.sleep(3)
		distance = distance_from_point(kulka)
	print("In range of home")
    
def main(i = 1, limit = 1, max_distance = 100, speed = 50):
	addrs = [
	'68:86:E7:06:FD:1D',
	'68:86:E7:07:07:6B',
	'68:86:E7:08:0E:DF']
	print("Connecting to Sphero", i)
	with Kulka(addrs[i]) as kulka:
		kulka.set_inactivity_timeout(300)
		t0 = time.time()
		t1 = time.time()
		print("Moving to random position")
		for _ in range(3):
			direction = randint(0, 359)
			kulka.roll(speed, direction)
		while ((t1 - t0) < limit * 60):
			time.sleep(3)
			distance = distance_from_point(kulka)
			# print(steps, distance)
			if distance > 100: 
				print("outside range, rolling home")
				taxicab_homing(kulka)
				break
			kulka.roll(speed, direction)	
			t1 = time.time()
	kulka.close()

if __name__ == '__main__':
    main()
