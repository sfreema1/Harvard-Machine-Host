import Tkinter as tk
from GlobalVariables import * 
import math

class FreeformFrame(tk.Toplevel):
	""" The FreeformFrame class creates a window for the selection of exact droplet placement for printing. """
	def __init__(self, parent, master=None, **settings):
		tk.Toplevel.__init__(self, parent)
		# Specify hierarchy - IMPORTANT TO DO FIRST
		self.parent = parent # parent widget
		if master == None:
			self.master = parent
		else:
			self.master = master
		# ============ IMPORTED VARIABLES =========== #
		if settings:
			self.settings = settings
			self.res = self.settings["Resolution"].get()
			self.dim_x = self.settings["X Dimension"].get()
			self.dim_y = self.settings["Y Dimension"].get()
		else:
			self.res = 200 # microns
			self.dim_x = 10 # mm
			self.dim_y = 10 # mm
		self.c_offset = 30		# Px - Adds some spacing between the edge of the canvas and where items are draw
		self.text_offset = 8 	# Px - Adds some spacing beween the edge of the canvas and where text is placed
		# ===================== WINDOW VARIABLES ===================== #
		self.tags_list = []		# Could be used later to target specific shapes drawn to the canvas
		# ========= FRAME PARAMETERS ========= #
		self.name = "Freeform Selection"					# Text that appears at the top of the window
		self.w_width = 700										# Pixel width of main Tk window
		self.w_height = 700										# Pixel height of main Tk window
		self.w_center_x = self.w_width/2					# px coordinate (x) of center of window
		self.w_center_y = self.w_height/2					# px coordinate (y) of center of window
		self.w_x_offset = 100# (self.master.scr_width-self.w_width)/2	# Pixel x offset for the Tk window.
		self.w_y_offset = 100# (self.master.scr_height-self.w_height)/2	# Pixel y offset for the Tk window.
		# ========== CHANNEL BUTTON SPACING ========== #
		self.buttons_x = int(math.ceil(1000.*self.dim_x/(self.res)))
		self.buttons_y = int(math.ceil(1000.*self.dim_y/(self.res)))
		self.selected = {}

		# ==================== CLASS INITIALIZATION ==================== #
		# ========== TOPLEVEL WINDOW =========== #
		self.wm_title(self.name)
		self.geometry("%dx%d+%d+%d" % (self.w_width, self.w_height, self.w_x_offset, self.w_y_offset))
		self.resizable(width=False,height=False)

		# ========== CANVAS CONFIGURATION ========== #
		# Start CanvasWell a.k.a. tk.Canvas in disguise preconfigured with buttons for selection
		self.freeform_space = FreeformCanvas(self,self.master)
		self.freeform_space.pack(fill="both", expand=True)

		# Draw channel buttons
		for col in range(self.buttons_x):
			for row in range(self.buttons_y):
				self.channel_button = ChannelButton(self.freeform_space,col,row)


class FreeformCanvas(tk.Canvas):
	""" The FreeformCanvas represents the freeform selection space """
	def __init__(self, parent, master=None, **kwargs):
		tk.Canvas.__init__(self, parent, **kwargs)
		# Specify hierarchy - IMPORTANT TO DO FIRST
		self.parent = parent # parent widget
		if master == None:
			self.master = parent
		else:
			self.master = master
		# ========== CANVAS PARAMETERS ========== #
		self.c_offset = parent.c_offset		# Adds some spacing between the edge of the canvas and where items are draw
		self.text_offset = parent.text_offset 	# Adds some spacing beween the edge of the canvas and where text is placed
		# Delimints the draw area
		self.bbox = [self.c_offset, self.c_offset, self.parent.w_width-self.c_offset, self.parent.w_height-self.c_offset]
		self.center_x = self.parent.w_center_x
		self.center_y = self.parent.w_center_y
		self.start_x = self.c_offset
		self.start_y = self.c_offset

		# TEST PARAMETERS
		self.res = parent.res # microns
		self.dim_x = parent.dim_x # mm
		self.dim_y = parent.dim_y # mm

		# Calculate the pixel scale
		self.px_per_mm = (self.bbox[2]-self.bbox[0])/(self.dim_x) # pixels per mm
		self.mm_per_px = self.px_per_mm **-1
		# Label placement
		self.label_coord = [self.text_offset, self.text_offset]
		# XY display placement
		self.xy_label_coord = [self.parent.w_width-self.text_offset, self.parent.w_height-self.text_offset]
		
		# ========== CANVAS WELL INITIALIZATION ========== #
		self.config(bg=PLATE_BG, width=self.parent.w_width, height=self.parent.w_height, highlightthickness=0, borderwidth=0)
		self.bind("<Motion>", self.show_coordinates)
		# Draw label for build type
		self.label = self.create_text(self.label_coord, text="Freeform Selection", anchor="nw", fill=TEXT_PREVIEW_COLOR)
		# Draw coordinate display
		self.xy_label = self.create_text(self.xy_label_coord,text="Coord: (X = ? mm, Y = ? mm)", anchor="se", fill=TEXT_PREVIEW_COLOR)

	def show_coordinates(self, event=None):
		x_coord = self.mm_per_px*(event.x-(self.parent.w_width/2.0))
		y_coord = self.mm_per_px*(event.y-(self.parent.w_height/2.0))
		self.itemconfigure(self.xy_label, text="Coord: (X = %.3f mm, Y = %.3f mm)" % (x_coord, y_coord))



class ChannelButton(object):
	def __init__(self, freeform_canvas, x, y):
		super(ChannelButton, self).__init__()
		# ========== IMPORTED VARIABLES ========== #
		self.canvas = freeform_canvas
		self.scale = freeform_canvas.px_per_mm
		
		# ========= CANVAS BUTTON PARAMETERS ========= #
		self.x = x # x index (column)
		self.y = y # y index (row) 
		self.res = freeform_canvas.res 			# in microns
		self.c_offset = freeform_canvas.c_offset
		self.c_width = freeform_canvas.dim_x	
		self.c_height = freeform_canvas.dim_y
		self.name = "%i,%i" % (self.x,self.y)
		self.scale = freeform_canvas.px_per_mm
		self.channel_select = 0 # color
		# Unselected: #FFFFFF (White)
		# Channel 1: #DE0600 (Red)
		# Channel 2: #032F95 (Blue)
		# Channel 3: #09B400 (Green)
		# Channel 4: #FFA100 (Orange)
		# Center-to-center spacing between channel buttons
		self.c_to_c = self.scale*self.res/1000.
		self.center_x = self.c_offset+(self.scale*self.res/2000.)+self.c_to_c*self.x
		self.center_y = self.c_offset+(self.scale*self.res/2000.)+self.c_to_c*self.y
		# Start of bbox
		self.start_x = self.c_offset+self.c_to_c*self.x
		self.start_y = self.c_offset+self.c_to_c*self.y
		# End of bbox
		self.end_x = self.c_offset+(self.scale*self.res/1000.)+self.c_to_c*self.x
		self.end_y = self.c_offset+(self.scale*self.res/1000.)+self.c_to_c*self.y
		# Construct bbox
		self.bbox = self.start_x, self.start_y, self.end_x, self.end_y
		# Draw self
		freeform_canvas.create_rectangle(self.bbox,tags=self.name,fill=UNSELECTED)
		freeform_canvas.tag_bind(self.name,'<Button-1>', lambda event, loc=[self.x,self.y]:self.click_button(event,loc))
		freeform_canvas.tag_bind(self.name,'<B1-Motion>', lambda event, loc=[self.x,self.y]:self.click_button(event,loc))

	def click_button(self, event, loc):
		x = loc[0]
		y = loc[1]
		str_name = "%i,%i"%(x,y)
		self.channel_select += 1
		self.channel_select = self.channel_select % 5
		self.canvas.parent.selected[str_name] = self.channel_select
		if self.channel_select == 0:
			self.canvas.itemconfig(str_name,fill=UNSELECTED)
		if self.channel_select == 1:
			self.canvas.itemconfig(str_name,fill=CH1)
		if self.channel_select == 2:
			self.canvas.itemconfig(str_name,fill=CH2)
		if self.channel_select == 3:
			self.canvas.itemconfig(str_name,fill=CH3)
		if self.channel_select == 4:
			self.canvas.itemconfig(str_name,fill=CH4)


if __name__ == "__main__":

	root = tk.Tk()
	fff = FreeformFrame(root)
	root.mainloop()
