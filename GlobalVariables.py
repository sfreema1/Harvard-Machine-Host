import Tkinter as tk

######### Globals ######
# I guess you don't need to declare global if you import 
# Maybe you just need global if you are going to want to modify these variables in the program
# A useful dictionary for converting indices into letters
ABC = {0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F", 6:"G", 7:"H", 8:"I", 9:"J"}

# If only one value is given for the key, then the print surface has a circular geometry (i.e wells) and the value represents its diameter
# If the key contains a list, its has a more rectangular geometry. The first entry is the width and the second entry is the height (X,Y)
# Dimension = [Plate Length, Plate Width, Plate Height]
DIMENSIONS = {	"Glass":{"Dimension":[200,200]}, 
				"100mm":{"Well Diameter":80.5},
				"60mm":{"Well Diameter":51.4}, 
				"35mm":{"Well Diameter":33.9},
				"6 Well":{"Layout":[2,3], "Well Depth":17.4, "Well Diameter":34.80, "Dimension":[127.76,85.47,20.27], "A1 Offset":[23.16,24.76], "Center-to-Center Spacing":39.12},
				"12 Well":{"Layout":[3,4], "Well Depth":17.53, "Well Diameter":22.11, "Dimension":[127.89,85.6,20.02], "A1 Offset":[16.79,24.94], "Center-to-Center Spacing":26.01},
				"24 Well":{"Layout":[4,6], "Well Depth":17.4, "Well Diameter":15.62, "Dimension":[127.89,85.6,19.69], "A1 Offset":[13.84,17.52], "Center-to-Center Spacing":19.3},
				"48 Well":{"Layout":[6,8], "Well Depth":17.4, "Well Diameter":11.05, "Dimension":[127.89,85.6,20.02], "A1 Offset":[10.08,18.16], "Center-to-Center Spacing":13.08},
				"96 Well":{"Layout":[8,12], "Well Depth":10.67, "Well Diameter":6.35, "Dimension":[127.8,85.5,14.2], "A1 Offset":[11.2,14.3], "Center-to-Center Spacing":9} }

# Newmark: Steps per mm
N_STEPS_PER_MM = 31496.063		# motor steps per mm

# Newmark Serial Baudrate
NEWMARK_BAUDRATE = 19200 # bits per sec

# Arduino Serial Baudrate
ARDUINO_BAUDRATE = 115200 # bits per sec

# Translate between XYZ axes and ABC axes
HOME_TRANSLATE = {"X" : "A", "Y": "B", "Z": "C", "XYZ": "ABC", "XY": "AB", "YZ": "BC", "XZ": "AC"}

########## COLORS (Hex Color Codes) ############
CTRL_TOP_BG = "#D3F723" 
CTRL_MID_BG = "#D3F723"
CTRL_BOT_BG = "#545994"

LAYER_TOP_BG = "#AAAAAA"
LAYER_LISTBOX_BG = "#BBBBBB"
LAYER_BOT_BG = "#AAAAAA"

TEXTBOX_BG = "#FFFBF7"

EXP_BG = "#BFB6A4"
PLATE_BG = "#2E4272"
WELL_COLOR = "#54a3b4"
ACT_WELL_COLOR = "#0D4D4D" #"#407F7F"
SEL_WELL_COLOR = "#0D4D4D"

TEXT_PREVIEW_COLOR = "#FBF100"




