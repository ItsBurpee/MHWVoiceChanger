from tkinter import filedialog
from tkinter import *
import os
import Query
import MainGUIVer

# import the library
from appJar import gui
# create a GUI variable called app
app = gui("MHW Voice Changer", "640x340")

otherAssets = "wwiseutil.exe"
otherAssetsFound = True

validInputFile = False
validInputVoice = True
validOutputVoice = True
canConvert = True

manualMode = False

#METHOD: convertCheck
#	Checks the conditions if conversion is possible
#	PARAMETERS:
#		None
#	RETURN:
#		If conversion is possible
def convertCheck():
	global otherAssetsFound
	global validInputVoice
	global validOutputVoice
	global canConvert
	
	#canConvert holds TRUE only IF:
		#otherAssetsFound - wwiseutil.exe is detected
		#validInputFile - The current input file is valid
		#A file is currently loaded
		#validInputVoice - The input voice is supported
		#validOutputVoice - The output voice is supported
	canConvert = otherAssetsFound and validInputFile and (app.getEntry("Input File Name") != "") and validInputVoice and validOutputVoice
	#IF: conversion is possible, allow conversion
	if canConvert:
		app.enableButton("CONVERT")
	#ELSE: conversion isn't possible, disallow conversion
	else:
		app.disableButton("CONVERT")
		
	return canConvert

#METHOD: otherAssetsCheck
#	Checks if the other assets are present
#	PARAMETERS:
#		None
#	RETURN:
#		None		
def otherAssetsCheck():
	global otherAssetsFound 
	
	currentDir = os.listdir("./")
	#TRY: Looking for Wwiseutil
	try:
		currentDir.index(otherAssets)
	#EXCEPT: Error for missing Wwiseutil, change it to the warning color (RED)
	except ValueError:
		app.setLabel("Wwise Label", "Wwiseutil: ERROR")
		app.setLabelFg("Wwise Label", "red") 
		otherAssetsFound = False
	
	#TRY: Checking the DB version
	try:
		dbVersion = Query.getVersion()	
		app.setLabel("DB Label", "DB Version: " + str(dbVersion[0]))
	#EXCEPT: Error for missing DB, change it to the warning color (RED)
	except:
		app.setLabel("DB Label", "DB Version: ERROR")
		app.setLabelFg("DB Label", "red") 

#METHOD: updateInputOverview
#	Updates the input voice overview
#	PARAMETERS:
#		None
#	RETURN:
#		None
def updateInputOverview():
	global validInputVoice
	
	#Get the input file info
	updateFileGender = app.getRadioButton("InGender")
	updateFileNumber = app.getOptionBox("InVoice")
	
	#Convert the format to used for a query and get the voice file information
	updateFileGender = updateFileGender.upper()		
	updateFileID = updateFileGender + "_" + updateFileNumber
	fileIDQuery = (updateFileID,)
	updateInfo = Query.identifyFileID(fileIDQuery)
	
	#Check if the voice file is supported (Ready = 1)
	validInputVoice = (updateInfo[4] == 1)
	
	#Update the input voice overview
	app.setLabel("InputNameOverview", updateInfo[1] + " Voice " + str(updateInfo[2]))
	app.setLabel("InputFileOverview", updateInfo[3])
	#IF: the voice file was supported, change it to the normal color (BLACK)
	if validInputVoice:
		app.setLabelFg("InputNameOverview", "black")
		app.setLabelFg("InputFileOverview", "black")
		app.setStatusbar("Updated input voice information", field=0)	
	#ELSE: the voice file wasn't supported, change it to the warning color (RED)
	else:
		app.setLabelFg("InputNameOverview", "red")
		app.setLabelFg("InputFileOverview", "red")
		app.setStatusbar("Updated input voice information. WARNING: Unsupported voice selected", field=0)	
	
	convertCheck()
	
#METHOD: updateOutputOverview
#	Updates the output voice overview
#	PARAMETERS:
#		None
#	RETURN:
#		None
def updateOutputOverview():
	global validOutputVoice
	
	#Get the output file info
	updateFileGender = app.getRadioButton("OutGender")
	updateFileNumber = app.getOptionBox("OutVoice")
	
	#Convert the format to used for a query and get the voice file information
	updateFileGender = updateFileGender.upper()		
	updateFileID = updateFileGender + "_" + updateFileNumber
	fileIDQuery = (updateFileID,)
	updateInfo = Query.identifyFileID(fileIDQuery)
	
	#Check if the voice file is supported (Ready = 1)
	validOutputVoice = (updateInfo[4] == 1)
	
	#Update the output voice overview
	app.setLabel("OutputNameOverview", updateInfo[1] + " Voice " + str(updateInfo[2]))
	app.setLabel("OutputFileOverview", updateInfo[3])
	#IF: the voice file was supported, change it to the normal color (BLACK)
	if validOutputVoice:
		app.setLabelFg("OutputNameOverview", "black")
		app.setLabelFg("OutputFileOverview", "black")
		app.setStatusbar("Updated output voice information", field=0)	
	#ELSE: the voice file wasn't supported, change it to the warning color (RED)
	else:
		app.setLabelFg("OutputNameOverview", "red")
		app.setLabelFg("OutputFileOverview", "red")
		app.setStatusbar("Updated output voice information. WARNING: Unsupported voice selected", field=0)	
	
	convertCheck()

#METHOD: autoDetect
#	Updates the input voice overview based on the input file's name
#	PARAMETERS:
#		None
#	RETURN:
#		If the input file was identified
def autoDetect():
	global manualMode

	#Run a query on the given nbnk file
	nbnkName = (app.getEntry("Input File Name"),)
	autoDetectInfo = Query.identifyFileName(nbnkName)
	
	#IF: the file name is identified, continue
	if(autoDetectInfo != None):
		if(autoDetectInfo[1] == "Other"):
			app.setStatusbar("WARNING: Voices outside the normal character voices are unsupported", field=0)
			return manualMode
		else:
			app.setRadioButton("InGender", autoDetectInfo[1], callFunction=False)
			app.setOptionBox("InVoice", autoDetectInfo[2]-1, callFunction=False)
			updateInputOverview()
			app.setStatusbar("Auto-detected voice information", field=0)
			return True
	#ELSE: the file name couldn't be identified, warn the user
	else:
		app.setStatusbar("WARNING: Could not auto-detect voice information", field=0)
		if nbnkExtensionCheck():
			return manualMode
		else:
			return False

#METHOD: nbnkExtensionCheck
#	Checks if the input file's extension is .nbnk
#	PARAMETERS:
#		None
#	RETURN:
#		If the input file's extension is .nbnk
def nbnkExtensionCheck():
	nbnkName = app.getEntry("Input File Name")
	extensionDot = nbnkName.rfind(".")
	fileExtension = nbnkName[extensionDot:]
	return fileExtension == ".nbnk"

#METHOD: validateInputFile
#	Updates the input file entry's status
#	PARAMETERS:
#		None
#	RETURN:
#		None
def validateInputFile():
	global validInputFile	
	global manualMode
	
	if manualMode and nbnkExtensionCheck():
		app.setEntryWaitingValidation("Input File Name")
	elif validInputFile:
		app.setEntryValid("Input File Name")
	else:
		app.setEntryInvalid("Input File Name")
	
#METHOD: loadFile
#	Loads a file and detects if it's valid
#	PARAMETERS:
#		None
#	RETURN:
#		None
def loadFile():
	global validInputFile
	
	#Open a file dialog for the user to pick a file
	root = Tk()
	root.withdraw()
	root.filename =  filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("nbnk files","*.nbnk"),("all files","*.*")))
	
	#IF: an input file was given, continue
	if (root.filename != ""):
	
		#Show the input file path at the top
		app.setEntry("Input File Path:", root.filename)
		
		#Parse the input file path for the file and its extension
		lastSlash = root.filename.rfind("/")
		nbnkName = root.filename[lastSlash+1:]
		app.setEntry("Input File Name", nbnkName)
		
		#IF: the input file is an .nbnk file, continue
		if nbnkExtensionCheck():
			validInputFile = autoDetect()
			validateInputFile()
		#ELSE: the input file isn't an .nbnk file, warn the user
		else:
			app.setEntryInvalid("Input File Name")
			app.setStatusbar("ERROR: The file loaded isn't an .nbnk file", field=0)
			validInputFile = False
			
		convertCheck()
		
#METHOD: convert
#	converts the voice file
#	PARAMETERS:
#		None
#	RETURN:
#		None
def convert(btn):
	inputFileID = str.upper(app.getRadioButton("InGender")) + "_" + app.getOptionBox("InVoice")
	outputFileID = str.upper(app.getRadioButton("OutGender")) + "_" + app.getOptionBox("OutVoice")
	confirmationMessage = "Confirm this conversion?\n" + app.getLabel("InputNameOverview") + " -> " + app.getLabel("OutputNameOverview")
	#IF: ask the user for confirmation
	if(app.okBox("Confirmation Box", confirmationMessage, parent=None)):
		outputPath = ""
		readyToConvert = False
		
		#IF: 'Save to "Output"' is on, it's ready to convert
		if(app.getCheckBox('Save to "Output"')):
			readyToConvert = True
		#ELSE: 'Save to "Output"' is off, open a file dialog for the user to save the file	
		else:
			root = Tk()
			root.withdraw()
			root.filename =  filedialog.asksaveasfilename(initialdir = "./",initialfile = (app.getLabel("OutputFileOverview")),title = "Save file",filetypes = (("nbnk files","*.nbnk"),("all files","*.*")))
			#IF: an input file was given, continue
			if(root.filename != ""):
				outputPath = root.filename
				readyToConvert = True
	
		#IF: it's ready to convert, continue
		if(readyToConvert):
			commandParameters = (app.getEntry("Input File Path:"), inputFileID, outputFileID, outputPath)
			#IF: the conversion was successful, state so
			if(MainGUIVer.Main.runCommand(commandParameters)):
				#IF: 'Save to "Output"' is on, tell the user to look in the "Output" folder
				if(app.getCheckBox('Save to "Output"')):
					successMessage = "Conversion successful!\nLook for your file in the Output folder: " + app.getLabel("OutputFileOverview")
					app.infoBox("Success Box", successMessage, parent=None)
					app.setStatusbar("Conversion successful. Look in the Output folder for: " + app.getLabel("OutputFileOverview"), field=0)
				#ELSE: 'Save to "Output"' is off, tell the user about the path
				else:
					successMessage = "Conversion successful!\nOutput file's path:\n" + outputPath
					app.infoBox("Success Box", successMessage, parent=None)
					app.setStatusbar("Conversion successful.", field=0)
			#ELSE: the conversion was unsuccessful, state so
			else:
				errorMessage = "Conversion failed!\nCheck the console to see what's wrong"
				app.errorBox("Error Box", errorMessage, parent=None)
				app.setStatusbar("WARNING: Conversion failed.", field=0)

#METHOD: manualModeChanged
#	Enable/Disables Manual Mode

#	PARAMETERS:
#		None
#	RETURN:
#		None
def manualModeChanged():
	global validInputFile
	global manualMode
	
	manualMode = app.getCheckBox("Manual Mode")
	#IF: Manual Mode is ON
	if app.getCheckBox("Manual Mode"):
		app.showLabel("Input Gender")
		app.showRadioButton("InGender")
		app.showLabel("Input Number")
		app.showOptionBox("InVoice")
		app.showButton("Auto Detect")
		validInputFile = nbnkExtensionCheck()
		
	#ELSE: Manual Mode is OFF
	else:
		app.hideLabel("Input Gender")
		app.hideRadioButton("InGender")
		app.hideLabel("Input Number")
		app.hideOptionBox("InVoice")
		app.hideButton("Auto Detect")

	validInputFile = autoDetect()
	validateInputFile()	
	convertCheck()

# GUI SECTION

app.setResizable(canResize=False)
app.setBg("white", override=True)
app.setLabelFont(weight="bold")

# Top Row - Input File Path
# Shows the path to the input file
app.setStretch('column')
app.setSticky('news')
app.addLabelEntry("Input File Path:", row=0, column=0, colspan=2)
app.disableEntry("Input File Path:")
# Top Row




app.setStretch('both')

# Left Section - Voice File Information
# Options for the input and output voice files
app.startFrame("VoiceInfoSection", row=1, column=0)


# Top Left Section - Input Voice
# Options for the input voice file
app.startLabelFrame("Input Voice", row=1, column=0)
app.setFont(12)

# Input Voice - File Input
# Allows loading a voice file
app.addLabel("Input File Label", "File:", 0, 0)
app.addValidationEntry("Input File Name", 0, 1, colspan=2)
app.disableEntry("Input File Name")
app.addButton("Load File", loadFile, 1, 1)
app.setButtonTooltip("Load File", "Load the voice file to be converted")

app.addCheckBox("Manual Mode", 1, 2)
app.setCheckBoxTooltip("Manual Mode", "Allows manual control over the input voice's information\nWARNING: This unrestricts checking the loaded file.\nAny file with an '.nbnk' extension will be considered valid")
app.setCheckBoxChangeFunction("Manual Mode", manualModeChanged)

# Input Voice - Gender
# Chooses the input voice file's gender
app.addLabel("Input Gender", "Gender:", 2, 0)
app.addRadioButton("InGender", "Female", 2, 1)
app.addRadioButton("InGender", "Male", 2, 2)
app.setRadioButtonChangeFunction("InGender", updateInputOverview)

# Input Voice - Number
# Chooses the input voice file's voice number
app.addLabel("Input Number", "Voice:", 3, 0)
inVoiceList = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"] 
app.addOptionBox("InVoice", inVoiceList, 3, 1)
app.setOptionBoxChangeFunction("InVoice", updateInputOverview)

app.addButton("Auto Detect", autoDetect, 3, 2)
app.setButtonTooltip("Auto Detect", "Auto assigns the gender and number based on the file name")

app.hideLabel("Input Gender")
app.hideRadioButton("InGender")
app.hideLabel("Input Number")
app.hideOptionBox("InVoice")
app.hideButton("Auto Detect")
		
app.stopLabelFrame()
# Top Left Section


#Bottom Left Section - Output Voice
#	Options for the output voice file
app.startLabelFrame("Output Voice", row=2, column=0)
app.setFont(12)

#Output Voice - Gender
#	Chooses the output voice file's gender
app.addLabel("Output Gender", "Gender:", 0, 0)
app.addRadioButton("OutGender", "Female", 0, 1)
app.addRadioButton("OutGender", "Male", 0, 2)
app.setRadioButtonChangeFunction("OutGender", updateOutputOverview)

#Output Voice - Number
#	Chooses the output voice file's voice number
app.addLabel("Output Number", "Voice:", 1, 0)
outVoiceList = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"] 
app.addOptionBox("OutVoice", inVoiceList, 1, 1)
app.setOptionBoxChangeFunction("OutVoice", updateOutputOverview)

app.addCheckBox('Save to "Output"', 1, 2)
app.setCheckBoxTooltip('Save to "Output"', 'Disables the "Save file" dialog.\nThe output file will save into the "Output" folder')

app.stopLabelFrame()
# Bottom Left Section


app.stopFrame()
# Left Section




#Right Section - Voice Preview
#	Shows an overview of the input and output voice files
app.startFrame("VoiceOverviewSection", row=1, column=1)

app.startLabelFrame("Overview")

app.addLabel("InputNameOverview", "Female Voice 1")
app.addLabel("InputFileOverview", "pl_act_vo_f_11_m.nbnk")
app.addLabel("To", "to")
app.addLabel("OutputNameOverview", "Female Voice 1")
app.addLabel("OutputFileOverview", "pl_act_vo_f_11_m.nbnk")

app.stopLabelFrame()

app.stopFrame()
#Right Section




#Bottom Left Section - Asset Info
#	Shows if the other assets are detected
app.startFrame("Asset Info", row=2, column=0)

app.addLabel("Wwise Label", "Wwiseutil: OK", 0, 0)
app.addLabel("DB Label", "DB Version: ???", 0, 1)

#Check if wwiseutil.exe is present
otherAssetsCheck()

app.stopFrame()
#Bottom Left Section




#Bottom Right Section - Convert Button
#	Button for converting
app.startFrame("Final", row=2, column=1)

app.addButton("CONVERT", convert)
app.disableButton("CONVERT")

app.stopFrame()
#Bottom Right Section




#Bottom Row - Status Bar
#	Provides various information and warnings
app.addStatusbar(header="", fields=1)
#IF: wwiseutil.exe is present, the program can run
if(otherAssetsFound):
	app.setStatusbar("Load a file with the 'Load File' button!", field=0)
#ELSE: wwiseutil.exe wasn't found, warn the user
else:
	app.setStatusbar("WARNING: Couldn't find Wwiseutil.exe! It should be in the same directory as this program", field=0)
#Bottom Row




# start the GUI
app.go()