import math
#from matplotlib import pyplot as plt

# make sure you give center and dim as type float

def make_rectangle(center, dim, resolution):
	center_x = center[0] 	# in mm
	center_y = center[1]	# in mm
	dim_x = dim[0]			# in mm
	dim_y = dim[1]	 		# in mm

	res = resolution 		# in microns
	res_mm = res/1000. 		# in mm

	start_x = center_x-(dim_x/2)	# in mm
	start_y = center_y-(dim_y/2)	# in mm


	x_droplets = int(round(1000.*dim_x/res))	# num of droplets on the horizontal edge of the rectangle
	y_droplets = int(round(1000.*dim_y/res))	# num of droplets on the vertical edge of the rectangle

	north = y_droplets
	east = x_droplets
	south = y_droplets
	west = x_droplets-1

	x_c = float(start_x) 	# current droplet x-coordinate
	y_c = float(start_y)	# current droplet y-coordinate

	x_list = [x_c]			# add the starting point to the x_list
	y_list = [y_c]			# add the starting point to the y_list

	last_dir_travelled = 0 # initial step=0 north=1, east=2, south=3, west=4

	if (x_droplets == 0 and y_droplets == 0):
		return [x_list, y_list]

	elif y_droplets == 0:
		for e in range(east):
				x_c += (res_mm) 
				# y_c does not change
				# append the new values
				x_list.append(x_c)
				y_list.append(y_c)
		last_dir_travelled = 2 # traveled east last
		return [x_list, y_list]

	elif x_droplets == 0:
		for n in range(north):
				# x_c does not change
				y_c += (res_mm)
				# append the new values
				x_list.append(x_c)
				y_list.append(y_c)
		last_dir_travelled = 1 # traveled north last
		return [x_list, y_list]


	"""
	There are several cases that will occur when giving dimensions and a desired resolution

	1. The number of droplets in the N and E direction are both 0. 
		a. This is a single droplet. Print the initial coordinate and return. 
			Ex: Dimension = 0.1 mm X 0.1 mm with resolution 500 microns

	2. The number of droplets initially in the N direction is 0 and in the E direction is greater than 0.
		a. Only the print the droplets in the E direction. There is no need to print in the S or W direction.
			The one drop put down initially in the N direction is now just the first in the E direction.
			Just print in the E direction and return.
			Ex: Dimension = 3.0 mm X 0.1 mm with resolution of 300 microns

	3. The number of droplets initially in the N direction is greater than 0 and in the E direction is 0.
		a. Only print the droplets in the N direction. There is no need to print in the E, S, or W direction.
			Just print the N direction and return.
			Ex: Dimension = 0.1 mm X 3.0 mm with resolution of 300 microns

	Each time you make a new inner rectangle, you must subtract 2X the resolution from both dimensions. If 10
	droplets are calculated for the initial northward move, that is actually 11 droplets that compose that northward
	trip. Each cycle first adds the initial step northward, and the remaining steps in the northward direction
	are 2 less than the last trip. The algorithm needs to account for different even and odd starting droplets for 
	both initial x and y droplets

	4. The number of droplets initially in the E direction is greater than the number of droplets in the N.
		Both are non-zero. The initial droplet array is even number by odd number.
		a. 
	"""

	#print "After adding the fist step, the first rectangle will be %r->>%r->>%r->>%r"%(north,east,south,west)

	for i in range(int(math.ceil(y_droplets/2.))):
		for n in range(north):
			# x_c does not change
			y_c += (res_mm)
			# append the new values
			x_list.append(x_c)
			y_list.append(y_c)
		last_dir_travelled = 1
		#print "Last traveled north"

		for e in range(east):
			x_c += (res_mm) 
			# y_c does not change
			# append the new values
			x_list.append(x_c)
			y_list.append(y_c)
		last_dir_travelled = 2
		#print "Last traveled east"

		for s in range(south):
			# x_c does not change
			y_c -= (res_mm)
			# append the new values
			x_list.append(x_c)
			y_list.append(y_c)
		last_dir_travelled = 3
		#print "Last traveled south"

		for w in range(west):
			x_c -= (res_mm) 
			# y_c does not change
			# append the new values
			x_list.append(x_c)
			y_list.append(y_c)
		last_dir_travelled = 4
		#print "Last traveled west"

		if (north-2) >= 0:
			# x_c does not change
			y_c += (res_mm)
			# append the new values
			x_list.append(x_c)
			y_list.append(y_c)
			last_dir_travelled = 0
			#print "Took first step north to begin next inner rectangle"
				
		north -= 2
		east -= 2
		south -= 2
		west -= 2

		#print "After adding the first step, the next rectangle will be %r->>%r->>%r->>%r"%(north,east,south,west)
		#print "Round %i complete!"%(i+1)

		if (north == 0 or east == 0):
			#print "Detected a possible end condition"
			if north == 0 and last_dir_travelled == 0:
				print 
				for e in range(east):
					x_c += (res_mm) 
					# y_c does not change
					# append the new values
					x_list.append(x_c)
					y_list.append(y_c)
					last_dir_travelled = 2

	return [x_list, y_list]

if __name__ == "__main__":
	# ========= Droplet array cases ========== #
	# Even X Even Case X > Y
	# result = make_rectangle([0,0],[1.7,1.1],100)
	# Even X Odd Case X > Y
	# result = make_rectangle([0,0],[1.7,1],100)
	# Odd X Even Case X > Y
	# result = make_rectangle([0,0],[1.8,0.9],100)
	# Odd X Odd Case X > Y
	# result = make_rectangle([0,0],[1.8,1],100)

	# Even X Even Case X < Y
	#result = make_rectangle([0,0],[1.1,1.7],100)
	# Even X Odd Case X < Y
	#result = make_rectangle([0,0],[1.1,1.8],100)
	# Odd X Even Case X < Y
	#result = make_rectangle([0,0],[1.,1.7],100)
	# Odd X Odd Case X < Y
	#result = make_rectangle([0,0],[1.,1.8],100)

	# Even X Even X == Y
	result = make_rectangle([5,3.234], [0.9,0.9],100)
	# Odd X Odd X == Y
	#result = make_rectangle([0,0], [1,1],100)
	x_result = result[0]
	y_result = result[1]

	plt.plot(x_result,y_result,label="Print")
	plt.scatter(x_result,y_result,label="Print")
	plt.show()