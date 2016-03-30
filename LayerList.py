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
		self.top_frame = tk.Frame(self,bg=LAYER_TOP_BG)
		self.top_frame.pack(side="top",fill="both")

		# Create a selected well label
		self.sel_well_label = tk.Label(self.top_frame, text="Selected well: %s%i" % (ABC[self.master.sel_ind[0]],self.master.sel_ind[1]+1))
		self.sel_well_label.config(bg=LAYER_TOP_BG)
		self.sel_well_label.grid(row=1,column=0,columnspan=3,sticky="nsew")

		# Add all the buttons
		self.new_button = tk.Button(self.top_frame,text="New",width=7,highlightbackground=LAYER_TOP_BG,command=self.add_layer)
		self.new_button.grid(row=2,column=0)
		self.edit_button = tk.Button(self.top_frame,text="Edit",width=7,highlightbackground=LAYER_TOP_BG,command=self.edit_layer)
		self.edit_button.grid(row=2,column=1)
		self.copy_button = tk.Button(self.top_frame,text="Copy",width=7,highlightbackground=LAYER_TOP_BG,command=self.copy_layer)
		self.copy_button.grid(row=3,column=1)
		self.delete_button = tk.Button(self.top_frame,text="Delete",width=7,highlightbackground=LAYER_TOP_BG,command=self.delete_layer)
		self.delete_button.grid(row=3,column=0)
		self.move_up_button = tk.Button(self.top_frame,text="Down",width=7,highlightbackground=LAYER_TOP_BG,command=self.move_down_layer)
		self.move_up_button.grid(row=3,column=2)
		self.move_down_button = tk.Button(self.top_frame,text="Up",width=7,highlightbackground=LAYER_TOP_BG,command=self.move_up_layer)
		self.move_down_button.grid(row=2,column=2)

		# Add separate frame to contain listbox and its scrollbar
		self.listbox_frame = tk.Frame(self,bg=LAYER_LISTBOX_BG)
		self.listbox_frame.pack(fill="both",expand=True)
		# Add the list box
		self.layer_listbox = tk.Listbox(self.listbox_frame)
		self.layer_listbox.pack(side="left", fill="both", expand=True)
		# Add the scrollbar
		self.listbox_scrollbar = ttk.Scrollbar(self.listbox_frame)
		self.listbox_scrollbar.pack(side="left",fill="y")
		# Unify listbox and scrollbar
		self.layer_listbox.config(yscrollcommand=self.listbox_scrollbar)
		self.listbox_scrollbar.config(command=self.layer_listbox.yview)

		# Add a final frame for some more buttons
		self.bot_frame = tk.Frame(self,bg=LAYER_BOT_BG)
		self.bot_frame.pack(fill="both")
		# Print well button
		self.print_button = tk.Button(self.bot_frame,text="Print well",width=7,highlightbackground=LAYER_BOT_BG,command=self.print_well)
		self.print_button.grid(row=0,column=0)
		# Print all button
		self.print_all_button = tk.Button(self.bot_frame,text="Print all",width=7,highlightbackground=LAYER_BOT_BG,command=self.print_all)
		self.print_all_button.grid(row=0,column=1)
		# Debug - ** For testing ** - Will be taken out/replaced later
		self.debug_button = tk.Button(self.bot_frame,text="Debug",width=7,highlightbackground=LAYER_BOT_BG,command=self.debug)
		self.debug_button.grid(row=0,column=2)


		########### Methods ##########
	def add_layer(self):
		self.layer_build_window = LayerBuildWindow(self.master) # I pass App as master of LayerBuildWindow instance

	def edit_layer(self,event=None):
		if self.layer_listbox.get("anchor"):
			row = self.master.sel_ind[0]
			col = self.master.sel_ind[1]
			ind = self.layer_listbox.index("anchor")
			self.layer_build_window = LayerBuildWindow(self.master,None,ind,**self.master.exp[row][col][ind])

	def copy_layer(self):
		if self.layer_listbox.get("anchor"):
			row = self.master.sel_ind[0]
			col = self.master.sel_ind[1]
			ind = self.layer_listbox.index("anchor")
			self.master.exp[row][col].append(self.master.exp[row][col][ind])
			self.update_listbox()
			self.layer_listbox.selection_anchor(ind)
			self.layer_listbox.selection_set(ind)
			self.layer_listbox.activate(ind)

	def delete_layer(self):
		if self.layer_listbox.get("anchor"):
			row = self.master.sel_ind[0]
			col = self.master.sel_ind[1]
			ind = self.layer_listbox.index("anchor")
			last_ind = len(self.master.exp[row][col])-1
			del self.master.exp[row][col][ind]
			self.update_listbox()
			if ind == last_ind:
				ind = last_ind-1
			self.layer_listbox.selection_anchor(ind)
			self.layer_listbox.selection_set(ind)
			self.layer_listbox.activate(ind)

	def move_up_layer(self):
		row = self.master.sel_ind[0]
		col = self.master.sel_ind[1]
		if self.layer_listbox.get("anchor") and (self.layer_listbox.index("anchor")!=0):
			ind = self.layer_listbox.index("anchor")
			# Make temporary copies of the layers to be switched
			current_layer = self.master.exp[row][col][ind]
			prev_layer = self.master.exp[row][col][ind-1]
			# Now switch the layers with each other
			self.master.exp[row][col][ind] = prev_layer
			self.master.exp[row][col][ind-1] = current_layer
			# Update the list after the change
			self.update_listbox()
			# Have the anchor highlight follow the selection
			self.layer_listbox.selection_anchor(ind-1)
			self.layer_listbox.selection_set(ind-1)
			self.layer_listbox.activate(ind-1)

	def move_down_layer(self):
		row = self.master.sel_ind[0]
		col = self.master.sel_ind[1]
		if self.layer_listbox.get("anchor") and (self.layer_listbox.index("anchor")!=len(self.master.exp[row][col])-1):
			ind = self.layer_listbox.index("anchor")
			# Make temporary copies of the layers to be switched
			current_layer = self.master.exp[row][col][ind]
			next_layer = self.master.exp[row][col][ind+1]
			# Now switch the layers with each other
			self.master.exp[row][col][ind] = next_layer
			self.master.exp[row][col][ind+1] = current_layer
			# Update the list after the change
			self.update_listbox()
			# Have the anchor highlight follow the selection
			self.layer_listbox.selection_anchor(ind+1)
			self.layer_listbox.selection_set(ind+1)
			self.layer_listbox.activate(ind+1)


	def update_listbox(self):
		self.layer_listbox.delete(0,"end")
		row = self.master.sel_ind[0]
		col = self.master.sel_ind[1]
		for layer in range(len(self.master.exp[row][col])):
			self.layer_listbox.insert("end",self.master.exp[row][col][layer]["Layer Name"].get())

	def print_well(self):
		pass

	def print_all(self):
		pass

	def debug(self):
		pass


if __name__ == "__main__":

	root = tk.Tk()
	layer_list = LayerListFrame(root)
	layer_list.pack(fill="both", expand=True)
	root.mainloop()


