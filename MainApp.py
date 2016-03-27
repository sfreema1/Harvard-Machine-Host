import Tkinter as tk
import ttk
from LayerList import *
from ExperimentFrame import *
from GlobalVariables import *


class App(tk.Tk):
	""" The App class represents the entire app and is the master to all """
	def __init__(self,*args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.wm_title("My Test App")
		self.geometry("1360x610")
		self.resizable(1,1)


		### App-scope variables ###
		# A plate configuration
		self.p_config = "6 Well"
		# self.exp is where all layers are kept
		self.exp = [[[] for column in range(DIMENSIONS[self.p_config]["Layout"][1])] for row in range(DIMENSIONS[self.p_config]["Layout"][0])]
		# Selected well index
		self.sel_well_ind = [0,0]

		########## MENU BAR ##########
		self.menuBar = tk.Menu(self)
		self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
		self.fileMenu.add_command(label="New Experiment")
		self.fileMenu.add_command(label="Open Experiment")
		self.fileMenu.add_command(label="Save")
		self.fileMenu.add_command(label="Save As...")
		self.menuBar.add_cascade(label="File", menu=self.fileMenu)
		### Display the menu after everything has been added to it
		self.config(menu=self.menuBar)

		########## LAYER LIST FRAME #########
		# The layer list frame is a frame that contains a list box and buttons for adding/editing/printing layers
		self.layer_list_frame = LayerListFrame(self)
		self.layer_list_frame.pack(side="right", fill="y")

		########## EXPERIMENT FRAME ##########
		# The ExperimentConstruction Frame instance is where the wells will be seen
		self.exp_constr_frame = ExperimentConstructionFrame(self)
		self.exp_constr_frame.pack(side="left")

if __name__ == "__main__":

	app = App()
	app.mainloop()
