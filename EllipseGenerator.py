import math
from matplotlib import pyplot as plt

def make_ellipse(center, dim, resolution):
	center_x = center[0] 	# in mm
	center_y = center[1]	# in mm
	dim_x = dim[0]			# in mm
	dim_y = dim[1]	 		# in mm
	x_list = []
	y_list = []

	res = resolution 		# in microns
	res_mm = res/1000. 		# in mm

	a = dim_x/2.			# x-axis radius
	b = dim_y/2.			# y-axis radius

	while a>=0 and b>=0:
		start_x = a + center_x	# in mm
		start_y = 0 + center_y	# in mm

		x_list += [start_x]
		y_list += [start_y]

		r_eff = (a+b)/2 		# average of the two radii

		circum_eff = 2*math.pi*r_eff
		n = int(round(circum_eff/res_mm))
		if n == 0:
			break
		del_theta = 2*math.pi/n

		if (b-res_mm) < 0:
			x_c = -a + center_x
			k = a/res_mm  
			for j in range(2*int(k)-1):
				x_c += res_mm
				x_list.append(x_c)
				y_list.append(center_y)
			break

		if (a-res_mm) < 0:
			y_c = -b + center_y
			k = b/res_mm  
			for j in range(2*int(k)-1):
				y_c += res_mm
				x_list.append(center_x)
				y_list.append(y_c)
			break

		theta_c = 0
		for i in range(n-1):
			theta_c += del_theta
			new_x = a*math.cos(theta_c) + center_x
			new_y = b*math.sin(theta_c) + center_y
			x_list.append(new_x)
			y_list.append(new_y)

		a -= res_mm
		b -= res_mm

	return x_list, y_list


if __name__ == "__main__":

	r = make_ellipse([10,14], [3,10], 200)
	plt.scatter(r[0],r[1],color="red")
	plt.plot(r[0],r[1],color="black")
	plt.show()
