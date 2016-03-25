import Tkinter as tk
import ttk
from LayerList import *

class App(tk.Tk):
	""" The App class represents the entire app and is the master to all """
	def __init__(self,*args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.wm_title("My Test App")
		self.geometry("600x600")
		self.resizable(1,1)

		# App-scope variables
		self.plateDiameterDict = {"35 mm":34.8}

		# The layer list frame is a frame that contains a list box and buttons for adding/editing/printing layers
		self.layerListFrame = LayerListFrame(self)
		self.layerListFrame.pack(side="right", fill="y")

if __name__ == "__main__":

	app = App()
	app.mainloop()

