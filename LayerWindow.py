import Tkinter as tk
import ttk
import tkMessageBox
from PreviewWindow import *

class LayerBuildWindow(tk.Toplevel):
	""" The LayerBuildWindow class uses tk.Toplevel to create a user-interface for inputting layer information"""
	def __init__(self, master, selectedEntry=None, **prevSettings):
		tk.Toplevel.__init__(self, master)
		# Set any bindings for keyboard shortcuts
		self.bind('<Return>',self.submit)
		self.bind('<Escape>',self.cancel)

		# Initialize the LayerBuildWindow
		self.master = master # App is received as master of LayerBuildWindow instance
		self.resizable(0,0) # Make the window non-resizable
		self.geometry("410x400")
		self.grab_set()

		# Set a flag that indicates whether the user is editing a layer - could also just check if prevSettings exist
		if prevSettings:
			self.editFlag = True
		else:
			self.editFlag = False

		# Set title of window differently depending on whether the user is editing or creating a new layer
		if self.editFlag:
			self.title("Edit layer")
		else:
			self.title("Create new layer")

		# Image Dictionary
		self.imageDict = {	"Square": tk.PhotoImage(file="square.gif"), 
							"Circle": tk.PhotoImage(file="circle.gif"), 
							"Freeform": tk.PhotoImage(file="free.gif")	}

		# Variable Dictionary
		self.varsDict = {	"Layer Name":tk.StringVar(), "Pattern":tk.StringVar(),
							"Channel":tk.IntVar(), "Resolution":tk.DoubleVar(),
							"X Placement":tk.DoubleVar(), "Y Placement":tk.DoubleVar(),
							"Horizontal Alignment":tk.IntVar(), "Vertical Alignment":tk.IntVar(),
							"X Dimension":tk.DoubleVar(), "Y Dimension":tk.DoubleVar()}

		# Default Variable Values Dictionary
		self.defaultVarsDict = {	"Layer Name":"New Layer", "Pattern":"Square",
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
		self.squareButton = tk.Button(self.pattern, image=self.imageDict["Square"], command=self.select_square)
		self.squareButton.grid(row=0, column=0)
		self.circleButton = tk.Button(self.pattern, image=self.imageDict["Circle"], command=self.select_circle)
		self.circleButton.grid(row=0, column=1)
		self.freeButton = tk.Button(self.pattern, image=self.imageDict["Freeform"], command=self.select_freeform)
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
		self.destroy()

	def preview(self):
		if self.varsDict["X Dimension"].get() == 0 or self.varsDict["Y Dimension"].get() == 0:
			self.createPopUpMsgBox("Error","Non-zero dimensions must be set to preview.")
		else:
			self.previewWindow = PreviewWindow(self.master, **self.varsDict)

	def cancel(self,event=None):
		self.destroy()

	def select_square(self):
		self.varsDict["Pattern"].set("Rectangle")

	def select_circle(self):
		self.varsDict["Pattern"].set("Ellipse")

	def select_freeform(self):
		self.varsDict["Pattern"].set("Freeform")

	def createPopUpMsgBox(self,title,msg):
		tkMessageBox.showinfo(title,msg)


if __name__ == "__main__":

	root = tk.Tk()
	lbw = LayerBuildWindow(root)
	root.mainloop()


