import Tkinter as tk
import ttk
from LayerWindow import *

class LayerListFrame(tk.Frame):
	""" The LayerListFrame class contains the buttons and listbox that are modified when a user adds a layer to be printed. It interacts with the PlanExperiment class to pass information to visualize the experiment """
	def __init__(self, parent, master=None, **kwargs):
		tk.Frame.__init__(self, parent, **kwargs)
		self.config(relief=tk.RIDGE, bd=5, takefocus=0)

		# Specify hierarchy
		self.parent = parent # parent widget
		if master == None:
			self.master = parent # master is App unless specified otherwise
		else:
			self.master = master

		# Top frame contains a label and the buttons that control the listbox
		self.top_frame = tk.Frame(self)
		self.top_frame.pack(side="top")

		# Create a label
		self.test_label = tk.Label(self.top_frame, text="Click on the buttons to create/edit layers")
		self.test_label.pack(side="top")

		# Add all the buttons
		self.new_button = ttk.Button(self.top_frame, text="New", command=self.add_layer)
		self.new_button.pack(side="left")
		self.edit_button = ttk.Button(self.top_frame, text="Edit")
		self.edit_button.pack(side="left")
		self.copy_button = ttk.Button(self.top_frame, text="Copy")
		self.copy_button.pack(side="left")
		self.delete_button = ttk.Button(self.top_frame, text="Delete")
		self.delete_button.pack(side="left")
		self.move_up_button = ttk.Button(self.top_frame, text="Move Up")
		self.move_up_button.pack(side="left")
		self.move_down_button = ttk.Button(self.top_frame, text="Move Down")
		self.move_down_button.pack(side="left")

		# Add separate frame to contain listbox and its scrollbar
		self.listbox_frame = tk.Frame(self)
		self.listbox_frame.pack(side="bottom", fill="both", expand=True)

		# Add the scrollbar
		self.listbox_scrollbar = ttk.Scrollbar(self.listbox_frame)
		self.listbox_scrollbar.pack(side="right")

		# Add the list box
		self.layer_listbox = tk.Listbox(self.listbox_frame)
		self.layer_listbox.pack(side="right", fill="both", expand=True)

		# Unify listbox and scrollbar
		self.layer_listbox.config(yscrollcommand=self.listbox_scrollbar.set)
		self.listbox_scrollbar.config(command=self.layer_listbox.yview)

		########### Methods ##########
	def add_layer(self):
		self.layer_build_window = LayerBuildWindow(self.parent) # I pass App as master of LayerBuildWindow instance

	def edit_layer(self):
		pass