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
		self.images = {"Purge":tk.PhotoImage(file="purge.gif")}
		# ========== FRAME PARAMETERS ========== #

		# =========== INITIALIZATION ========== #
		self.ch1 = ValveControlFrame(self, 1, self.parent)
		self.ch1.grid(row=0,column=0,sticky="nsew")
		self.ch2 = ValveControlFrame(self, 2, self.parent)
		self.ch2.grid(row=0,column=1,sticky="nsew")
		self.ch3 = ValveControlFrame(self, 3, self.parent)
		self.ch3.grid(row=0,column=2,sticky="nsew")
		self.ch4 = ValveControlFrame(self, 4, self.parent)
		self.ch4.grid(row=0,column=3,sticky="nsew")

class ValveControlFrame(tk.Frame):
	""" The ValveControlFrame gives options for controlling a microvalve """
	def __init__(self, parent, channel, master=None, **kwargs):
		tk.Frame.__init__(self, parent, **kwargs)
		# Specify hierarchy - IMPORTANT TO DO FIRST
		self.parent = parent # parent widget
		if master == None:
			self.master = parent
		else:
			self.master = master
		# ========== FRAME PARAMETERS ========== #
		self.valve_num = channel


		# ========== FRAME CONFIGURATION ========== #
		self.config(relief=tk.SUNKEN)

		# ========== INITIALIZATION ========== #
		self.label = tk.Label(self, text="Channel %i"%self.valve_num)
		self.label.grid(row=0,column=0)
		self.purge_label = tk.Label(self,text="Purge")
		self.purge_label.grid(row=1,column=2)
		self.button = tk.Button(self,image=self.parent.images["Purge"])
		self.button.grid(row=0,column=2)
		self.radio_button1 = tk.Radiobutton(self, text="Definite")
		self.radio_button1.grid(row=1,column=0)
		self.radio_button2 = tk.Radiobutton(self, text="Indefinite")
		self.radio_button2.grid(row=2,column=0)
		self.opening_label = tk.Label(self, text="Opening")
		self.opening_label.grid(row=3,column=0)
		self.freq_label = tk.Label(self,text="Frequency")
		self.freq_label.grid(row=4,column=0)
		self.drops_label = tk.Label(self,text="Droplets")
		self.drops_label.grid(row=5,column=0)

		self.opening_sb = tk.Spinbox(self,from_=300,to=2000,increment=50)
		self.opening_sb.grid(row=3,column=1)
		self.freq_sb = tk.Spinbox(self,from_=300,to=2000,increment=50)
		self.freq_sb.grid(row=4,column=1)
		self.drops_sb = tk.Spinbox(self,from_=300,to=2000,increment=50)
		self.drops_sb.grid(row=5,column=1)
