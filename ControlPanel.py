import Tkinter as tk
from GlobalVariables import *
import ttk

class ControlPanel(tk.Frame):
	""" The ControlPanel will send commands to the printer when connected. """
	def __init__(self, parent, master=None, **kwargs):
		tk.Frame.__init__(self, parent, **kwargs)

		# Specify hierarchy
		self.parent = parent # parent widget
		if master == None:
			self.master = parent # master is App unless specified otherwise
		else:
			self.master = master

		########## FRAME CONFIGURATION ##########
		# Set the dimensions of the frame
		self.frame_width = 300
		self.frame_height = 800
		# Configure the dimensions of the frame
		self.config(width=self.frame_width, height=self.frame_height)

		########## FRAME VARIABLES ##########
		self.xy_opt = ["0.1", "1", "10", "100"]
		self.z_opt = ["0.1", "1", "10", "100"]
		self.home_opt = ["XYZ", "XY", "X", "Y", "Z"]
		self.xy_var = tk.StringVar()
		self.xy_var.set(self.xy_opt[0])
		self.z_var = tk.StringVar()
		self.z_var.set(self.z_opt[0])
		self.home_var = tk.StringVar()
		self.home_var.set(self.home_opt[0])
		self.gcode_var = tk.StringVar()

		########## Load images ##########
		self.images = {		"Home":tk.PhotoImage(file="home.gif"), 
							"Init":tk.PhotoImage(file="initialization.gif"),
							"InitPressed":tk.PhotoImage(file="initializationPressed.gif"),
							"Stop":tk.PhotoImage(file="emergency.gif"),
							"StopPressed":tk.PhotoImage(file="emergencyPressed.gif"),
							"Pause":tk.PhotoImage(file="pause.gif"),
							"PausePressed":tk.PhotoImage(file="pausePressed.gif"),
							"Resume":tk.PhotoImage(file="resume.gif"),
							"ResumePressed":tk.PhotoImage(file="resumePressed.gif"),
							"Left":tk.PhotoImage(file="leftButton.gif"),
							"Right":tk.PhotoImage(file="rightButton.gif"),
							"Up":tk.PhotoImage(file="upButton.gif"),
							"Down":tk.PhotoImage(file="downButton.gif")	}

		########### Test variables
		self.isPaused = False

		########## TOP FRAME ##########
		# Top Frame - Emergency Frame
		self.top_frame = tk.Frame(self, bg=CTRL_TOP_BG)
		self.top_frame.pack(side="top",fill="both",expand=True)
		# Label
		self.label = tk.Label(self.top_frame, text="Manual Control",bg=CTRL_TOP_BG)
		self.label.pack()
		# Initialization Button
		self.init_button = tk.Label(self.top_frame, image=self.images["Init"],bg=CTRL_TOP_BG)
		self.init_button.pack(side="left")
		self.init_button.bind('<Button-1>',self.initialize)
		self.init_button.bind('<ButtonRelease-1>',self.initialize)
		# Stop Button
		self.stop_button = tk.Label(self.top_frame, image=self.images["Stop"],bg=CTRL_TOP_BG)
		self.stop_button.pack(side="left")
		self.stop_button.bind('<Button-1>',self.stop)
		self.stop_button.bind('<ButtonRelease-1>',self.stop)
		# Pause Button
		self.pause_button = tk.Label(self.top_frame, image=self.images["Pause"],bg=CTRL_TOP_BG)
		self.pause_button.pack(side="left")
		self.pause_button.bind('<Button-1>',self.pause)
		self.pause_button.bind('<ButtonRelease-1>',self.pause)

		########## MIDDLE FRAME ##########
		# Middle Frame - XYZ Frame
		self.mid_frame = tk.Frame(self,bg=CTRL_MID_BG)
		self.mid_frame.pack(fill="both",expand=True)
		# XY Label
		self.xy_label = tk.Label(self.mid_frame, text="XY Motion",bg=CTRL_MID_BG)
		self.xy_label.grid(row=0,column=2)
		# Z Label
		self.z_label = tk.Label(self.mid_frame, text="Z Motion",bg=CTRL_MID_BG)
		self.z_label.grid(row=0,column=4)
		# X Negative Motion
		self.x_neg_button = tk.Button(self.mid_frame, image=self.images["Left"],highlightbackground=CTRL_MID_BG)
		self.x_neg_button.grid(row=2,column=1)
		# X Positive Motion
		self.x_pos_button = tk.Button(self.mid_frame, image=self.images["Right"],highlightbackground=CTRL_MID_BG)
		self.x_pos_button.grid(row=2,column=3)
		# Y Negative Movement
		self.y_neg_button = tk.Button(self.mid_frame, image=self.images["Down"],highlightbackground=CTRL_MID_BG)
		self.y_neg_button.grid(row=4,column=2)
		# Y Positive Movement
		self.y_pos_button = tk.Button(self.mid_frame, image=self.images["Up"],highlightbackground=CTRL_MID_BG)
		self.y_pos_button.grid(row=1,column=2)
		# XY Selection Menu
		self.xy_select = apply(tk.OptionMenu, (self.mid_frame,self.xy_var)+tuple(self.xy_opt))
		self.xy_select.config(bg=CTRL_MID_BG)
		self.xy_select.grid(row=2, column=2)
		# Z Negative Movement
		self.z_neg_button = tk.Button(self.mid_frame, image=self.images["Down"],highlightbackground=CTRL_MID_BG)
		self.z_neg_button.grid(row=4,column=4)
		# Z Positive Movement
		self.z_pos_button = tk.Button(self.mid_frame, image=self.images["Up"],highlightbackground=CTRL_MID_BG)
		self.z_pos_button.grid(row=1,column=4)
		# Z Selection Menu
		self.xy_select = apply(tk.OptionMenu, (self.mid_frame,self.z_var)+tuple(self.z_opt))
		self.xy_select.config(bg=CTRL_MID_BG)
		self.xy_select.grid(row=2,column=4)
		# Home Label
		self.home_label = tk.Label(self.mid_frame,text="Home",bg=CTRL_MID_BG)
		self.home_label.grid(row=5,column=3)
		# Home Button
		self.home_button = tk.Button(self.mid_frame,image=self.images["Home"],highlightbackground=CTRL_MID_BG)
		self.home_button.grid(row=6,column=2)
		# Home Selection Menu
		self.home_select = apply(tk.OptionMenu, (self.mid_frame,self.home_var)+tuple(self.home_opt))
		self.home_select.config(bg=CTRL_MID_BG)
		self.home_select.grid(row=6,column=4)

		########## G Code Frame ##########
		self.gcode_frame = tk.Frame(self,bg=CTRL_BOT_BG)
		self.gcode_frame.pack(fill="both",expand=True)
		# G Code Label
		self.gcode_label = tk.Label(self.gcode_frame,text="Enter G-code:",bg=CTRL_BOT_BG)
		self.gcode_label.grid(row=0,column=0)
		# G Code Entry
		self.gcode_entry = tk.Entry(self.gcode_frame,textvariable=self.gcode_var,width=25,highlightbackground=CTRL_BOT_BG)
		self.gcode_entry.grid(row=1,column=0,columnspan=2)
		self.gcode_entry.bind('<Return>',self.send_code)
		# G Code Send
		self.send_button = tk.Button(self.gcode_frame,text="Send",highlightbackground=CTRL_BOT_BG,command=self.send_code)
		self.send_button.grid(row=1,column=2)
		# Log Frame
		self.log_frame = tk.Frame(self,bg=CTRL_BOT_BG)
		self.log_frame.pack(fill="both",expand=True)
		# G Code Log Textbox
		self.gcode_log = tk.Text(self.log_frame,height=10,width=35,state="disabled")
		self.gcode_log.pack(side="left",fill="y")
		# G Code Textbox Scrollbar
		self.gcode_scrollbar = tk.Scrollbar(self.log_frame)
		self.gcode_scrollbar.pack(side="left",fill="y")
		# Bind the scrollbar
		self.gcode_log.config(yscrollcommand=self.gcode_scrollbar)

		########## Methods ##########
	def initialize(self,event=None):
		if event.type == '4':
			self.init_button.config(image=self.images["InitPressed"])
		if event.type == '5':
			self.init_button.config(image=self.images["Init"])
			print "Homing printer ... "

	def pause(self,event):
		if event.type == '4':
			if self.isPaused == False:
				self.pause_button.config(image=self.images["PausePressed"])
			else:
				self.pause_button.config(image=self.images["ResumePressed"])
		if event.type == '5':
			if self.isPaused == False:
				self.pause_button.config(image=self.images["Resume"])
				self.isPaused = True
			else:
				self.pause_button.config(image=self.images["Pause"])
				self.isPaused = False

	def stop(self,event):
		if event.type == '4':
			self.stop_button.config(image=self.images["StopPressed"])
		if event.type == '5':
			self.stop_button.config(image=self.images["Stop"])

	def send_code(self,event=None):
		if self.gcode_entry.get():
			line = self.gcode_entry.get()
			self.gcode_log.config(state="normal")
			self.gcode_log.insert("end",line.strip()+"\n")
			self.gcode_log.see("end")
			self.gcode_entry.delete(0,"end")


if __name__ == "__main__":

	root = tk.Tk()
	cp = ControlPanel(root)
	cp.pack(fill="both",expand=True)
	root.mainloop()