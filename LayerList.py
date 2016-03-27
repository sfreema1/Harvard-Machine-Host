import Tkinter as tk
import ttk
from LayerWindow import *
from GlobalVariables import *

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
		self.label = tk.Label(self.top_frame, text="Click on the buttons to create/edit layers")
		self.label.pack(side="top")
		self.sel_well_label = tk.Label(self.top_frame, text="Selected well: %s%i" % (ABC[parent.sel_well_ind[0]],parent.sel_well_ind[1]+1))
		self.sel_well_label.pack(side="top")

		# Add all the buttons
		self.new_button = ttk.Button(self.top_frame, text="New", command=self.add_layer)
		self.new_button.pack(side="left")
		self.edit_button = ttk.Button(self.top_frame, text="Edit", command=self.edit_layer)
		self.edit_button.pack(side="left")
		self.copy_button = ttk.Button(self.top_frame, text="Copy", command=self.copy_layer)
		self.copy_button.pack(side="left")
		self.delete_button = ttk.Button(self.top_frame, text="Delete", command=self.delete_layer)
		self.delete_button.pack(side="left")
		self.move_up_button = ttk.Button(self.top_frame, text="Down", command=self.move_down_layer)
		self.move_up_button.pack(side="left")
		self.move_down_button = ttk.Button(self.top_frame, text="Up", command=self.move_up_layer)
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

	def edit_layer(self,event=None):
		if self.layer_listbox.get("anchor"):
			row = self.parent.sel_well_ind[0]
			col = self.parent.sel_well_ind[1]
			ind = self.layer_listbox.index("anchor")
			self.layer_build_window = LayerBuildWindow(self.parent,None,ind,**self.parent.exp[row][col][ind])

	def copy_layer(self):
		if self.layer_listbox.get("anchor"):
			row = self.parent.sel_well_ind[0]
			col = self.parent.sel_well_ind[1]
			ind = self.layer_listbox.index("anchor")
			self.parent.exp[row][col].append(self.parent.exp[row][col][ind])
			self.update_listbox()
			self.layer_listbox.selection_anchor(ind)
			self.layer_listbox.selection_set(ind)
			self.layer_listbox.activate(ind)

	def delete_layer(self):
		if self.layer_listbox.get("anchor"):
			row = self.parent.sel_well_ind[0]
			col = self.parent.sel_well_ind[1]
			ind = self.layer_listbox.index("anchor")
			last_ind = len(self.parent.exp[row][col])-1
			del self.parent.exp[row][col][ind]
			self.update_listbox()
			if ind == last_ind:
				ind = last_ind-1
			self.layer_listbox.selection_anchor(ind)
			self.layer_listbox.selection_set(ind)
			self.layer_listbox.activate(ind)

	def move_up_layer(self):
		row = self.parent.sel_well_ind[0]
		col = self.parent.sel_well_ind[1]
		if self.layer_listbox.get("anchor") and (self.layer_listbox.index("anchor")!=0):
			ind = self.layer_listbox.index("anchor")
			# Make temporary copies of the layers to be switched
			current_layer = self.parent.exp[row][col][ind]
			prev_layer = self.parent.exp[row][col][ind-1]
			# Now switch the layers with each other
			self.parent.exp[row][col][ind] = prev_layer
			self.parent.exp[row][col][ind-1] = current_layer
			# Update the list after the change
			self.update_listbox()
			# Have the anchor highlight follow the selection
			self.layer_listbox.selection_anchor(ind-1)
			self.layer_listbox.selection_set(ind-1)
			self.layer_listbox.activate(ind-1)

	def move_down_layer(self):
		row = self.parent.sel_well_ind[0]
		col = self.parent.sel_well_ind[1]
		if self.layer_listbox.get("anchor") and (self.layer_listbox.index("anchor")!=len(self.parent.exp[row][col])-1):
			ind = self.layer_listbox.index("anchor")
			# Make temporary copies of the layers to be switched
			current_layer = self.parent.exp[row][col][ind]
			next_layer = self.parent.exp[row][col][ind+1]
			# Now switch the layers with each other
			self.parent.exp[row][col][ind] = next_layer
			self.parent.exp[row][col][ind+1] = current_layer
			# Update the list after the change
			self.update_listbox()
			# Have the anchor highlight follow the selection
			self.layer_listbox.selection_anchor(ind+1)
			self.layer_listbox.selection_set(ind+1)
			self.layer_listbox.activate(ind+1)


	def update_listbox(self):
		self.layer_listbox.delete(0,"end")
		row = self.parent.sel_well_ind[0]
		col = self.parent.sel_well_ind[1]
		for layer in range(len(self.parent.exp[row][col])):
			self.layer_listbox.insert("end",self.parent.exp[row][col][layer]["Layer Name"].get())


if __name__ == "__main__":

	root = tk.Tk()
	layer_list = LayerListFrame(root)
	layer_list.pack(fill="both", expand=True)
	root.mainloop()


