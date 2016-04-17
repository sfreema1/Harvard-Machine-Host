import Tkinter as tk

class App(tk.Tk):
	def __init__(self,*args,**kwargs):
		tk.Tk.__init__(self,*args,**kwargs)
		# =================== APP VARIABLES ==================== #
		# ========== SYSTEM VARIABLES ========== # 
		# Screen parameters
		self.scr_width = self.winfo_screenwidth()		# screen width (pixels)
		self.scr_height = self.winfo_screenheight()		# screen height (pixels)
		self.scr_area = self.scr_width*self.scr_height 	# screen area (pixels X pixels)
		# ========== APP FRAME PARAMETERS ========== #
		self.app_name = "YooPrint Bioprinter" 				# Text that appears in at the top of the app
		self.icon_name = "yooprinter.ico"					# Filename of logo icon file (.ico file)
		self.w_width = 1120									# Pixel width of main Tk window (W: 1120)
		self.w_height = 745									# Pixel height of main Tk window (W: 730)
		self.w_area = self.w_width*self.w_height 			# Window pixel area
		self.w_center_x = self.scr_width/2
		self.w_center_y = self.scr_height/2
		self.w_x_offset = (self.scr_width-self.w_width)/2		# Pixel x offset for the Tk window
		self.w_y_offset = (self.scr_height-self.w_height)/2		# Pixel y offset for the Tk window

		# ========== EXPERIMENT FRAME PARAMETERS ========== #
		self.b_config = "None"

		# =================== TK WINDOW INITIALIZATION ==================== #
		self.expFrame = ExperimentFrame(self)

class ExperimentFrame(tk.Frame):
	def __init__(self, parent, master=None, **kwargs):
		tk.Frame.__init__(self, parent, **kwargs)
		# Specify hierarchy - IMPORTANT TO DO FIRST
		# The assignments below do not create new copies of object instances, only references
		self.parent = parent # parent widget
		if master == None:
			self.master = parent
		else:
			self.master = master
		# ===================== FRAME VARIABLES ===================== #
		self._bot_frame_offset = 10

		''' ========== CANVAS VARIABLES ========== #
		# self.b_config 

		'''
		# ========== INITIALIZATION ========== #
		self.build_canvas = CanvasBuildPlate(self,self.master)
		self.build_canvas.pack()

	def _get_experiment_parameters(self):
		self.b_config = self.master.b_config

	def draw_build(self):
		pass



class CanvasBuildPlate(tk.Canvas):
	def __init__(self,parent, master=None, **kwargs):
		tk.Canvas.__init__(self, parent, **kwargs)
		# Specify hierarchy - IMPORTANT TO DO FIRST
		self.parent = parent # parent widget
		if master == None:
			self.master = parent
		else:
			self.master = master
		# ==================== CANVAS VARIABLES ==================== #
		self.width = 30
		self.tags = []


if __name__ == "__main__":
	app = App()
	app.mainloop()

