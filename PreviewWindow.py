import Tkinter as tk
import ttk

class PreviewWindow(tk.Toplevel):
	""" The PreviewWindow class is used to display the desired pattern in the well. """
	def __init__(self, parent, master=None, **settings):
		tk.Toplevel.__init__(self, parent)
		# Set any bindings for keyboard shortcuts
		self.bind('<Return>', self.close_preview)

		# Specify hierarchy
		self.parent = parent # parent widget
		if master == None:
			self.master = parent
		else:
			self.master = master

		self.grab_set()

		# Initialize Preview Window
		self.init_window() # Not sure how I feel about this function - might remove it

		# Initialize Canvas and backdrop elements for drawing
		self.init_canvas_backdrop()

		##### Start drawing shape to be printed
		# Load variable dictionary imported from LayerWindow
		# Channel
		# Diameter
		# Horizontal Alignment
		# Layer Name
		# Pattern
		# Resolution
		# Vertical Alignment
		# X Dimension
		# X Placement
		# Y Dimension
		# Y Placement

		self.shape_label = settings["Pattern"].get()
		if self.shape_label == "Rectangle":
			self.shape = Rectangle(self.px_per_mm, self.center, self.well_diameter, [settings["X Dimension"].get(),settings["Y Dimension"].get()], 
																					[settings["X Placement"].get(),settings["Y Placement"].get()],
																					settings["Horizontal Alignment"].get(), 
																					settings["Vertical Alignment"].get())
			self.canvas.create_rectangle(self.shape.shape_coord, fill="blue")

		if self.shape_label == "Ellipse":
			self.shape = Ellipse(self.px_per_mm, self.center, self.well_diameter, [settings["X Dimension"].get(),settings["Y Dimension"].get()], 
																					[settings["X Placement"].get(),settings["Y Placement"].get()],
																					settings["Horizontal Alignment"].get(), 
																					settings["Vertical Alignment"].get())
			self.canvas.create_oval(self.shape.shape_coord, fill="blue")


	########## Methods ##########
	def init_window(self):
		# Initialize the LayerBuildWindow
		self.resizable(0,0) # Make the window non-resizable
		self.grab_set()
		self.title("Preview well")

		# Set parameters for window size
		self.wm_width = 700
		self.wm_height = 700
		self.center = [self.wm_width/2, self.wm_height/2]

		# Set size of PreviewWindow
		self.geometry("%dx%d" % (self.wm_width, self.wm_height))

	def init_canvas_backdrop(self):
		# Canvas frame
		self.canvasFrame = tk.Frame(self, padx=0, pady=0)
		self.canvasFrame.pack(fill="both", expand=True)

		# Drawn well frame dimensions
		self.offset = 25
		self.frame_coord = self.offset, self.offset, self.wm_width-self.offset, self.wm_height-self.offset

		# Start coordinate for all drawings
		self.start_coord = self.offset, self.offset

		# Calculate scaling
		self.well_diameter = 34.8 # mm
		self.px_per_mm = (self.frame_coord[3]-self.frame_coord[0])/self.well_diameter
		self.mm_per_px = self.well_diameter/(self.frame_coord[3]-self.frame_coord[0])

		# Start Canvas
		self.canvas = tk.Canvas(self.canvasFrame, bg="#54a3b4", width=self.wm_width, height=self.wm_height,
									highlightthickness=0, borderwidth=0)
		self.canvas.pack(fill="both", expand=True)

		# Draw well
		self.well = self.canvas.create_oval(self.frame_coord,fill="grey")

		# Draw text instructions
		self.text_offset = 8
		self.text_coord = self.text_offset, self.wm_height-self.text_offset
		self.text_instruct = self.canvas.create_text(self.text_coord, text="Press 'Return' to exit preview", anchor="sw")

		# Draw XY coordinates
		self.text_xy_coord = self.wm_width-self.text_offset, self.wm_height-self.text_offset
		self.text_xy = self.canvas.create_text(self.text_xy_coord, text="Coord: (X = , Y = )", anchor="se")
		self.canvas.bind("<Motion>", self.show_coordinates)

		# Draw well type
		self.text_well_size = "35 mm"
		self.text_well_size_coord = self.text_offset, self.text_offset
		self.text_well_type = self.canvas.create_text(self.text_well_size_coord, text="Well type: %s" % self.text_well_size, anchor="nw")

	def show_coordinates(self, event=None):
		x_coord = self.mm_per_px*(event.x-(self.wm_width/2.0))
		y_coord = self.mm_per_px*(event.y-(self.wm_height/2.0))
		self.canvas.itemconfigure(self.text_xy, text="Coord: (X = %.3f mm, Y = %.3f mm)" % (x_coord, y_coord))

	def close_preview(self,event=None):
		self.destroy()


class Rectangle(object):
	""" The Rectangle class represents the geometric objects of rectangles and squares """
	def __init__(self, scale, center, well_diameter, dim, offset, horiz_align, vert_align):
		super(Rectangle, self).__init__()

		self.scale = scale						# pixels per mm
		print "There are %r pixels per mm in the object " % self.scale
		self.well_center_x = center[0]		# x coordinate of well center (px)
		self.well_center_y = center[1]		# y coordinate of well center (px)
		print "The center's x-coord is %r and its y-coord is %r" % (self.well_center_x, self.well_center_y)
		self.well_diameter = well_diameter		# diameter of well mm
		print "The well's diameter is %r mm" % self.well_diameter

		self.name = "Rectangle"					# Name of shape
		self.horiz_align = horiz_align			# -1=left, 0=center, 1=right
		self.vert_align = vert_align			# -1=botton, 0=middle, 1=top
		print "The alignment configuration is (%r, %r)" % (self.horiz_align, self.vert_align)

		self.x_offset = offset[0]				# mm
		self.y_offset = offset[0]				# mm
		self.x_dim = dim[0]						# mm
		self.y_dim = dim[1]						# mm
		print "The shape will have dimensions %r mm X %r mm and offset by %r mm and %r mm" % (self.x_dim, self.y_dim, self.x_offset, self.y_offset)

		# Calculate the center of the shape
		# X pixel coordinate
		self.shape_center_x = self.well_center_x+(self.horiz_align*(self.well_diameter*self.scale/4))
		# Y pixel coordinates
		self.shape_center_y = self.well_center_y+(self.vert_align*(self.well_diameter*self.scale/4))
		print "The desired shape center is at x coord %r and y coord %r" % (self.shape_center_x, self.shape_center_y)
		# Shift the center of the shape by offsets
		self.shape_center_x += self.x_offset*self.scale
		self.shape_center_y += self.y_offset*self.scale
		print "The offset shifts the shape center to x coord %r and y coord %r" % (self.shape_center_x, self.shape_center_y)

		# Calculate the start and end coordinates for the rectangle
		self.start_x = self.shape_center_x-(self.x_dim*self.scale/2)
		self.start_y = self.shape_center_y-(self.y_dim*self.scale/2)
		self.end_x = self.shape_center_x+(self.x_dim*self.scale/2)
		self.end_y = self.shape_center_y+(self.y_dim*self.scale/2)

		# Compose shape bbox coordinates
		self.shape_coord = self.start_x, self.start_y, self.end_x, self.end_y
		print self.shape_coord


class Ellipse(object):
	""" The Ellipse class represents the geometric objects of ellipses and circles """
	def __init__(self, scale, center, well_diameter, dim, offset, horiz_align, vert_align):
		super(Ellipse, self).__init__()

		self.scale = scale						# pixels per mm
		print "There are %r pixels per mm in the object " % self.scale
		self.well_center_x = center[0]		# x coordinate of well center (px)
		self.well_center_y = center[1]		# y coordinate of well center (px)
		print "The center's x-coord is %r and its y-coord is %r" % (self.well_center_x, self.well_center_y)
		self.well_diameter = well_diameter		# diameter of well mm
		print "The well's diameter is %r mm" % self.well_diameter

		self.name = "Ellipse"					# Name of shape
		self.horiz_align = horiz_align			# -1=left, 0=center, 1=right
		self.vert_align = vert_align			# -1=botton, 0=middle, 1=top
		print "The alignment configuration is (%r, %r)" % (self.horiz_align, self.vert_align)

		self.x_offset = offset[0]				# mm
		self.y_offset = offset[0]				# mm
		self.x_dim = dim[0]						# mm
		self.y_dim = dim[1]						# mm
		print "The shape will have dimensions %r mm X %r mm and offset by %r mm and %r mm" % (self.x_dim, self.y_dim, self.x_offset, self.y_offset)

		# Calculate the center of the shape
		# X pixel coordinate
		self.shape_center_x = self.well_center_x+(self.horiz_align*(self.well_diameter*self.scale/4))
		# Y pixel coordinates
		self.shape_center_y = self.well_center_y+(self.vert_align*(self.well_diameter*self.scale/4))
		print "The desired shape center is at x coord %r and y coord %r" % (self.shape_center_x, self.shape_center_y)
		# Shift the center of the shape by offsets
		self.shape_center_x += self.x_offset*self.scale
		self.shape_center_y += self.y_offset*self.scale
		print "The offset shifts the shape center to x coord %r and y coord %r" % (self.shape_center_x, self.shape_center_y)

		# Calculate the start and end coordinates for the rectangle
		self.start_x = self.shape_center_x-(self.x_dim*self.scale/2)
		self.start_y = self.shape_center_y-(self.y_dim*self.scale/2)
		self.end_x = self.shape_center_x+(self.x_dim*self.scale/2)
		self.end_y = self.shape_center_y+(self.y_dim*self.scale/2)

		# Compose shape bbox coordinates
		self.shape_coord = self.start_x, self.start_y, self.end_x, self.end_y
		print self.shape_coord


		


if __name__ == "__main__":

	root = tk.Tk()
	pw = PreviewWindow(root)
	root.mainloop()

