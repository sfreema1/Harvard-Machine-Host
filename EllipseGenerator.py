import math
from matplotlib import pyplot as plt

""" 
A Note: The following algorith to generate conics is derived from projective geometry.
There are point conics and line conics.

Ex:

Ellipse: 
a-radius = 2
b-radius = 1

BBox = 4 X 4 centered at the origin
The horizontal of the bbox is split into 10 division (11 points)
The vertical of the bbox is split into 20 divison (21 points)

The ellipse is drawn by finding the intersection point of two lines, which we will call U and V.

U is a line which always passes through (a,0), and whose other point starts at (a,a) moves the top, left, and bottom
sides of the bbox in a CCW fashion 

V is a line which always passes through (-a,0) and whose other point starts at (a,0) and along the right, top, 
bottom sides (and back up the right side to finish) CCW and ends back at (a,0)



"""

def make_ellipse(center, dim, sections):
	center_x = center[0] 	# in mm
	center_y = center[1]	# in mm
	dim_x = dim[0]			# in mm
	dim_y = dim[1]	 		# in mm

	n = sections

	a = float(dim_x/2)		# x axes radius
	b = float(dim_y/2)		# y axes radius

	del_x = a/n
	del_y = b/n

	x_list = []
	y_list = []

	start_x = -a
	start_y = 0

	# Calculate the point perpective
	x_c = start_x
	y_c = start_y

	h_x_list = []
	h_y_list = []

	v_x_list = []
	v_y_list = []

	for i in range(n-1):
		x_c += del_x
		y_c += del_y

		# Append to h_lists
		h_x_list.append(x_c)
		h_y_list.append(0)

		# Append to v_lists
		v_x_list.append(-a)
		v_y_list.append(y_c)

	# Calculate the points of the ellipse/circle
	# h_list lines are calculated to all pass through (0,-b)
	# v_list lines are calculated to all pass through (0,b)

	h_m = []
	h_b = []
	v_m = []
	v_b = []

	for i in range(n-1):
		m1, b1 = calculate_line(h_x_list[i], h_y_list[i], 0, -b)
		m2, b2 = calculate_line(v_x_list[i], v_y_list[i], 0, b)
		new_x, new_y = get_intersection(m1, b1, m2, b2)
		x_list.append(new_x)
		y_list.append(new_y)



	return [x_list, y_list]
	
	
def calculate_line(x1, y1, x2, y2):
	""" Calculate the slope """
	try:
		m = float((y2 - y1))/(x2-x1)
	except(ZeroDivisionError):
		print "Error: Division by zero"
		return None

	b = y1-m*x1

	return [m,b]

def get_intersection(m1, b1,m2 ,b2):
	if m1 == m2:
		print "Error: Division by zero."
		return
	x = -1*float(b1-b2)/(m1-m2)
	y = -(-b2*m1 + b1*m2)/(m1-m2)

	return [x,y]

if __name__ == "__main__":

	result = make_ellipse([0,0],[10,10],50)
	x3 = result[0]
	y3 = result[1]

	plt.scatter(x3,y3,color="green")
	plt.show()



