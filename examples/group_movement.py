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

def align_zeros(addrs, kulkas = []):
	def test_offset(kulka):
		happy = False
		kulka.roll(50, 0)
		time.sleep(1)
		kulka.roll(0, 0)
		offset_est = int(input("Enter offset estimate:"))
		kulka.roll(50, offset_est)
		happy_str = input("Happy with offset?\n")
		if happy_str != "y":
   			test_offset(kulka)
		else:
			return offset_est

	addr = addrs.pop()
	with Kulka(addr) as kulka:
		kulkas.append(kulka)
		print("Sphero " + str(len(kulkas)) + " online")
		kulka.set_inactivity_timeout(30)
		kulka.set_rgb(0xFF, 0, 0)
		if len(addrs) > 0: 
			align_zeros(addrs, kulkas)
		else:
			offsets = []
			for kulka in kulkas:
				offsets.append(test_offset(kulka))
			return (offsets, kulkas)

def move_as_group(addrs):
	offsets, kulkas = align_zeros(addrs)
	direction = input()
	while direction != "x":
		if direction == "w":
			angle = 0
		elif direction == "a":
			angle = 90
		elif direction == "s":
			angle = 180
		elif direction == "d":
			angle = 270
		for i, kulka in enumerate(kulkas):
			kulka.roll(50, angle + offsets[i])


def main(i = 1, limit = 1, max_distance = 100, speed = 50):
	addrs = [
	'68:86:E7:06:FD:1D',
	'68:86:E7:07:07:6B',
	'68:86:E7:08:0E:DF']
	move_as_group(addrs)

if __name__ == '__main__':
    main()
