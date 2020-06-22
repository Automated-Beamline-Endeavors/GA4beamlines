#!/usr/bin/env python3

#This implementation of the Ackley function is intended to work with two or more variables.

print("I've been imported!")

import numpy as np

def AckleyFunc(x, lengthParam = 4.0, invert=False, trans=True, amp = 5.0):
	'''
	Parameters:
		x           :   Array/list of positioner values
		lengthParam :   scale length - needed to change the number of extrema
		invert      :   A boolean that determines whether the function performs
							normally or inverts the value.
		trans		:	A boolean that keeps the values of the function between
							0 and 1 when True.  Otherwise, usual values are calculated.
		amp			:	A float that is the relative amplitude between the exponential
							and sinusoidal parts of the function.
	'''
	d = 1 / len(x)
	value = None

	#part1 = -0.2 * np.sqrt(0.5 * np.sum(np.power(x, 2)))
	#part2 = 0.5 * np.sum(np.cos(np.multiply(x, 2.0 * np.pi / lengthParam)))
	part1 = -0.2 * np.sqrt(d * np.sum(np.power(x, 2)))
	part2 = d * np.sum(np.cos(np.multiply(x, 2.0 * np.pi / lengthParam)))

	if trans:
		value = (amp * np.exp(part1) + np.exp(part2) - np.e)/amp
	else:
		value = np.e + amp - amp * np.exp(part1) - np.exp(part2)

	if invert:
		value = -1 * value

	return value
