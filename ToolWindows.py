import Tkinter as tk
import ttk
import tkMessageBox
from GlobalVariables import *
from ExperimentFrame import *
from CanvasObjects import *

class LayerBuildWindow(tk.Toplevel):
	""" The LayerBuildWindow class uses tk.Toplevel to create a user-interface for inputting layer information"""
	def __init__(self, parent, master=None, layer_ind=None, **prevSettings):
		tk.Toplevel.__init__(self, master)
		# Set any bindings for keyboard shortcuts
		#self.bind('<Return>',self.submit)
		#self.bind('<Escape>',self.cancel)

		# Specify hierarchy
		self.parent = parent # parent widget
		if master == None:
			self.master = parent
		else:
			self.master = master

		# Initialize the LayerBuildWindow
		self.resizable(0,0) # Make the window non-resizable
		self.geometry("410x400")
		#self.grab_set()

		# Set a flag that indicates whether the user is editing a layer - could also just check if prevSettings exist
		if prevSettings:
			self.editFlag = True
			self.layer_ind = layer_ind
		else:
			self.editFlag = False

		# Set title of window differently depending on whether the user is editing or creating a new layer
		if self.editFlag:
			self.title("Edit layer")
		else:
			self.title("Create new layer")

		# Image Dictionary
		self.images = {	"Square": tk.PhotoImage(file="square.gif"), 
							"Circle": tk.PhotoImage(file="circle.gif"), 
							"Freeform": tk.PhotoImage(file="free.gif")	}

		# Variable Dictionary
		self.varsDict = {	"Layer Name":tk.StringVar(), "Pattern":tk.StringVar(),
							"Channel":tk.IntVar(), "Resolution":tk.DoubleVar(),
							"X Placement":tk.DoubleVar(), "Y Placement":tk.DoubleVar(),
							"Horizontal Alignment":tk.IntVar(), "Vertical Alignment":tk.IntVar(),
							"X Dimension":tk.DoubleVar(), "Y Dimension":tk.DoubleVar()}

		# Default Variable Values Dictionary
		self.defaultVarsDict = {	"Layer Name":"New Layer", "Pattern":"Ellipse",
									"Channel":1, "Resolution": 200,
									"X Placement":0, "Y Placement":0,
									"Horizontal Alignment":0, "Vertical Alignment":0,
									"X Dimension":0, "Y Dimension":0}

		# If editing a layer, load all the previously set variables
		if self.editFlag:
			for label in prevSettings.keys():
				self.varsDict[label].set(prevSettings[label].get())
		# If not, load default values
		else:
			for label in self.defaultVarsDict.keys():
				self.varsDict[label].set(self.defaultVarsDict[label])

		# Four Labelframes are used to organize the window:
		# 1. General
			# a. Entry Label
			# b. Entry Field
			# c. Channel Label 
			# d. Channel Spinbox
			# e. Resolution Label
			# f. Resolution Spinbox
		# 2. Placement
			# a. Center-of-Shape Coordinates Label
			# b. X Placement Label
			# c. X Placement Spinbox
			# d. Y Placement Label
			# e. Y Placement Spinbox
			# f. Aligment Label
			# g. Horizontal Alignment Radiobuttons
			# h. Vertical Alignment Radiobuttons
		# 3. Pattern
			# a. Square Button
			# b. Circle Button
			# c. Freeform Button
		# 4. Dimensions
			# a. X Dimension Label
			# b. X Dimension Spinbox
			# c. Y Dimension Label
			# d. Y Dimension Spinbox
			# e. Diameter Label
			# f. Diameter Spinbox

		########## LabelFrames ##########
		##### General section LabelFrame #####
		self.general = tk.LabelFrame(self, text="General")
		self.general.pack(fill="both", side="top", expand=True)
		# An entry field for the new layer name and a label
		self.entryLabel = tk.Label(self.general, text="Label:")
		self.entryLabel.grid(row=0, column=0, sticky="e")
		self.entry = tk.Entry(self.general, width=30, textvariable=self.varsDict["Layer Name"])
		self.entry.grid(row=0, column=1, sticky="w", columnspan=3)
		# A spinbox for entering the valve channel number and its label
		self.chanLabel = tk.Label(self.general, text="Channel:")
		self.chanLabel.grid(row=1, column=0)
		self.chanSpinbox = tk.Spinbox(self.general, width=7, from_=1, to=4,
													textvariable=self.varsDict["Channel"])
		self.chanSpinbox.grid(row=1, column=1)
		# A spinbox for entering the resolution value and its label
		self.resLabel = tk.Label(self.general, text=u"Resolution (\u03bcm):")
		self.resLabel.grid(row=1, column=2)
		self.resSpinbox = tk.Spinbox(self.general, width=7, from_=200,to=2000, increment=10,
													textvariable=self.varsDict["Resolution"])
		self.resSpinbox.grid(row=1, column=3)


		##### Placement section LabelFrame #####
		self.placement = tk.LabelFrame(self, text="Placement")
		self.placement.pack(fill="both", side="top", expand=True)
		# Center coordinate label
		self.centerLabel = tk.Label(self.placement, text="Shape center offset:")
		self.centerLabel.grid(row=0, column=0)
		# A spinbox for choose the x and y coordinates to place the pattern
		self.xPlaceLabel = tk.Label(self.placement, text="X (mm):")
		self.xPlaceLabel.grid(row=1, column=0)
		self.xPlaceSpinbox = tk.Spinbox(self.placement, width=8, from_=0, to=10, increment=0.1,
														textvariable=self.varsDict["X Placement"])
		self.xPlaceSpinbox.grid(row=1, column=1)
		self.yPlaceLabel = tk.Label(self.placement, text="Y (mm):")
		self.yPlaceLabel.grid(row=2, column=0)
		self.yPlaceSpinbox = tk.Spinbox(self.placement, width=8, from_=0, to=10, increment=0.1,
														textvariable=self.varsDict["Y Placement"])
		self.yPlaceSpinbox.grid(row=2, column=1)
		# Alignment label
		self.alignLabel = tk.Label(self.placement, text="Alignment:")
		self.alignLabel.grid(row=0, column=3)
		# Three radio buttons to choose the horizontal alignment
		row = 1
		HORIZONTAL_ALIGNMENT = [("Left", -1), ("Center", 0), ("Right", 1)]
		for text, value in HORIZONTAL_ALIGNMENT:
			radio = tk.Radiobutton(self.placement, text=text, value=value, variable=self.varsDict["Horizontal Alignment"])
			radio.grid(row=row, column=3)
			row += 1
		# Three radio buttons to choose the vertical 
		row = 1
		VERTICAL_ALIGNMENT = [("Top", -1), ("Middle", 0), ("Bottom", 1)]
		for text, value in VERTICAL_ALIGNMENT:
			radio = tk.Radiobutton(self.placement, text=text, value=value, variable=self.varsDict["Vertical Alignment"])
			radio.grid(row=row, column=4)
			row += 1
		

		##### Pattern section LabelFrame ####
		self.pattern = tk.LabelFrame(self, text="Pattern")
		self.pattern.pack(fill="both", side="top", expand=True)
		# Buttons to select pattern geometry - Square, Circle, Freeform
		self.squareButton = tk.Button(self.pattern, image=self.images["Square"], command=self.select_square)
		self.squareButton.grid(row=0, column=0)
		self.circleButton = tk.Button(self.pattern, image=self.images["Circle"], command=self.select_circle)
		self.circleButton.grid(row=0, column=1)
		self.freeButton = tk.Button(self.pattern, image=self.images["Freeform"], command=self.select_freeform)
		self.freeButton.grid(row=0, column=2)


		##### Dimension section LabelFrame ####
		self.dimension = tk.LabelFrame(self, text="Dimension")
		self.dimension.pack(fill="both", side="top", expand=True)
		# Dimensions for the pattern - X/Y or diameter
		# X
		self.xDimLabel = tk.Label(self.dimension, text="X (mm):")
		self.xDimLabel.grid(row=0, column=0)
		self.xDimSpinbox = tk.Spinbox(self.dimension, width=8, from_=0.00, to=100.00, increment=0.1, textvariable=self.varsDict["X Dimension"])
		self.xDimSpinbox.grid(row=0, column=1)
		# Y
		self.yDimLabel = tk.Label(self.dimension, text="Y (mm):")
		self.yDimLabel.grid(row=1, column=0)
		self.yDimSpinbox = tk.Spinbox(self.dimension, width=8, from_=0.00, to=100.00, increment=0.1, textvariable=self.varsDict["Y Dimension"])
		self.yDimSpinbox.grid(row=1, column=1)

		##### Submit, Preview, and Cancel buttons #####
		self.cancelButton = tk.Button(self, text="Cancel", bd=5, command=self.destroy)
		self.cancelButton.pack(side="right", expand=True)
		self.previewButton = tk.Button(self, text="Preview", bd=5, command=self.preview)
		self.previewButton.pack(side="right", expand=True)
		self.submitButton = tk.Button(self, text="Submit", bd=5, command=self.submit)
		self.submitButton.pack(side="left", expand=True)

	########## Methods ##########
	def submit(self,event=None):
		if self.varsDict["X Dimension"].get() == 0 or self.varsDict["Y Dimension"].get() == 0:
			self.createPopUpMsgBox("Error","Non-zero dimensions must be selected to add a new layer.")
			return
		else:
			row = self.master.sel_ind[0]
			col = self.master.sel_ind[1]
			if self.editFlag and self.layer_ind is not None:
				self.master.exp[row][col][self.layer_ind] = self.varsDict
			else:
				self.master.exp[row][col].append(self.varsDict)
			self.master.layer_list_frame.update_listbox()
			self.destroy()

	def preview(self):
		if self.varsDict["X Dimension"].get() == 0 or self.varsDict["Y Dimension"].get() == 0:
			self.createPopUpMsgBox("Error","Non-zero dimensions must be set to preview.")
		else:
			self.previewWindow = PreviewWindow(self.master, **self.varsDict)

	def cancel(self,event=None):
		self.destroy()

	def select_square(self):
		print "Rectangle selected"
		self.varsDict["Pattern"].set("Rectangle")

	def select_circle(self):
		print "Ellipse selected"
		self.varsDict["Pattern"].set("Ellipse")

	def select_freeform(self):
		self.varsDict["Pattern"].set("Freeform")
		if self.varsDict["X Dimension"].get() == 0 or self.varsDict["Y Dimension"].get() == 0:
			self.createPopUpMsgBox("Error","Non-zero dimensions must be set to preview.")
		else:
			self.freeformWindow = FreeformFrame(self.master, **self.varsDict)

	def createPopUpMsgBox(self, title, msg):
		tkMessageBox.showinfo(title, msg)



class PreviewWindow(tk.Toplevel):
	""" The PreviewWindow class is used to display the desired pattern in the well. """
	def __init__(self, parent, master=None, **settings):
		tk.Toplevel.__init__(self, parent)
		# Specify hierarchy - IMPORTANT TO DO FIRST
		self.parent = parent # parent widget
		if master == None:
			self.master = parent
		else:
			self.master = master
		# ===================== WINDOW VARIABLES ===================== #
		self.tags_list = []		# Could be used later to target specific shapes drawn to the canvas
		# ========== IMPORTED VARIABLES ========= #
		# Get current row and column plate selection
		self.cur_row = self.master.sel_ind[0] 	# row in plate
		self.cur_col = self.master.sel_ind[1]	# column in plate
		# Get well/print surface type
		self.b_config = self.master.b_config	# Print build config
		self.prev_vars = settings

		# ========== FRAME PARAMETERS ========== #
		self.name = "Preview well" 								# Text that appears in at the top of the app
		self.w_width = 700										# Pixel width of main Tk window
		self.w_height = 700										# Pixel height of main Tk window
		self.w_center_x = self.w_width/2
		self.w_center_y = self.w_height/2
		self.w_center = [self.w_center_x, self.w_center_y]
		self.w_x_offset = (self.master.scr_width-self.w_width)/2	# Pixel x offset for the Tk window
		self.w_y_offset = (self.master.scr_height-self.w_height)/2	# Pixel y offset for the Tk window

		# ==================== CLASS INITILIZATION ==================== #
		# ========== TOPLEVEL WINDOW CONFIGURATION ========== #
		self.wm_title(self.name)
		self.geometry("%dx%d+%d+%d" % (self.w_width, self.w_height, self.w_x_offset, self.w_y_offset))
		self.resizable(width=False,height=False)

		# ========== CANVAS CONFIGURATION ========== #
		# Start CanvasWell a.k.a. tk.Canvas in disguise preconfigured with a well, and coordinate display
		self.canvas_well = CanvasWell(self,self.master)
		self.canvas_well.pack(fill="both", expand=True)

		# ========== DRAW SHAPES =========== #
		self.draw()

	def draw(self):
		row = self.cur_row
		col = self.cur_col
		num_layer = len(self.master.exp[row][col])
		# First draw any previous created layers in the well
		if num_layer > 0:
			for layer in range(num_layer):
				# Quick reference variables to pass to the CanvasShape object
				layer_vars = self.master.exp[row][col][layer]
				dim = [layer_vars["X Dimension"].get(), layer_vars["Y Dimension"].get()]
				offset = [layer_vars["X Placement"].get(), layer_vars["Y Placement"].get()]
				horiz_align = layer_vars["Horizontal Alignment"].get()
				vert_align = layer_vars["Vertical Alignment"].get()

				if layer_vars["Pattern"].get() == "Rectangle":
					shape = CanvasRectangle(self.canvas_well, dim, offset, horiz_align, vert_align,layer)
					self.tags_list.append(shape.tag)
				elif layer_vars["Pattern"].get() == "Ellipse":
					shape = CanvasEllipse(self.canvas_well, dim, offset, horiz_align, vert_align,layer)
					self.tags_list.append(shape.tag)

		# Then draw the PreviewWindow Shape
		dim = [self.prev_vars["X Dimension"].get(), self.prev_vars["Y Dimension"].get()]
		offset = [self.prev_vars["X Placement"].get(), self.prev_vars["Y Placement"].get()]
		horiz_align = self.prev_vars["Horizontal Alignment"].get()
		vert_align = self.prev_vars["Vertical Alignment"].get()

		if self.prev_vars["Pattern"].get() == "Rectangle":
			shape = CanvasRectangle(self.canvas_well, dim, offset, horiz_align, vert_align)
			self.tags_list.append(shape.tag)
		elif self.prev_vars["Pattern"].get() == "Ellipse":
			shape = CanvasEllipse(self.canvas_well, dim, offset, horiz_align, vert_align)
			self.tags_list.append(shape.tag)



class HelpWindow(tk.Toplevel):
	""" The HelpWindow class generates a tk.Toplevel to display help information. """
	def __init__(self,parent,master=None,**kwargs):
		tk.Toplevel.__init__(self,master)
		# Specify hierarchy
		self.parent = parent # parent widget
		if master == None:
			self.master = parent
		else:
			self.master = master

		# ========== TOPLEVEL FRAME PARAMETERS ========== #
		self.name = "Help"
		self.icon_name = self.master.icon_name
		self.w_width = 400
		self.w_height = 175
		self.w_center_x = self.master.w_center_x
		self.w_center_y = self.master.w_center_y
		self.w_x_offset = self.master.w_x_offset
		self.w_y_offset = self.master.w_y_offset
		
		# ========== CLASS INITIALIZATION ========== #
		self.title(self.name)
		self.iconbitmap(self.master.icon_name)
		self.resizable()
		self.geometry("%dx%d+%d+%d" % (self.w_width, self.w_height, self.w_x_offset, self.w_y_offset))
		# Textbox
		self.textbox = tk.Text(self,bg=HELP_WINDOW_BG,fg=HELP_WINDOW_FG,wrap="word")
		# Scrollbar
		self.scrollbar = tk.Scrollbar(self,command=self.textbox.yview)
		self.scrollbar.pack(side="right",fill="y")
		self.textbox.config(yscrollcommand=self.scrollbar.set)
		# Finally pack the textbox
		self.textbox.pack(side="left",fill="both",expand="true")
		# insert text
		# ========== HELP WINDOW TEXT ========== #
		with open("help.txt") as f:
			for line in f:
				self.textbox.insert("insert",line)

		#self.bind('<Configure>',self._frame_configure)

	def _frame_configure(self,event):
		self.w_width = self.winfo_reqwidth()
		self.w_height = self.winfo_reqheight()
		test = self.winfo_geometry()
		print "The current frame dimensions are (%rX%r)" % (self.w_width,self.w_height)
		print "The geometry is %r" % test

class AboutWindow(tk.Toplevel):
	""" The AboutWindow class generates a tk.Toplevel to display information about YeLabs """
	def __init__(self,parent,master=None,**kwargs):
		tk.Toplevel.__init__(self,master)
		# Specify hierarchy
		self.parent = parent # parent widget
		if master == None:
			self.master = parent
		else:
			self.master = master

		# ========== TOPLEVEL FRAME PARAMETERS ========== #
		self.name = "About "+ self.master.app_name
		self.icon_name = self.master.icon_name
		self.w_width = 400
		self.w_height = 175
		self.w_center_x = self.master.w_center_x
		self.w_center_y = self.master.w_center_y
		self.w_x_offset = self.master.w_x_offset
		self.w_y_offset = self.master.w_y_offset

		# ========== CLASS INITIALIZATION ========== #
		self.title(self.name)
		self.iconbitmap(self.master.icon_name)
		self.resizable(0,0)
		self.geometry("%dx%d+%d+%d" % (self.w_width, self.w_height, self.w_x_offset, self.w_y_offset))

		# LabelFrame
		self.labelFrame = tk.LabelFrame(self,bg=ABOUT_WINDOW_BG)
		self.labelFrame.pack(fill="both",expand=True)
		# About information
		self.printer_title = tk.Label(self.labelFrame,text=self.master.app_name+" Host Software",font='bold',bg=ABOUT_WINDOW_BG,fg=ABOUT_WINDOW_FG)
		self.printer_title.pack()
		self.lab_title = tk.Label(self.labelFrame,text="Ye Labs",bg=ABOUT_WINDOW_BG,fg=ABOUT_WINDOW_FG)
		self.lab_title.pack()
		self.author_contact_1 = tk.Label(self.labelFrame,text="Kyle Reeser: kreeser1@binghamton.edu",bg=ABOUT_WINDOW_BG,fg=ABOUT_WINDOW_FG)
		self.author_contact_1.pack()
		self.author_contact_2 = tk.Label(self.labelFrame,text="Sebastian Freeman: sfreema1@binghamton.edu",bg=ABOUT_WINDOW_BG,fg=ABOUT_WINDOW_FG)
		self.author_contact_2.pack()
		# Separator
		self.separator = tk.Frame(self.labelFrame,height=2,bd=1,relief="sunken")
		self.separator.pack(fill="x",padx=5,pady=5)
		self.credit_label = tk.Label(self.labelFrame,text="Credits: Kaiming Ye, Kyle Reeser, Sebastian Freeman, Alise Au")
		self.credit_label.config(bg=ABOUT_WINDOW_BG,fg=ABOUT_WINDOW_FG)
		self.credit_label.pack()
		self.univ_label=tk.Label(self.labelFrame,text="Biomedical Engineering Department, ITC, 2015-2016")
		self.univ_label.config(bg=ABOUT_WINDOW_BG,fg=ABOUT_WINDOW_FG)
		self.univ_label.pack()

class ExpConfigSelectionWindow(tk.Toplevel):
	""" The SelectionWindow class generates a tk.Toplevel to allow the user to  """
	def __init__(self,parent,master=None,**kwargs):
		tk.Toplevel.__init__(self,master)
		# Specify hierarchy
		self.parent = parent # parent widget
		if master == None:
			self.master = parent
		else:
			self.master = master

		# ========== TOPLEVEL FRAME PARAMETERS ========== #
		self.name = "Select a build platform"
		self.icon_name = self.master.icon_name
		self.w_width = 400
		self.w_height = 200
		self.w_center_x = self.master.w_center_x
		self.w_center_y = self.master.w_center_y
		self.w_x_offset = self.master.w_x_offset
		self.w_y_offset = self.master.w_y_offset

		# ========== CLASS INITIALIZATION ========== #
		self.title(self.name)
		self.iconbitmap(self.master.icon_name)
		#self.resizable(0,0)
		self.geometry("%dx%d+%d+%d" % (self.w_width, self.w_height, self.w_x_offset, self.w_y_offset))
		# Top frame with listbox
		self.top_frame = tk.Frame(self)
		self.top_frame.pack(side="top",fill="both",expand=True)
		# Selection listbox
		self.selection_list = tk.Listbox(self.top_frame)
		self.selection_list.pack(side="left",fill="both",expand=True)
		# Selection list scrollbar
		self.scrollbar = ttk.Scrollbar(self.top_frame)
		self.scrollbar.pack(side="left",fill="y")
		# Bottom frame with buttons
		self.bot_frame = tk.Frame(self)
		self.bot_frame.pack(side="bottom",fill="both",expand=True)
		# Buttons
		# Select button
		self.select_button = tk.Button(self.bot_frame,text="Select",command=self.select)
		self.select_button.pack(side="left",expand=True)
		# Cancel button
		self.cancel_button = tk.Button(self.bot_frame,text="Cancel",command=self.destroy)
		self.cancel_button.pack(side="right",expand=True)

		self.update_listbox()

	def update_listbox(self):
		self.selection_options = DIMENSIONS.keys()
		for key in self.selection_options:
			self.selection_list.insert("end",key)

	def select(self,event=None):
		selection = self.selection_list.get("anchor")		# The selection as a string
		if selection:
			self.master._reload_app_vars(selection)
			self.destroy()
			
			