import Tkinter as tk
from GlobalVariables import *
import serial
import sys
import glob

class PreferenceFrame(tk.Frame):
	""" The PreferenceFrame gives user a quick interface to change basic variables or connect to devices """
	def __init__(self, parent, master=None, **kwargs):
		tk.Frame.__init__(self, parent, **kwargs)
		# Specify hierarchy - IMPORTANT TO DO FIRST
		self.parent = parent # parent widget
		if master == None:
			self.master = parent
		else:
			self.master = master
		# ========== USER VARIABLES ========= #

		# ========== FRAME PARAMETERS ========== #
