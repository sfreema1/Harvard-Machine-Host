import Tkinter as tk
import ttk
from GlobalVariables import *

class PreviewWindow(tk.Toplevel):
	""" The PreviewWindow class is used to display the desired pattern in the well. """
	def __init__(self, parent, master=None, **settings):
		tk.Toplevel.__init__(self, parent)
		# Specify hierarchy - IMPORTANT TO DO FIRST
		self.parent = parent # parent widget
		if master == None:
			self.master = parent
		else:
			self.master = master
		# ===================== WINDOW VARIABLES ===================== #
		self.tags_list = []		# Could be used later to target specific shapes drawn to the canvas
		# ========== IMPORTED VARIABLES ========= #
		# Get current row and column plate selection
		self.cur_row = self.master.sel_ind[0] 	# row in plate
		self.cur_col = self.master.sel_ind[1]	# column in plate
		# Get well/print surface type
		self.b_config = self.master.b_config	# Print build config
		self.prev_vars = settings

		# ========== FRAME PARAMETERS ========== #
		self.name = "Preview well" 								# Text that appears in at the top of the app
		self.w_width = 700										# Pixel width of main Tk window
		self.w_height = 700										# Pixel height of main Tk window
		self.w_center_x = self.w_width/2
		self.w_center_y = self.w_height/2
		self.w_center = [self.w_center_x, self.w_center_y]
		self.w_x_offset = (self.master.scr_width-self.w_width)/2	# Pixel x offset for the Tk window
		self.w_y_offset = (self.master.scr_height-self.w_height)/2	# Pixel y offset for the Tk window

		# ==================== CLASS INITILIZATION ==================== #
		# ========== TOPLEVEL WINDOW CONFIGURATION ========== #
		self.wm_title(self.name)
		self.geometry("%dx%d+%d+%d" % (self.w_width, self.w_height, self.w_x_offset, self.w_y_offset))
		self.resizable(width=False,height=False)

		# ========== CANVAS CONFIGURATION ========== #
		# Start CanvasWell a.k.a. tk.Canvas in disguise preconfigured with a well, and coordinate display
		self.canvas_well = CanvasWell(self,self.master)
		self.canvas_well.pack(fill="both", expand=True)

		# ========== DRAW SHAPES =========== #
		self.draw()

	def draw(self):
		row = self.cur_row
		col = self.cur_col
		num_layer = len(self.master.exp[row][col])
		# First draw any previous created layers in the well
		if num_layer > 0:
			for layer in range(num_layer):
				# Quick reference variables to pass to the CanvasShape object
				layer_vars = self.master.exp[row][col][layer]
				dim = [layer_vars["X Dimension"].get(), layer_vars["Y Dimension"].get()]
				offset = [layer_vars["X Placement"].get(), layer_vars["Y Placement"].get()]
				horiz_align = layer_vars["Horizontal Alignment"].get()
				vert_align = layer_vars["Vertical Alignment"].get()

				if layer_vars["Pattern"].get() == "Rectangle":
					shape = CanvasRectangle(self.canvas_well, dim, offset, horiz_align, vert_align,layer)
					self.tags_list.append(shape.tag)
				elif layer_vars["Pattern"].get() == "Ellipse":
					shape = CanvasEllipse(self.canvas_well, dim, offset, horiz_align, vert_align,layer)
					self.tags_list.append(shape.tag)

		# Then draw the PreviewWindow Shape
		dim = [self.prev_vars["X Dimension"].get(), self.prev_vars["Y Dimension"].get()]
		offset = [self.prev_vars["X Placement"].get(), self.prev_vars["Y Placement"].get()]
		horiz_align = self.prev_vars["Horizontal Alignment"].get()
		vert_align = self.prev_vars["Vertical Alignment"].get()

		if self.prev_vars["Pattern"].get() == "Rectangle":
			shape = CanvasRectangle(self.canvas_well, dim, offset, horiz_align, vert_align)
			self.tags_list.append(shape.tag)
		elif self.prev_vars["Pattern"].get() == "Ellipse":
			shape = CanvasEllipse(self.canvas_well, dim, offset, horiz_align, vert_align)
			self.tags_list.append(shape.tag)

		print self.tags_list


class CanvasWell(tk.Canvas):
	""" The CanvasWell class represents the well where everything is drawn inside """
	def __init__(self, parent, master=None, **kwargs):
		tk.Canvas.__init__(self, parent, **kwargs)
		# Specify hierarchy - IMPORTANT TO DO FIRST
		self.parent = parent # parent widget
		if master == None:
			self.master = parent
		else:
			self.master = master

		# ========== CANVAS PARAMETERS ========== #
		self.c_offset = 25						# Adds some spacing between the edge of the canvas and where items are draw
		self.text_offset = 8 					# Adds some spacing beween the edge of the canvas and where text is placed
		self.b_type = self.master.b_config 		# Kind of build surface (well or glass or dish etc)
		# Delimits the draw area
		self.bbox = [self.c_offset, self.c_offset, self.parent.w_width-self.c_offset, self.parent.w_height-self.c_offset]
		self.diameter = DIMENSIONS[self.b_type]["Well Diameter"]
		self.center_x = self.parent.w_center_x
		self.center_y = self.parent.w_center_y
		self.center = self.parent.w_center
		# Scaling
		self.px_per_mm = (self.bbox[3]-self.bbox[0])/self.diameter
		self.mm_per_px = self.diameter/(self.bbox[3]-self.bbox[0])
		# Label placement
		self.label_coord = [self.text_offset, self.text_offset]
		# XY display placement
		self.xy_label_coord = [self.parent.w_width-self.text_offset, self.parent.w_height-self.text_offset]
		
		# ========== CANVAS WELL INITIALIZATION ========== #
		self.config(bg=PLATE_BG, width=self.parent.w_width, height=self.parent.w_height, highlightthickness=0, borderwidth=0)
		self.bind("<Motion>", self.show_coordinates)
		# Draw itself (The well)
		self.well = self.create_oval(self.bbox,fill=WELL_COLOR)
		# Draw label for build type
		self.label = self.create_text(self.label_coord, text="Print Build Surface: %s" % self.b_type, anchor="nw", fill=TEXT_PREVIEW_COLOR)
		# Draw coordinate display
		self.xy_label = self.create_text(self.xy_label_coord,text="Coord: (X = ? mm, Y = ? mm)", anchor="se", fill=TEXT_PREVIEW_COLOR)

		# ========== CLASS METHODS ========== #
	def show_coordinates(self, event=None):
		x_coord = self.mm_per_px*(event.x-(self.parent.w_width/2.0))
		y_coord = self.mm_per_px*(event.y-(self.parent.w_height/2.0))
		self.itemconfigure(self.xy_label, text="Coord: (X = %.3f mm, Y = %.3f mm)" % (x_coord, y_coord))


class CanvasRectangle(object):
	""" The Rectangle class represents the geometric objects of rectangles and squares """
	def __init__(self, canvas_well, dim, offset, horiz_align, vert_align, layer=None):
		super(CanvasRectangle, self).__init__()
		# ========== IMPORTED VARIABLES ========== #
		self.canvas = canvas_well
		self.well_center_x = canvas_well.center[0]		# x coordinate of well center (px)
		self.well_center_y = canvas_well.center[1]		# y coordinate of well center (px)
		self.well_diameter = canvas_well.diameter		# diameter of well mm
		self.scale = canvas_well.px_per_mm 				# Conversion from mm to pixels

		# ========= SHAPE PARAMETERS ========== #
		self.name = "Rectangle"					# Name of shape

		if layer is not None:
			self.tag = "Layer%s" % (layer+1) 	# Define a tag to be bound to the shape if it is an already set layer from the layer list
			self.label = (layer+1)
		else:
			self.tag = "Preview"				# Otherwise, tag the shape as preview since it has not been yet added to the list
			self.label = self.tag

		self.horiz_align = horiz_align			# -1=left, 0=center, 1=right
		self.vert_align = vert_align			# -1=botton, 0=middle, 1=top
		self.x_offset = offset[0]				# X-offset in mm
		self.y_offset = offset[1]				# Y-offset in mm
		self.x_dim = dim[0]						# X-dimension in mm
		self.y_dim = dim[1]						# Y-dimension in mm
		# Calculate the center of the shape
		# X pixel coordinate
		self.center_x = self.well_center_x+(self.horiz_align*(self.well_diameter*self.scale/4))
		self.center_x += self.x_offset*self.scale
		# Y pixel coordinates
		self.center_y = self.well_center_y+(self.vert_align*(self.well_diameter*self.scale/4))
		self.center_y += self.y_offset*self.scale
		self.center = [self.center_x,self.center_y]
		# Calculate the start and end coordinates for the rectangle
		self.start_x = self.center_x-(self.x_dim*self.scale/2)
		self.start_y = self.center_y-(self.y_dim*self.scale/2)
		self.end_x = self.center_x+(self.x_dim*self.scale/2)
		self.end_y = self.center_y+(self.y_dim*self.scale/2)
		# Compose shape bbox coordinates
		self.bbox = [self.start_x, self.start_y, self.end_x, self.end_y]
		# Draw itself and its label
		canvas_well.create_rectangle(self.bbox,fill="blue",tags=self.tag)
		canvas_well.create_text(self.center,text=self.label, fill=TEXT_PREVIEW_COLOR)


class CanvasEllipse(object):
	""" The Ellipse class represents the geometric objects of ellipses and circles """
	def __init__(self, canvas_well, dim, offset, horiz_align, vert_align, layer=None):
		super(CanvasEllipse, self).__init__()
		# ========== IMPORTED VARIABLES ========== #
		self.canvas = canvas_well
		self.well_center_x = canvas_well.center[0]		# x coordinate of well center (px)
		self.well_center_y = canvas_well.center[1]		# y coordinate of well center (px)
		self.well_diameter = canvas_well.diameter		# diameter of well mm
		self.scale = canvas_well.px_per_mm 				# Conversion from mm to pixels

		# ========= SHAPE PARAMETERS ========== #
		self.name = "Ellipse"					# Name of shape

		if layer is not None:
			self.tag = "Layer%s" % (layer+1) 	# Define a tag to be bound to the shape if it is an already set layer from the layer list
			self.label = (layer+1)
		else:
			self.tag = "Preview"				# Otherwise, tag the shape as preview since it has not been yet added to the list
			self.label = self.tag

		self.horiz_align = horiz_align			# -1=left, 0=center, 1=right
		self.vert_align = vert_align			# -1=botton, 0=middle, 1=top
		self.x_offset = offset[0]				# X-offset in mm
		self.y_offset = offset[1]				# Y- offset in mm
		self.x_dim = dim[0]						# X-dimension in mm
		self.y_dim = dim[1]						# Y-dimension in mm
		# Calculate the center of the shape
		# X pixel coordinate
		self.center_x = self.well_center_x+(self.horiz_align*(self.well_diameter*self.scale/4))
		self.center_x += self.x_offset*self.scale
		# Y pixel coordinates
		self.center_y = self.well_center_y+(self.vert_align*(self.well_diameter*self.scale/4))
		self.center_y += self.y_offset*self.scale
		self.center = [self.center_x,self.center_y]
		# Calculate the start and end coordinates for the rectangle
		self.start_x = self.center_x-(self.x_dim*self.scale/2)
		self.start_y = self.center_y-(self.y_dim*self.scale/2)
		self.end_x = self.center_x+(self.x_dim*self.scale/2)
		self.end_y = self.center_y+(self.y_dim*self.scale/2)
		# Compose shape bbox coordinates
		self.bbox = [self.start_x, self.start_y, self.end_x, self.end_y]
		# Draw itself and its label
		canvas_well.create_oval(self.bbox,fill="blue",tags=self.tag)
		canvas_well.create_text(self.center,text=self.label, fill=TEXT_PREVIEW_COLOR)

if __name__ == "__main__":

	root = tk.Tk()
	pw = PreviewWindow(root)
	root.mainloop()
