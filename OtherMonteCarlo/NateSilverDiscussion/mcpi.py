#!/usr/bin/env python

from random import random

DARTS=1000000
hits = 0
throws = 0
for i in range (1, DARTS):
	throws += 1
	x = random()
	y = random()
	dist = x*x+y*y
	if dist <= 1.0:
		hits = hits + 1.0

# hits / throws = 1/4 Pi
pi = 4 * (hits / throws)

print "pi = %s" %(pi)
