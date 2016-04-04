from Tkinter import *
    

def messageHelp(self):
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

def messageAbout(self):
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



def createTearOffWin(self):
    newWin = Toplevel()
    newWin.resizable(0,0)
    newWin.geometry("450x330")
    newWin.title('Initialization Window')

def generalSettingsWindow(self):
    genSetWin = Toplevel()
    genSetWin.resizable(0,0)
    genSetWin.geometry("450x330")
    genSetWin.title('General Settings')

def mQuit(self):
    mExit = tkMessageBox.askyesno(title="Quit", message="Are you sure you want to quit?")

    if mExit == True:
        self.parent.destroy()
        return
