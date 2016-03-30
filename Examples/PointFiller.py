import math as m

"""
class Solver(object):
	docstring for Solver
	def __init__(self, seed, increment):
		super(Solver, self).__init__()
		
		self.increment = increment
		self.seed_x = seed[0]
		self.seed_y = seed[1]
		self.x_list = [self.seed_x]
		self.y_list = [self.seed_y]

		self.new_point = Point(self,[self.seed_x,self.seed_y])
"""

class Point(object):
	"""docstring for Point"""
	def __init__(self, coordinates, increment, solver=None):
		super(Point, self).__init__()
		
		self.increment = increment
		self.x = coordinates[0]
		self.y = coordinates[1]
		self.neighbors_x = []
		self.neighbors_y = []

		self._find_neighbors()

	def _find_neighbors(self):

		while len(self.neighbors_x) < 1 and len(self.neighbors_y) < 1:
			if len(self.neighbors_x) == 0:
				new_x = self.x+self.increment
				new_y = self.y
				self.neighbors_x.append(new_x)
				self.neighbors_y.append(new_y)

			if len(self.neighbors_x) == 1:
				dx = self.neighbors_x[0]-self.x 
				dy = self.neighbors_y[0]-self.y
				d = m.sqrt(dx**2 + dy**2)
				


	def _print_neighbors(self):
		print self.neighbors_x, self.neighbors_y





start_x = 0
start_y = 1

point = Point([start_x,start_y],1)
point._print_neighbors()