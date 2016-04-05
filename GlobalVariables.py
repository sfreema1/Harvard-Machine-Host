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

# Newmark Build Dimensions
BUILD_LENGTH = 160.0 # mm
BUILD_HEIGHT = 160.0 # mm

# Newmark: Steps per mm
N_STEPS_PER_MM = 31496.063		# motor steps per mm

# Newmark Serial Baudrate
NEWMARK_BAUDRATE = 19200 # bits per sec

# Arduino Serial Baudrate
ARDUINO_BAUDRATE = 9600 # bits per sec

# Build Surface Start - This is the start)x, start_y of the build surface (well plate, single dish, glass) 
BUILD_START = [-6.0,8.5] # [start_x, start_y] in mm in canvas/frame coordinates

# Microvalve Offsets
VALVE_OFFSETS = [[0,0], [-0.2,9.8], [0,19.6], [-0.7,32]] # Valve 1, Valve 2, Valve 3, Valve 4 offsets in (x,y) in mm 
VALVE_OFFSETS_X = [0,-9.8,-19.6,-32]
VALVE_OFFSETS_Y = [0,-0.2,0,-0.7]

# Translate between XYZ axes and ABC axes
HOME_TRANSLATE = {"X" : "A", "Y": "B", "Z": "C", "XYZ": "ABC", "XY": "AB", "YZ": "BC", "XZ": "AC"}

PRESSURE_DICT = {0.0:0,0.1:0,0.2:0,0.3:0,0.4:15,0.5:18,0.6:23,0.7:27,0.8:32,0.9:36,1.0:42,
                         1.1:47,1.2:52,1.3:57,1.4:63,1.5:68,1.6:72,1.7:78,1.8:84,1.9:90,2.0:95,
                        2.1:100,2.2:105,2.3:111,2.4:116,2.5:121,2.6:126,2.7:131,2.8:136,2.9:140,3.0:145,
                        3.1:150,3.2:154,3.3:158,3.4:163,3.5:167,3.6:170,3.7:173,3.8:177,3.9:181,4.0:184,
                        4.1:187,4.2:190,4.3:194,4.4:197,4.5:200,4.6:202,4.7:205,4.8:208,4.9:211,5.0:213,
                        5.1:216,5.2:218,5.3:220,5.4:222,5.5:225,5.6:227,5.7:229,5.8:231,5.9:233,6.0:235,
                        6.1:237,6.2:238,6.3:240,6.4:242,6.5:243,6.6:245,6.7:246,6.8:248,6.9:249,7.0:251,
                        7.0:251,7.1:252,7.2:254,7.3:255}

#

########## COLORS (Hex Color Codes) ############
CTRL_TOP_BG = "#644079" 
CTRL_MID_BG = "#644079"
CTRL_BOT_BG = "#644079"
CTRL_TEXT = "#E1D8E6"

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

# Freeform button colors #
# Unselected: #FFFFFF (White)
# Channel 1: #DE0600 (Red)
# Channel 2: #032F95 (Blue)
# Channel 3: #09B400 (Green)
# Channel 4: #FFA100 (Orange)
UNSELECTED = "#FFFFFF"
CH1 = "#DE0600"
CH2 = "#032F95"
CH3 = "#09B400"
CH4 = "#FFA100"

######### FONT ##########
CTRL_FONT = ('Arial',10,'bold')






