import Tkinter as tk
from GlobalVariables import *

class ExperimentConstructionFrame(tk.Frame):
	""" The ExperimentConstructionFrame class uses canvas to visualize the entire experiment including all the contents inside the well(s) """
	def __init__(self, parent, master=None, **kwargs):
		tk.Frame.__init__(self, parent, **kwargs)

		# Specify hierarchy
		self.parent = parent # parent widget
		if master == None:
			self.master = parent # master is App unless specified otherwise
		else:
			self.master = master

		# Set the dimensions of the frame
		self.frame_width = 900
		self.frame_height = 700

		# Configure the dimensions of the frame
		self.config(width=self.frame_width, height=self.frame_height)

		# Start canvas
		self.canvas = tk.Canvas(self, bg="#54a3b4", width=self.frame_width, height=self.frame_height,
									highlightthickness=0, borderwidth=0)
		self.canvas.pack(fill="both", expand=True)

		# Offset
		self.offset = 10

		# Calculate what the length of the plate will be assuming that it will use all the frame width minus 2*offsets
		self.plate_length = self.frame_width-2*self.offset #px

		# Calculate scale (pixels per mm)
		self.pixel_per_mm = self.plate_length/(DIMENSIONS[parent.p_config]["Dimension"][0])
		print "There are %r pixels per mm" % self.pixel_per_mm

		# With scale, calculate the width of the plate (width of plate will be parallel to height of frame)
		self.plate_width = DIMENSIONS[parent.p_config]["Dimension"][1]*self.pixel_per_mm

		# Define the bbox of the plate frame
		self.plate_bbox = self.offset, self.offset, self.offset+self.plate_length, self.offset+self.plate_width

		# Draw the plate frame (rectangle)
		self.canvas.create_rectangle(self.plate_bbox,fill="#FFA0F0")

		# Draw wells
		self.well_offset = DIMENSIONS[parent.p_config]["A1 Offset"]
		self.well_offset[0] *= self.pixel_per_mm
		self.well_offset[1] *= self.pixel_per_mm
		print self.well_offset
		self.well_center = [self.offset+self.well_offset[1], self.offset+self.well_offset[0]]
		print self.well_center
		self.well_diameter = self.pixel_per_mm*DIMENSIONS[self.parent.p_config]["Well Diameter"]
		self.c_to_c = DIMENSIONS[parent.p_config]["Center-to-Center Spacing"]*self.pixel_per_mm

		for i in range(DIMENSIONS[parent.p_config]["Layout"][0]):
			for j in range(DIMENSIONS[parent.p_config]["Layout"][1]):
				self.well_bbox = [(j*self.c_to_c)+self.well_center[0]-(self.well_diameter/2), (i*self.c_to_c)+self.well_center[1]-(self.well_diameter/2), 
									(j*self.c_to_c)+self.well_center[0]+(self.well_diameter/2), (i*self.c_to_c)+self.well_center[1]+(self.well_diameter/2)]
				self.canvas.create_oval(self.well_bbox,fill="purple", tags="%s%i"%(ABC[i],j+1))
				print "%s%i" % (ABC[i],j+1)
				self.canvas.tag_bind("%s%i" % (ABC[i],j+1), '<Button-1>', lambda event, loc=[i,j]:self.selectWell(event, loc))

	########## Methods ##########
	def selectWell(self, event, loc):
		self.parent.sel_well_index = loc
		print "You selected me, well %r!" % self.parent.sel_well_index
		self.parent.layer_list_frame.sel_well_label.config(text="Selected well: %s%i" % (ABC[loc[0]],loc[1]+1))






if __name__ == "__main__":
	root = tk.Tk()
	ecf = ExperimentConstructionFrame(root)
	ecf.pack(fill="both", expand=True)
	root.mainloop()


