import Tkinter as tk
from GlobalVariables import *

class ExperimentFrame(tk.Frame):
	""" The ExperimentFrame class uses canvas to visualize the entire experiment including all the contents inside the well(s) """
	def __init__(self, parent, master=None, **kwargs):
		tk.Frame.__init__(self, parent, **kwargs)
		# Specify hierarchy - IMPORTANT TO DO FIRST
		self.parent = parent # parent widget
		if master == None:
			self.master = parent
		else:
			self.master = master
		# ===================== WINDOW VARIABLES ===================== #
		self.tags_list = []		# Stores tags bound to wells
		# ========== IMPORTED VARIABLES ========== #
		# Get well/print surface type
		self.b_config = self.master.b_config	# Print build config
		# ========== FRAME PARAMETERS ========== #
		# Set the dimensions of the frame
		self.width = 660
		self.height = 510
		# ==================== CLASS INITILIZATION ==================== #
		# ========== FRAME CONFIGURATION ========== #
		# Configure the dimensions of the frame
		self.config(width=self.width, height=self.height)
		# ========== WELL PLATE INITIALIZATION ========== #
		# Create the plate
		self.well_plate = WellPlate(self,self.master)
		self.well_plate.config(bg=EXP_BG, width=self.width, height=self.height, highlightthickness=0, borderwidth=0)
		self.well_plate.pack(fill="both", expand=True)
		
		# Add wells
		for row in range(self.well_plate.num_rows):
			for col in range(self.well_plate.num_cols):
				self.well = Well(self.well_plate, [row,col])
				self.tags_list.append(self.well.tag)

		print self.tags_list

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

		# ========== IMPORTED VARIABLES ========== #
		self.frame_width = parent.width 		# px
		self.frame_height = parent.height		# px
		self.b_type = self.master.b_config 		# Kind of build surface (well or glass or dish etc)
		self.num_rows = self.master.p_row
		self.num_cols = self.master.p_col

		# ========== WELL PLATE PARAMETERS ========== #
		self.tag = "Plate"
		self.layout = [self.num_rows, self.num_cols]
		self.c_offset = 25 									# Offset padding between the well plate and the frame
		self.text_offset = 8
		self.length = self.frame_width-2*self.c_offset								# px
		self.pixel_per_mm = self.length/(DIMENSIONS[self.b_type]["Dimension"][0]) 	# (scale) px per mm
		self.mm_per_pixel = (DIMENSIONS[self.b_type]["Dimension"][0])/self.length 	# (scale) mm per px
		self.width = DIMENSIONS[self.b_type]["Dimension"][1]*self.pixel_per_mm			# px
		self.c_to_c = DIMENSIONS[self.b_type]["Center-to-Center Spacing"]*self.pixel_per_mm		# px

		# A1 offsets is a two element list:
		# First element is distance from top of plate to center of first well (Y-displacement)
		# Second element is distance from left side of plate to center of first well (X-displacement)
		# That gave a lot of confusion
		self.A1_offset = DIMENSIONS[self.b_type]["A1 Offset"] # in mm
		self.A1_offset[0] *= self.pixel_per_mm				# Convert to px
		self.A1_offset[1] *= self.pixel_per_mm				# Convert to px

		self.bbox = [self.c_offset, self.c_offset, self.c_offset+self.length, self.c_offset+self.width] # px coordinates
		self.start_x = self.c_offset
		self.start_y = self.c_offset
		self.end_x = self.c_offset+self.length
		self.end_y = self.c_offset+self.width

		# Well label placement
		self.w_label_coord = [self.text_offset,self.frame_height-self.text_offset]

		# XY display placement
		self.xy_label_coord = [self.frame_width-self.text_offset, self.frame_height-self.text_offset]
		self.bind("<Motion>", self.show_coordinates)

		# Draw itself
		self.create_rectangle(self.bbox,fill=PLATE_BG,tags=self.tag)

		# Draw well label
		self.w_label = self.create_text(self.w_label_coord,text="Build surface: %s"%self.b_type, anchor="sw",fill="black")

		# Draw coordinate display
		self.xy_label = self.create_text(self.xy_label_coord,text="Coord: (X = ? mm, Y = ? mm)", anchor="se", fill="black")

		# ========== CLASS METHODS ========== #
	def show_coordinates(self, event=None):
		x_coord = self.mm_per_pixel*(event.x-self.c_offset)
		y_coord = self.mm_per_pixel*(event.y-self.c_offset)
		self.itemconfigure(self.xy_label, text="Coord: (X = %.3f mm, Y = %.3f mm)" % (x_coord, y_coord))

	def deselect_all_wells(self,event=None):
		tags_list = self.parent.tags_list
		num_tags = len(tags_list)
		for i in range(num_tags):
			self.itemconfig(tags_list[i],fill=WELL_COLOR)

	def select_well(self, event, loc):
		self.master.sel_ind = loc
		self.master.layer_list_frame.sel_well_label.config(text="Selected well: %s%i" % (ABC[loc[0]],loc[1]+1))
		self.master.layer_list_frame.update_listbox()
		self.deselect_all_wells()
		self.itemconfig("Well%s%i"%(ABC[loc[0]],loc[1]+1),fill=SEL_WELL_COLOR)


class Well(object):
	""" The Well class is a single instance of the a well located on the plate. """
	def __init__(self, well_plate, location):
		super(Well, self).__init__()

		# ========== IMPORTED VARIABLES ========== #
		self.well_plate = well_plate
		self.A1_offset = well_plate.A1_offset		# Was converted to px by the WellPlate object
		self.scale = well_plate.pixel_per_mm
		self.well_type = well_plate.b_type
		self.c_offset = well_plate.c_offset
		self.c_to_c = well_plate.c_to_c

		# ========== WELL PARAMETERS ========== #
		self.row_loc = location[0]
		self.col_loc = location[1]
		self.tag = "Well%s%i"%(ABC[self.row_loc], self.col_loc+1)
		self.diameter = self.scale*DIMENSIONS[self.well_type]["Well Diameter"]				# px
		self.center_x = self.c_offset+self.A1_offset[1]+self.c_to_c*self.col_loc			# px
		self.center_y = self.c_offset+self.A1_offset[0]+self.c_to_c*self.row_loc			# px

		self.bbox = [self.center_x-self.diameter/2, self.center_y-self.diameter/2, self.center_x+self.diameter/2, self.center_y+self.diameter/2]

		# Draw itself
		well_plate.create_oval(self.bbox,fill=WELL_COLOR,tags=self.tag,activefill=ACT_WELL_COLOR)
		well_plate.tag_bind(self.tag, '<Button-1>', lambda event, loc=[self.row_loc,self.col_loc]:well_plate.select_well(event,loc))

		
		


""""
class WellPlate(object):
	The WellPlate calculates the geometry parameters for a well plate and displays it.
	def __init__(self, master, canvas, frame_width, frame_height, offset, type_):
		super(WellPlate, self).__init__()

		# Draw the wells
		self.well_center = [self.offset+self.well_offset[1], self.offset+self.well_offset[0]]
		self.well_diameter = self.pixel_per_mm*DIMENSIONS[type_]["Well Diameter"]
		self.c_to_c = DIMENSIONS[type_]["Center-to-Center Spacing"]*self.pixel_per_mm

		for i in range(DIMENSIONS[type_]["Layout"][0]):
			for j in range(DIMENSIONS[type_]["Layout"][1]):
				self.well_bbox = [(j*self.c_to_c)+self.well_center[0]-(self.well_diameter/2), (i*self.c_to_c)+self.well_center[1]-(self.well_diameter/2), 
									(j*self.c_to_c)+self.well_center[0]+(self.well_diameter/2), (i*self.c_to_c)+self.well_center[1]+(self.well_diameter/2)]
				
				self.canvas.create_oval(self.well_bbox,fill=WELL_COLOR, tags="%s%i"%(ABC[i],j+1))
				self.canvas.itemconfig("%s%i"%(ABC[i],j+1), activefill=ACT_WELL_COLOR)
				self.canvas.tag_bind("%s%i" % (ABC[i],j+1), '<Button-1>', lambda event, loc=[i,j]:self.master.selectWell(event, loc))
"""


if __name__ == "__main__":
	root = tk.Tk()
	ef = ExperimentFrame(root)
	ef.pack(fill="both", expand=True)
	root.mainloop()


