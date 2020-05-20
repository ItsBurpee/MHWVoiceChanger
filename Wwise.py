import os
import subprocess
from shutil import copyfile

#MODULE: Wwise
#	Module for Wwiseutil commands

#METHOD: unpackNbnk
#	Unpacks the target Nbnk file
#	PARAMETERS:
#		targetFileName - The Nbnk file path
#	RETURN:
#		None
def unpackNbnk(targetFilePath):
	#TRY: Making a new directory for the input file wems
	try:
		os.mkdir("inputWems")
	#EXCEPT: The directory already exists
	except FileExistsError:
		#FOR: Delete each file in the directory
		for wem in os.listdir("inputWems"):
			src = 'inputWems\\' + wem
			os.remove(src)
	
	#Copy the target file to the new directory
	#This is used to make wwiseutil work
	lastSlash = targetFilePath.rfind("/")
	targetFileName = targetFilePath[lastSlash+1:]
	currentDir = os.path.abspath(os.getcwd())+"\\inputWems\\"+targetFileName
	copyfile(targetFilePath, currentDir)
	
	#Run the wwiseutil command to unpack the nbnk
	command = 'wwiseutil -u -f "inputWems"\\' + targetFileName + ' -o "inputWems"\\'
	subprocess.call(command)
	
	#Remove the target file after unpacking it
	os.remove(currentDir)
	
#METHOD: repackNbnk
#	Repacks the new Nbnk file
#	PARAMETERS:
#		newTargetFileName - The new Nbnk file name
#	RETURN:
#		None
def repackNbnk(newTargetFileName):
	#TRY: Making a new directory for the output file
	#This is used to make wwiseutil work
	try:
		os.mkdir("Output")
	#EXCEPT: The directory already exists, pass
	except:
		pass
	#TRY: Removing the old file if it exists
	try:
		src = 'Output\\' + newTargetFileName
		os.remove(src)
	#EXCEPT: The old file doesn't exist, pass
	except:
		pass

	#Run the wwiseutil command to pack the nbnk
	command = 'wwiseutil -r -f EmptyNbnks\\'+ newTargetFileName + ' -o Output\\' + newTargetFileName + ' -t inputWems\\'
	subprocess.call(command)
	
	#TRY: Deleting the directory for the input file wems
	try:
		#FOR: Delete each file in the directory
		for wem in os.listdir("inputWems"):
			src = 'inputWems\\' + wem
			os.remove(src)
		os.rmdir("inputWems")
	#EXCEPT: Something went wrong when trying to delete the directory, print an error
	except:
		print("Error during delete")
	