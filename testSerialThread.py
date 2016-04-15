
from Tkinter import *
from time import sleep
import serial
from threading import *


i = 0

def handle_click():

	def press():
		ser = serial.Serial('COM11',19200)
		code = open('Code_wellA1.txt')
		line = code.readline()
		global i
		while line:
			if i == 1:
				i = 0
				ser.close()
				break
				# need to exit the thread

			elif i == 2:
				i = 0
				while True:
					if i ==2:
						i = 0
						break
			else:
				if line == "END":
					#break

					print ("YOU'RE DONE")

				else:
					ser.write(line.strip("\n")+"\r")
					print line.strip("\n")+"\r"
					readport(ser)
				line = code.readline()
		code.close()

	def readport(server):
		ser = server
		while True:
			data = ser.readline().strip(":?")
			data = data.strip("\r\n")
			data= float(data)
			data = int(data)
			print data
			if data ==0:
				sleep(0.2)
				break
			else:
				sleep(0.01)

		
	

	t = Thread(target=press)
	t.start()



def stopevent():
	global i
	i = 1

def pause():
	global i
	i = 2

root = Tk()
#Button(root, text='Connect', command = connection).pack()
Button(root, text='Read', command=handle_click).pack()
Button(root, text="Stop",command=stopevent).pack()
Button(root, text="Pause",command=pause).pack()
label = Label(root)
label.pack()
root.mainloop()
