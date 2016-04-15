import Tkinter as tk
import ttk
from GlobalVariables import *

class WellPlate(tk.Canvas):
	""" The WellPlate class represents the well plate"""
	def __init__(self, parent, master=None, **kwargs):
		tk.Canvas.__init__(self, parent, **kwargs)
		# Specify hierarchy - IMPORTANT TO DO FIRST
		self.parent = parent # parent widget
		if master == None:
			self.master = parent
		else:
			self.master = master

		self.tags_list = []		# Stores tags bound to wells
		# ========== IMPORTED VARIABLES ========== #
		self.frame_width = parent.width 		# px
		self.frame_height = parent.height		# p

		# ========== WELL PLATE PARAMETERS ========== #
		self.c_offset = 25 									# Offset padding between the well plate and the frame
		self.text_offset = 8
		self.tag = "Plate"

		self.calculate_dimensions()
		self.draw()


		# ========== CLASS METHODS ========== #
	def show_coordinates(self, event=None):
		x_coord = self.mm_per_pixel*(event.x-self.c_offset)
		y_coord = self.mm_per_pixel*(event.y-self.c_offset)
		self.itemconfigure(self.xy_label, text="Coord: (X = %.3f mm, Y = %.3f mm)" % (x_coord, y_coord))

	def deselect_all_wells(self,event=None):
		tags_list = self.tags_list
		num_tags = len(tags_list)
		for i in range(num_tags):
			self.itemconfig(tags_list[i],fill=WELL_COLOR)

	def select_well(self, event, loc):
		self.master.sel_ind = loc
		self.master.layer_list_frame.sel_well_label.config(text="Selected well: %s%i" % (ABC[loc[0]],loc[1]+1))
		self.master.layer_list_frame.update_listbox()
		self.deselect_all_wells()
		self.itemconfig("Well%s%i"%(ABC[loc[0]],loc[1]+1),fill=SEL_WELL_COLOR)

	def draw(self):
		# Well label placement
		self.w_label_coord = [self.text_offset,self.frame_height-self.text_offset]
		# XY display placement
		self.xy_label_coord = [self.frame_width-self.text_offset, self.frame_height-self.text_offset]
		self.bind("<Motion>", self.show_coordinates)
		# Draw itself
		self.create_rectangle(self.bbox,fill=PLATE_BG,tags=self.tag)
		# Draw well label
		self.w_label = self.create_text(self.w_label_coord,text="Build surface: %s"%self.b_config, anchor="sw",fill="black")
		# Draw coordinate display
		self.xy_label = self.create_text(self.xy_label_coord,text="Coord: (X = ? mm, Y = ? mm)", anchor="se", fill="black")
		# Add wells
		for row in range(self.num_rows):
			for col in range(self.num_cols):
				self.well = Well(self, [row,col])
				self.tags_list.append(self.well.tag)

	def calculate_dimensions(self):
		self.b_config = self.master.b_config 		# Kind of build surface (well or glass or dish etc)
		self.num_rows = self.master.p_row
		self.num_cols = self.master.p_col
		self.layout = [self.num_rows, self.num_cols]
		self.length = self.frame_width-2*self.c_offset								# px
		self.pixel_per_mm = self.length/(DIMENSIONS[self.b_config]["Dimension"][0]) 	# (scale) px per mm
		self.mm_per_pixel = (DIMENSIONS[self.b_config]["Dimension"][0])/self.length 	# (scale) mm per px
		self.width = DIMENSIONS[self.b_config]["Dimension"][1]*self.pixel_per_mm			# px
		self.c_to_c = DIMENSIONS[self.b_config]["Center-to-Center Spacing"]*self.pixel_per_mm		# px

		# A1 offsets is a two element list:
		# First element is distance from top of plate to center of first well (Y-displacement)
		# Second element is distance from left side of plate to center of first well (X-displacement)
		# That gave a lot of confusion
		self.A1_offset_x = DIMENSIONS[self.b_config]["A1 Offset"][1] # in mm
		self.A1_offset_y = DIMENSIONS[self.b_config]["A1 Offset"][0] # in mm
		self.A1_offset_x *= self.pixel_per_mm				# Convert to px
		self.A1_offset_y *= self.pixel_per_mm				# Convert to px
		
		self.bbox = [self.c_offset, self.c_offset, self.c_offset+self.length, self.c_offset+self.width] # px coordinates
		self.start_x = self.c_offset
		self.start_y = self.c_offset
		self.end_x = self.c_offset+self.length
		self.end_y = self.c_offset+self.width

	def redraw(self):
		self.tags_list = []		# create new tags list
		self.calculate_dimensions()
		self.draw()



class Well(object):
	""" The Well class is a single instance of the a well located on the plate. """
	def __init__(self, well_plate, location):
		super(Well, self).__init__()

		# ========== IMPORTED VARIABLES ========== #
		self.well_plate = well_plate
		self.A1_offset_x = well_plate.A1_offset_x		# Was converted to px by the WellPlate object
		self.A1_offset_y = well_plate.A1_offset_y		# Was converted to px by the WellPlate object
		self.scale = well_plate.pixel_per_mm
		self.well_type = well_plate.b_config
		self.c_offset = well_plate.c_offset
		self.c_to_c = well_plate.c_to_c

		# ========== WELL PARAMETERS ========== #
		self.row_loc = location[0]
		self.col_loc = location[1]
		self.tag = "Well%s%i"%(ABC[self.row_loc], self.col_loc+1)
		self.diameter = self.scale*DIMENSIONS[self.well_type]["Well Diameter"]			# px
		self.center_x = self.c_offset+self.A1_offset_x+self.c_to_c*self.col_loc			# px
		self.center_y = self.c_offset+self.A1_offset_y+self.c_to_c*self.row_loc			# px

		self.bbox = [self.center_x-self.diameter/2, self.center_y-self.diameter/2, self.center_x+self.diameter/2, self.center_y+self.diameter/2]

		# Draw itself
		well_plate.create_oval(self.bbox,fill=WELL_COLOR,tags=self.tag,activefill=ACT_WELL_COLOR)
		well_plate.tag_bind(self.tag, '<Button-1>', lambda event, loc=[self.row_loc,self.col_loc]:well_plate.select_well(event,loc))

		

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
		self.b_config = self.master.b_config 		# Kind of build surface (well or glass or dish etc)
		# Delimits the draw area
		self.bbox = [self.c_offset, self.c_offset, self.parent.w_width-self.c_offset, self.parent.w_height-self.c_offset]
		self.diameter = DIMENSIONS[self.b_config]["Well Diameter"]
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
		self.label = self.create_text(self.label_coord, text="Print Build Surface: %s" % self.b_config, anchor="nw", fill=TEXT_PREVIEW_COLOR)
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
