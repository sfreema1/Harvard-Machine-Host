import Tkinter as tk
import ttk
from LayerWindow import *


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


class LayerListFrame(tk.Frame):
	""" The LayerListFrame class contains the buttons and listbox that are modified when a user adds a layer to be printed. It interacts with the PlanExperiment class to pass information to visualize the experiment """
	def __init__(self, parent, **kwargs):
		tk.Frame.__init__(self, parent, **kwargs)
		self.config(relief=tk.RIDGE, bd=5, takefocus=0)
		self.parent = parent # parent is App

		# Top frame contains a label and the buttons that control the listbox
		self.topFrame = tk.Frame(self)
		self.topFrame.pack(side="top")

		# Create a label
		self.testLabel = tk.Label(self.topFrame, text="Click on the buttons to create/edit layers")
		self.testLabel.pack(side="top")

		# Add all the buttons
		self.newButton = ttk.Button(self.topFrame, text="New", command=self.add_layer)
		self.newButton.pack(side="left")
		self.editButton = ttk.Button(self.topFrame, text="Edit")
		self.editButton.pack(side="left")
		self.copyButton = ttk.Button(self.topFrame, text="Copy")
		self.copyButton.pack(side="left")
		self.deleteButton = ttk.Button(self.topFrame, text="Delete")
		self.deleteButton.pack(side="left")
		self.moveUpButton = ttk.Button(self.topFrame, text="Move Up")
		self.moveUpButton.pack(side="left")
		self.moveDownButton = ttk.Button(self.topFrame, text="Move Down")
		self.moveDownButton.pack(side="left")

		# Add separate frame to contain listbox and its scrollbar
		self.listBoxFrame = tk.Frame(self)
		self.listBoxFrame.pack(side="bottom", fill="both", expand=True)

		# Add the scrollbar
		self.listScrollbar = ttk.Scrollbar(self.listBoxFrame)
		self.listScrollbar.pack(side="right")

		# Add the list box
		self.layerList = tk.Listbox(self.listBoxFrame)
		self.layerList.pack(side="right", fill="both", expand=True)

		# Unify listbox and scrollbar
		self.layerList.config(yscrollcommand=self.listScrollbar.set)
		self.listScrollbar.config(command=self.layerList.yview)

		########### Methods ##########
	def add_layer(self):
		self.layerBuildWindow = LayerBuildWindow(self.parent) # I pass App as master of LayerBuildWindow instance

	def edit_layer(self):
		pass

if __name__ == "__main__":

	app = App()
	app.mainloop()

