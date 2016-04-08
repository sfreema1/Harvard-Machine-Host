import Tkinter as tk
import ttk
from GlobalVariables import *

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
