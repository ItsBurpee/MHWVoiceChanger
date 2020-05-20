import os
import sys
from shutil import copyfile
#copyfile(src, dst)

import Query
import Wwise

#Parameters: "input file path" "input file ID" "output file ID" "output file path"
class Main:
	
	def runCommand(parameters):
		#Get the input file path and ID
		inputPath = parameters[0]
		input = (parameters[1],)
		inputInfo = Query.identifyFileID(input)

		print()
		validFiles = True
		completedConversion = False
		
		#IF: the input file path is valid, check there's an extension
		if os.path.isfile(inputPath):
			extensionDot = inputPath.rfind(".")
			inputFileExtension = inputPath[extensionDot:]
			#IF: the input file has an extension, check if it's .nbnk
			if inputFileExtension == ".nbnk":
				print("Target file: %s" % inputPath)
			else:
				print("ERROR: Invalid input file extension. Must be .nbnk")
				validFiles = False					
		#ELSE: the input file path is invalid
		else:
			print("ERROR: Invalid input file path")
			validFiles = False		
			
		#TRY: Checking if the input file ID is valid
		try:
			print("\n%s Voice %d" % (inputInfo[1], inputInfo[2]))
			inputFileID = inputInfo[0]
		#EXCEPT: If the input file ID is invalid
		except TypeError:
			print("ERROR: Invalid input file ID")
			validFiles = False

		#Get the output file ID
		output = (parameters[2],)
		outputInfo = Query.identifyFileID(output)
		
		#TRY: Checking if the output file ID is valid
		try:
			print("to \n%s Voice %d \n" % (outputInfo[1], outputInfo[2]))
			outputFileID = outputInfo[0]
			outputFileName = outputInfo[3]
		#EXCEPT: If the output file ID is invalid
		except TypeError:
			print("ERROR: Invalid output file ID")
			validFiles = False
		
		#IF: Both the input and output files are valid, continue
		if validFiles:
			#Tell Wwiseutil to unpack the input file
			Wwise.unpackNbnk(parameters[0])
			
			try:
				#FOR: Each wem in the input file directory, renumber them
				for wem in os.listdir("inputWems"):
					#Remove the .nbnk from the end
					extensionDot = wem.rfind(".")
					wemNumber = wem[:extensionDot]
					#IF: There's a leading 0 (01, 02, ...), remove it
					if wemNumber[0] is "0":
						wemNumber = wemNumber[1:]
					#Get the wem number's information
					wemInfo = Query.wemToBnk(inputFileID, wemNumber)
					#Use that information to get the output file's wem number and renumber
					outputNumber = Query.bnkToWem(outputFileID, wemInfo[0], wemInfo[1])
					outputWem = str(outputNumber[0]) + ".wem_"
					#print("%s -> %s" % (wemNumber, outputNumber[0]))
					src = 'inputWems\\' + wem
					dst = 'inputWems\\' + outputWem
					os.rename(src,dst)
				#FOR: Each new wem in the input file directory, remove the "_" at the end
				for wem in os.listdir("inputWems"):
					src = 'inputWems\\' + wem
					dst = 'inputWems\\' + wem[:-1]
					os.rename(src,dst)
					
				#Tell Wwiseutil to repack to the output file
				Wwise.repackNbnk(outputFileName)
				completedConversion = True
			except TypeError:
				print("\nERROR: Bad number in the input ID table. Check for duplicates: %s" % (wemNumber))
				validFiles = False
			except FileExistsError:
				print("\nERROR: Bad number in the output ID table. Check for duplicates: %d" % (outputNumber[0]))
				validFiles = False	
				
			#TRY: Checking if the file was successfully created
			try:
				outputDir = os.listdir(".\\Output")
				#TRY: Looking for the output file
				try:
					outputDir.index(outputFileName)
					if completedConversion:
						print("\nConversion successful!")
						#IF: an output path was given, try to move the file
						if(parameters[3] != ""):
							print("\nTarget Output Path: %s" % parameters[3])
							#TRY: copying the file to the given output path
							try:
								outputFilePath = os.path.abspath(os.getcwd())+"\\Output\\"+outputFileName
								copyfile(outputFilePath, parameters[3])
								#Then delete the version that's in "Output"
								os.remove(outputFilePath)
								print("\nOutput File move successful!")
							#EXCEPT: the output file doesn't exist, print an error
							except:
								print("\nOutput File move failed!")
								return False
						return True
					else:
						raise TypeError
				#EXCEPT: the output file doesn't exist, print an error
				except ValueError:
					raise TypeError
			#EXCEPT: The output folder wasn't created, the error occurred before repacking
			except TypeError:
				print("\nConversion failed!")
			return False
			