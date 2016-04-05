
from GlobalVariables import *

"""
CANVAS COORDINATE SYSTEM
(0,0)---------------------------------> +X
	|
	|
	|
	|
	|
	|
	|
	|
	|
	|
	|
	|
	|
	|
	V
	+Y


NEWMARK COORDINATE SYSTEM
+Y<---------------------------------(0,0)
										|
										|
										|
										|
										|
										|
										|
										|
										|
										|
										|
										|
										|
										|
										V
										+X


Below is a function that can transform frame coordinates to Newmark coordinates per the Newmark's current configuration

"""

def transform(x, y):
	len_x = len(x)
	len_y = len(y)
	x_list = []
	y_list = []
	for i in range(len_x):
		x_prime = y[i]
		y_prime = BUILD_LENGTH - x[i]
		x_list.append(x_prime)
		y_list.append(y_prime)
	return x_list,y_list

def inv_transform(x_prime, y_prime):
	len_x_prime = len(x_prime)
	len_y_prime = len(y_prime)
	x_list = []
	y_list = []
	for i in range(len(x_prime)):
		x = BUILD_LENGTH - y_prime[i]
		y = x_prime[i]
		x_list.append(x)
		y_list.append(y)
	return x_list,y_list

if __name__ == "__main__":
	pass




