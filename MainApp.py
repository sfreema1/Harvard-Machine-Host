import Tkinter as tk
from Tkinter import *
import ttk
import serial
from LayerList import *
from ExperimentFrame import *
from GlobalVariables import *
from ControlPanel import *
from PreferenceFrame import *
#from Help import *

"""Even Newer Comment"""


class App(tk.Tk):
	""" The App class represents the entire app and is the master to all """
	def __init__(self,*args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		# ===================== APP VARIABLES ===================== #
		# ========== SYSTEM VARIABLES ========== #
		self.scr_width = self.winfo_screenwidth()
		self.scr_height = self.winfo_screenheight()
		# ========== FRAME PARAMETERS ========== #
		self.app_name = "My Test App" 							# Text that appears in at the top of the app
		self.w_width = 1120										# Pixel width of main Tk window (W: 1120)
		self.w_height = 745										# Pixel height of main Tk window (W: 730)
		self.w_x_offset = (self.scr_width-self.w_width)/2	# Pixel x offset for the Tk window
		self.w_y_offset = (self.scr_height-self.w_height)/2	# Pixel y offset for the Tk window
		# ========== USER VARIABLES ========== #
		self.b_config = "96 Well" 															# A build surface/plate configuration
		self.p_row = DIMENSIONS[self.b_config]["Layout"][0]									# Number of well rows
		self.p_col = DIMENSIONS[self.b_config]["Layout"][1]									# Number of well columns
		self.exp = [[[] for column in range(self.p_col)] for row in range(self.p_row)] 		# Initialization of 2D list where experimental layout information will be stored
		self.sel_ind = [0,0]																# Selected well index
		self.isConnected_arduino = False
		self.isConnected_newmark = False

		# ==================== APP INITILIZATION ==================== #
		# ========== TK WINDOW CONFIGURATION ========== #
		self.wm_title(self.app_name)
		self.geometry("%dx%d+%d+%d" % (self.w_width, self.w_height, self.w_x_offset, self.w_y_offset))
		self.resizable(width=False,height=False)
		# ========== MENUBAR ========== #
		self.menuBar = tk.Menu(self)


		# Add items to a file menu
		self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
		# Add file menu to menubar
		self.menuBar.add_cascade(label="File", menu=self.fileMenu)
		self.fileMenu.add_command(label="New Experiment")
		self.fileMenu.add_command(label="Open Experiment")
		self.fileMenu.add_command(label="Save")
		self.fileMenu.add_command(label="Save As...")
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label="Exit",command=self.quit)



		editMenu = tk.Menu(self.menuBar, tearoff=0)
		self.menuBar.add_cascade(label="Edit", menu=editMenu)


		optionsMenu = tk.Menu(self.menuBar, tearoff=0)

		#mode submenu
		modeMenu = tk.Menu(optionsMenu, tearoff=0)
		    #printer submenu
		    #mapper
		    #viewer
		currentState = tk.StringVar()
		currentState.set("TissueBot")
		
		optionsMenu.add_command(label="Debug G-code")
		optionsMenu.add_separator()
		optionsMenu.add_command(label="Initialization")

		self.menuBar.add_cascade(label="Options", menu=optionsMenu)




		settingsMenu = tk.Menu(self.menuBar, tearoff=0)
		settingsMenu.add_command(label="General", command=generalSettingsWindow)
		#settingsMenu.add_command(label="gantry", command=self.modularGantry)
		self.menuBar.add_cascade(label="Settings", menu=settingsMenu)


		# Create Connect Menu
		self.connectMenu = tk.Menu(self.menuBar, tearoff=0)
		self.menuBar.add_cascade(label="Connect",menu=self.connectMenu)
		self.connectMenu.add_command(label="Refresh",command=self.refresh_available_ports_list)
		self.connectMenu.add_separator()
		# Create the menu to connect to the Newmark
		self.connectNewmarkMenu = tk.Menu(self.connectMenu,tearoff=0)
		self.connectNewmarkMenu.add_command(label="Autoconnect")
		self.connectNewmarkMenu.add_separator()
		self.connectNewmarkMenu.add_command(label="Disconnect", command=self.disconnect_newmark)
		self.connectMenu.add_cascade(label="Connect to Newmark", menu=self.connectNewmarkMenu)
		# Create the menu to connect to the Arduino
		self.connectArduinoMenu = tk.Menu(self.connectMenu,tearoff=0)
		self.connectArduinoMenu.add_command(label="Autoconnect")
		self.connectArduinoMenu.add_separator()
		self.connectArduinoMenu.add_command(label="Disconnect",command=self.disconnect_arduino)
		self.connectMenu.add_cascade(label="Connect to Arduino", menu=self.connectArduinoMenu)

		helpMenu = tk.Menu(self.menuBar, tearoff=0)
		helpMenu.add_command(label="Help Index", command=messageHelp)
		helpMenu.add_command(label="About", command=messageAbout)
		self.menuBar.add_cascade(label="Help", menu=helpMenu)

		self.config(menu=self.menuBar)  
		

		# ========== WORKSPACE ========== #
		self.workspace = ttk.Notebook(self, width=850)
		self.workspace.grid(row=0,column=0,columnspan=1,sticky="nsw")
		# Construction Tab
		self.constr_tab = tk.Frame(self.workspace)
		self.workspace.add(self.constr_tab,text="Construction")
		# Execution Tab
		self.exec_tab = tk.Frame(self.workspace)
		self.workspace.add(self.exec_tab,text="Execution")

		# ========== EXPERIMENT FRAME ========== #
		# The ExperimentConstruction Frame instance is where the wells will be seen
		self.exp_frame = ExperimentFrame(self.constr_tab,self)
		self.exp_frame.grid(row=0,column=0,sticky="nsew")

		# ========== LAYER LIST FRAME ========== #
		# The layer list frame is a frame that contains a list box and buttons for adding/editing/printing layers
		self.layer_list_frame = LayerListFrame(self.constr_tab,self)
		self.layer_list_frame.grid(row=0,column=1,sticky="nsew")

		# ========== CONTROL PANEL ========== #
		# THe control panel contains the buttons that will move the printer
		self.cp = ControlPanel(self)
		self.cp.grid(row=0,column=1,sticky="nsw")

		#========== SETTINGS TABS ==========#
		self.settings = ttk.Notebook(self)
		# Log Tab
		self.log_tab = tk.Frame(self.settings)
		self.log_tab.pack(fill="both",expand=True)
		self.settings.add(self.log_tab,text="Log")
		# G Code Log Textbox
		self.gcode_log = tk.Text(self.log_tab,height=10,width=135,state="disabled",bg=TEXTBOX_BG)
		self.gcode_log.pack(side="left",fill="both",expand=True)
		# G Code Textbox Scrollbar
		self.gcode_scrollbar = tk.Scrollbar(self.log_tab)
		self.gcode_scrollbar.pack(side="left",fill="y")
		# Bind the scrollbar
		self.gcode_log.config(yscrollcommand=self.gcode_scrollbar)
		self.gcode_scrollbar.config(command=self.gcode_log.yview)

		# Preference Tab
		self.pref_tab = PreferenceFrame(self.settings, self)
		self.pref_tab.pack(fill="both",expand=True)
		self.settings.add(self.pref_tab,text="Preferences")
		self.settings.grid(row=1,column=0,columnspan=2,ipadx=0,ipady=0,sticky="nsew")

	def refresh_available_ports_list(self,event=None):
		print "Refreshing ..."
		list_ = list_serial_ports()
		num_avail_ports = len(list_)
		# Delete all items in the menu
		self.connectNewmarkMenu.delete(0,"end")
		self.connectArduinoMenu.delete(0,"end")
		# Recreate them
		self.connectNewmarkMenu.insert_command(0,label="Autoconnect")
		self.connectArduinoMenu.insert_command(0,label="Autoconnect")
		self.connectNewmarkMenu.add_separator()
		self.connectArduinoMenu.add_separator()
		for i in range(num_avail_ports):
			self.connectNewmarkMenu.insert_command(i+1,label=list_[i],command=lambda port=list_[i]:self.connect_newmark(port))
			self.connectArduinoMenu.insert_command(i+1,label=list_[i],command=lambda port=list_[i]:self.connect_arduino(port))
		self.connectNewmarkMenu.insert_command("end",label="Disconnect", command=self.disconnect_newmark)
		self.connectArduinoMenu.insert_command("end",label="Disconect", command=self.disconnect_arduino)

	def connect_newmark(self,port):
		if self.isConnected_newmark == False:
			try:
				self.ser_newmark = serial.Serial(port,NEWMARK_BAUDRATE)
			except serial.SerialException:
				self.createPopUpMsgBox("Error","No serial available")
				return
			print self.ser_newmark.name
			self.isConnected_newmark = True
			self.refresh_available_ports_list()

	def disconnect_newmark(self):
		if self.isConnected_newmark == True:
			self.ser_newmark.close()
			self.refresh_available_ports_list()
			self.isConnected_newmark = False

	def connect_arduino(self, port):
		if self.isConnected_arduino == False:
			try:
				self.ser_arduino = serial.Serial(port,ARDUINO_BAUDRATE)
			except serial.SerialException:
				self.createPopUpMsgBox("Error","No serial available")
				return
			self.isConnected_arduino = True
			self.refresh_available_ports_list()

	def disconnect_arduino(self):
		if self.isConnected_arduino == True:
			self.ser_arduino.close()
			self.refresh_available_ports_list()
			self.isConnected_arduino = False



def messageHelp():
    mH = Toplevel()
    mH.resizable()
    mH.geometry("400x175")
    mH.title("Help")
    mHText = Text(mH,bg='#666666',fg='white',wrap=WORD)
    scrollbar = Scrollbar(mH,command=mHText.yview) #Fancy thing you have to do for the scrollbar to work
    scrollbar.pack(side=RIGHT,fill=Y) #Fancy thing you have to do for the srollbar to work
    mHText['yscrollcommand'] = scrollbar.set #Fancy thing you have to do for the srollbar to work
    mHText.insert(INSERT,"""Below are descriptions of valid commands to send the Harvard Bioprinter Arduino

Command format: M0 Rx Ly
This command sets pressure regulator 'x' to level 'y'. The level is a number between 0-255. At the current voltage settings,
a level of 255 will give about 7.4 psi.

Example: M0 R2 L255 - This will set pressure regulator #2 at 7.4 psi.

Command format: M1 Vx Ts
This command sets the microvalve opening time in microseconds for use in external mode only. The opening time has a lower and upper bound
which is set in the firmware Configuration.h file. Default opening times are set upon initialization and can also be found in Configuration.h file.
Closing time is not a user-controllable parameter.

Example: M1 V4 T750 - This will set valve #4 to remain open for 750 microseconds when pulses are received from the Newmark

Command format: M2 Vx (T or P)s Os Nq
This command sets opening and closing times for the microvalves in internal mode. Adding Nq to the command will caused the valves to run q times
Opening time can be set in microseconds using 'T' or milliseconds using 'P'. Opening time can only be set in milliseconds.
Both input methods have limits which are set in the firmware Configuration.h file. Default opening and closing times are loaded on initialization and can be found in
the Configuration.h file. If no 'Nq' is given, the opening and/or closing times will be set, but the microvalves will not run. 
Please see the following examples to understand the command's use.

Example: M2 V3 T500 - This will set valve #3 to open for 500 microseconds when it is run next. Other parameters are unchanged.
Example: M2 V3 P500 - This will set valve #3 to open for 500 milliseconds when it is run next. Other parameters are unchanged.
Example: M2 V3 O1000 - This will set the valve #3 to close for 1000 milliseconds. Other parameters are unchanged.
Example: M2 V3 T600 O500 - This is will set valve #3 to open for 600 microseconds and close for 500 milliseconds. Other parameters are unchanged.
Example: M2 V3 T755 O750 N10 - This will set valve #3 to open for 755 microseconds and close for 750 milliseconds. In additional, the valve will run this cycle 10 times.
Example: M2 V3 N50 - This will run the microvalves 50 times. The opening and closing times used will be those last given or the default values.

Command format: M90
This command sets the program in external mode. In external mode, the microvalves can only be controlled by the Newmark. M2 commands can be used to set the microvalve settings
for using in internal mode, but the microvalves cannot be run manually (an error will display).

Command format: M91
This command sets the program in internal mode. In internal mode, the microvalves can only be manually controlled. M2 command will be accepted. Pulses from the Newmark will be
ignored.""")
    mHText.pack(fill=BOTH, expand=TRUE) 

def messageAbout():
    mA = Toplevel()
    mA.resizable(0,0)
    mA.geometry("410x175")
    mLF = LabelFrame(mA, bg="#666666")
    mLF.pack(fill=BOTH, expand=TRUE)
    mA.title("About TissueBot")
    mA1=Label(mLF,text='TissueBot',font='bold',bg="#666666",fg="white").pack() #bg stands for background, fg stands for foreground (letter color)
    mA2=Label(mLF,text='Ye Labs',bg="#666666",fg="white").pack()
    mA4=Label(mLF,text='Kyle Reeser: kreeser1@binghamton.edu',bg="#666666",fg="white").pack()
    mA3=Label(mLF,text='Sebastian Freeman: sfreema1@binghamton.edu',bg="#666666",fg="white").pack()
    separator = Frame(mLF,height=2, bd=1, relief=SUNKEN) #The horizontal embedded in the "About" window
    separator.pack(fill=X, padx=5, pady=5) #Puts the separator on the screen
    mA5=Label(mLF,text='Credits: Kaiming Ye, Kyle Reeser, Sebastian Freeman, Alise Au',bg="#666666",fg="white").pack()
    mA6=Label(mLF,text='State University of New York at Binghamton',bg="#666666",fg="white").pack()
    mA7=Label(mLF,text='Biomedical Engineering Department, ITC, 2015-2016',bg="#666666",fg="white").pack()


def createTearOffWin():
    newWin = Toplevel()
    newWin.resizable(0,0)
    newWin.geometry("450x330")
    newWin.title('Initialization Window')

def generalSettingsWindow():
    genSetWin = Toplevel()
    genSetWin.resizable(0,0)
    genSetWin.geometry("450x330")
    genSetWin.title('General Settings')

def mQuit(self):
    mExit = tkMessageBox.askyesno(title="Quit", message="Are you sure you want to quit?")

    if mExit == True:
        self.parent.destroy()
        return


def list_serial_ports():
	""" 
		Lists serial port names
		:raises EnvironmentError:
			On unsupported or unknown platforms
		:returns:
			A list of the serial ports available on the system
	"""
	if sys.platform.startswith('win'):
		ports = ['COM%s' % (i + 1) for i in range(256)]
	elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
		# this excludes your current terminal "/dev/tty"
		ports = glob.glob('/dev/tty[A-Za-z]*')
	elif sys.platform.startswith('darwin'):
		ports = glob.glob('/dev/tty.*')
	else:
		raise EnvironmentError('Unsupported platform')

	result = []
	for port in ports:
		try:
			s = serial.Serial(port)
			s.close()
			result.append(port)
		except (OSError, serial.SerialException):
			pass
	return result


if __name__ == "__main__":

	app = App()
	app.mainloop()

