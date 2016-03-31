import Tkinter as tk
import ttk
import serial
from LayerList import *
from ExperimentFrame import *
from GlobalVariables import *
from ControlPanel import *
from PreferenceFrame import *


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

		# Add the menu to "self", which is the App
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
		self.pref_tab = PreferenceFrame(self.settings)
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

