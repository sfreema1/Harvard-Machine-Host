import Tkinter as tk
from GlobalVariables import *
from CanvasObjects import *

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

		# ========== IMPORTED VARIABLES ========== #
		# Get well/print surface type
		self.b_config = self.master.b_config	# Print build config
		# ========== USER PARAMETERS ========== #
		self.selected_x = []
		self.selected_y = []

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


if __name__ == "__main__":
	root = tk.Tk()
	ef = ExperimentFrame(root)
	ef.pack(fill="both", expand=True)
	root.mainloop()


