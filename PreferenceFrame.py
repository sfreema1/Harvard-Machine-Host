import Tkinter as tk
#from Tkinter import *
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
		self.ch1 = ValveControlFrame(self, 1, self.master)
		self.ch1.grid(row=0,column=0,sticky="nsew")
		self.ch2 = ValveControlFrame(self, 2, self.master)
		self.ch2.grid(row=0,column=1,sticky="nsew")
		self.ch3 = ValveControlFrame(self, 3, self.master)
		self.ch3.grid(row=0,column=2,sticky="nsew")
		self.ch4 = ValveControlFrame(self, 4, self.master)
		self.ch4.grid(row=0,column=3,sticky="nsew")

		self.lastFrame = tk.Frame(self)
		self.lastFrame.grid(row=0,column=4,sticky="nsew")

		self.lastFrame1 = tk.Frame(self)
		self.lastFrame1.grid(row=0,column=5,sticky="nsew")
		label1 = tk.Label(self.lastFrame1,text = "Channels to Execute")
		label1.pack()



        #self.label1 = tk.Label(lastFrame,text="Hello!")
        #self.label1.pack()
        
		self.pressureVar1 = tk.DoubleVar()
		self.pressureVar1.set(0.0)
		self.pressureVar2 = tk.DoubleVar()
		self.pressureVar2.set(0.0)
		self.pressureVar3 = tk.DoubleVar()
		self.pressureVar3.set(0.0)
		self.pressureVar4 = tk.DoubleVar()
		self.pressureVar4.set(0.0)
		self.last_Label = tk.Label(self.lastFrame, text="Pressures and Command Execution").pack()
		self.pressure_int1 = tk.Spinbox(self.lastFrame, bd =5,width=8,from_=0.0,to=7.3, increment = 0.1,wrap="FALSE",textvariable=self.pressureVar1,command=self.setPressure_int1)
		self.pressure_int1.pack()
		self.pressure_int2 = tk.Spinbox(self.lastFrame, bd =5,width=8,from_=0.0,to=7.3, increment = 0.1,wrap="FALSE",textvariable=self.pressureVar2,command=self.setPressure_int2)
		self.pressure_int2.pack()
		self.pressure_int3 = tk.Spinbox(self.lastFrame, bd =5,width=8,from_=0.0,to=7.3, increment = 0.1,wrap="FALSE",textvariable=self.pressureVar3,command=self.setPressure_int3)
		self.pressure_int3.pack()
		self.pressure_int4 = tk.Spinbox(self.lastFrame, bd =5,width=8,from_=0.0,to=7.3, increment = 0.1,wrap="FALSE",textvariable=self.pressureVar4,command=self.setPressure_int4)
		self.pressure_int4.pack()
		

		self.checkVar = tk.IntVar()

		ch1_check = tk.Radiobutton(self.lastFrame1,text = "Channel 1",variable = self.checkVar, value = 1)
		ch2_check = tk.Radiobutton(self.lastFrame1,text = "Channel 2",variable = self.checkVar, value = 2)
		ch3_check = tk.Radiobutton(self.lastFrame1,text = "Channel 3",variable = self.checkVar, value = 3)
		ch4_check = tk.Radiobutton(self.lastFrame1,text = "Channel 4",variable = self.checkVar, value = 4)

		ch1_check.pack()
		ch2_check.pack()
		ch3_check.pack()
		ch4_check.pack()

		self.start_internal1 = tk.Button(self.lastFrame1, text="Start", width=3, font=('Helvetica',12),command = self.startInternal)
		self.start_internal1.pack()

	
	def startInternal(self):
		#closing = self.calculateClosing()
		if self.master.isConnected_arduino:
			# In Hz
			frequency_1 = self.ch1.freq_var.get()
			frequency_2 = self.ch2.freq_var.get()
			frequency_3 = self.ch3.freq_var.get()
			frequency_4 = self.ch4.freq_var.get()
			#print "Desired frequencies (Hz): Ch1:%r,Ch2:%r,Ch3:%r,Ch4:%r"%(frequency_1,frequency_2,frequency_3,frequency_4)
			
			# Period time in milliseconds
			period_1 = 1000.*(1./frequency_1)
			period_2 = 1000.*(1./frequency_2)
			period_3 = 1000.*(1./frequency_3)
			period_4 = 1000.*(1./frequency_4)
			#print "Desired periods (ms): Ch1:%r,Ch2:%r,Ch3:%r,Ch4:%r"%(period_1, period_2, period_3, period_4)

			opening_1 = self.ch1.opening_var.get()
			opening_2 = self.ch2.opening_var.get()
			opening_3 = self.ch3.opening_var.get()
			opening_4 = self.ch4.opening_var.get()
			#print "Desired opening time (us): Ch1:%r,Ch2:%r,Ch3:%r,Ch4:%r"%(opening_1, opening_2, opening_3, opening_4)

			closing_1 = period_1 - opening_1/1000.0
			closing_2 = period_2 - opening_2/1000.0
			closing_3 = period_3 - opening_3/1000.0
			closing_4 = period_4 - opening_4/1000.0
			#print "Calculated closing time (ms): Ch1:%r,Ch2:%r,Ch3:%r,Ch4:%r"%(closing_1, closing_2, closing_3, closing_4)

			self.channelNum = self.checkVar.get()
			self.master.ser_arduino.write("M91"+"\r\n") # enter internal mode
			#print (self.channelNum)
			if self.channelNum == 1:
				line = 'M2 V1 T%i C%d N%i'%(opening_1,closing_1,self.ch1.drops_var.get())
				#print (line)
				self.master.ser_arduino.write(line +"\r\n")
				return
			elif self.channelNum == 2:
				line = 'M2 V2 T%i C%d N%i'%(opening_2,closing_2,self.ch2.drops_var.get())
				#print (line)
				self.master.ser_arduino.write(line +"\r\n")
				return
			elif self.channelNum == 3:
				line = 'M2 V3 T%i C%d N%i'%(opening_3,closing_3,self.ch3.drops_var.get())
				#print (line)
				self.master.ser_arduino.write(line +"\r\n")
				return
			elif self.channelNum == 4:
				line = 'M2 V4 T%i C%d N%i'%(opening_4,closing_4,self.ch4.drops_var.get())
				#print (line)
				self.master.ser_arduino.write(line +"\r\n")
				return
			else:
				pass
			self.master.ser_arduinio.write("M90"+"\r\n") # return internal mode

	def setPressure_int1(self):
		if self.master.isConnected_arduino:
			pressure = self.pressureVar1.get()
			pressure1 = PRESSURE_DICT.get(pressure)
			#print (pressure1)
			line = 'M0 R1 L%s'%(pressure1)
			#print (line)
			self.master.ser_arduino.write(line +"\r\n")
			return

	def setPressure_int2(self):
		if self.master.isConnected_arduino:
			pressure = self.pressureVar2.get()
			pressure1 = PRESSURE_DICT.get(pressure)
			#print (pressure1)
			line = 'M0 R2 L%s'%(pressure1)
			#print (line)
			self.master.ser_arduino.write(line +"\r\n")
			return

	def setPressure_int3(self):
		if self.master.isConnected_arduino:
			pressure = self.pressureVar3.get()
			pressure1 = PRESSURE_DICT.get(pressure)
			#print (pressure1)
			line = 'M0 R3 L%s'%(pressure1)
			#print (line)
			self.master.ser_arduino.write(line +"\r\n")
			return

	def setPressure_int4(self):
		if self.master.isConnected_arduino:
			pressure = self.pressureVar4.get()
			pressure1 = PRESSURE_DICT.get(pressure)
			#print (pressure1)
			line = 'M0 R4 L%s'%(pressure1)
			#print (line)
			self.master.ser_arduino.write(line +"\r\n")
			return




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

		# ========== FUNCTIONS ========== #


		
		'''
		def setFrequency(self):
			frequency = self.freq_var.get()
			print (frequency)
			line = 'M1 R%i L%i'%(self.valve_num),%(opening)
			print (line)
			self.master.ser_arduino.write(line +"\r\n")
			return

		def setDrops(self):
			drops = self.drops_var.get()
			print (drops)
			line = 'M1 R%i L%i'%(self.valve_num),%(opening)
			print (line)
			self.master.ser_arduino.write(line +"\r\n")
			return
		'''


		# ========== INITIALIZATION ========== #
		self.defIndef = tk.IntVar() #Control variable for Definite/Indefinite radio buttons
		self.defIndef.set(1)        #Setting control variable to 1 makes "Definite" selected automatically upon launch of the program

		self.label = tk.Label(self, text="Channel %i"%self.valve_num)
		self.label.grid(row=0,column=0)
		self.purge_label = tk.Label(self,text="Purge")
		self.purge_label.grid(row=1,column=1)
		self.button = tk.Button(self,image=self.parent.images["Purge"])
		self.button.grid(row=0,column=1)
		self.radio_button1 = tk.Radiobutton(self, text="Definite",variable=self.defIndef, value=1,command = self.defIndef_func)
		self.radio_button1.grid(row=1,column=0)
		self.radio_button2 = tk.Radiobutton(self, text="Indefinite",variable=self.defIndef, value=2,command = self.defIndef_func)
		self.radio_button2.grid(row=2,column=0)
		self.opening_label = tk.Label(self, text="Opening")
		self.opening_label.grid(row=3,column=0)
		self.freq_label = tk.Label(self,text="Frequency")
		self.freq_label.grid(row=4,column=0)
		self.drops_label = tk.Label(self,text="Droplets")
		self.drops_label.grid(row=5,column=0)

		self.button.bind('<Button-1>', self.initialPressedEvent)
		self.button.bind('<ButtonRelease-1>', self.initialReleasedEvent)


		self.opening_var = tk.IntVar()
		self.freq_var = tk.DoubleVar()
		self.drops_var = tk.IntVar()
		self.opening_sb = tk.Spinbox(self,from_=300,to=2000,increment=50,wrap="TRUE",width=10,textvariable=self.opening_var,command=self.setOpening)
		self.opening_sb.grid(row=3,column=1,sticky="W")
		self.freq_sb = tk.Spinbox(self,from_=0.1,to=20,increment=0.1,wrap="TRUE",width=10,textvariable=self.freq_var)
		self.freq_sb.grid(row=4,column=1,sticky="W")
		self.drops_sb = tk.Spinbox(self,from_=1,to=1000,increment=1,wrap="TRUE",width=10,textvariable=self.drops_var)
		self.drops_sb.grid(row=5,column=1,sticky="W")

		self.opening_unit = tk.Label(self,text="us")
		self.opening_unit.grid(row=3,column=2)
		self.freq_unit = tk.Label(self,text="Hz")
		self.freq_unit.grid(row=4,column=2)
		self.drops_unit = tk.Label(self,text="Drops")
		self.drops_unit.grid(row=5,column=2)

	def setOpening(self):
		if self.master.isConnected_arduino:
			opening = self.opening_var.get()
			#print (opening)
			valve = self.valve_num
			#print (valve)
			line = 'M1 V%i T%i'%(valve,opening)
			#print (line)
			self.master.ser_arduino.write("M91"+"\r\n") # Enter external mode
			self.master.ser_arduino.write(line +"\r\n")
			self.master.ser_arduino.write("M90"+"\r\n") # Return to internal mode
			return

	def defIndef_func(self):
		if self.defIndef.get() == 1:
			self.defIndef.set(2)
			self.drops_sb.config(state = "disabled")
			#print (self.defIndef.get())
			return
		else:
			self.defIndef.set(1)
			self.drops_sb.config(state = "normal")
			#print (self.defIndef.get())
			return

	def initialPressedEvent(self,event):
		if self.master.isConnected_arduino:
			line = 'M3 V%i S255'%self.valve_num
			self.master.ser_arduino.write("M91"+"\r\n")
			self.master.ser_arduino.write(line +"\r\n")
			#print("Hello")
			#print(line)


	def initialReleasedEvent(self, event):
		if self.master.isConnected_arduino:
			line = 'M3 V%i S0'%self.valve_num
			self.master.ser_arduino.write(line +"\r\n")
			self.master.ser_arduino.write("M90"+"\r\n")
			#print("Good Bye")
			#print(line)