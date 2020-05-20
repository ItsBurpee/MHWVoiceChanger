import sqlite3

conn = sqlite3.connect('MHWCharacterVoices.db')
c = conn.cursor()

#MODULE: Query
#	Module for all SQLite queries

#METHOD: getVersion
#	Gets the database version number from the database
#	PARAMETERS:
#		None
#	RETURN:
#		The database version number
def getVersion():
	query = "SELECT Version_num FROM Version"
	c.execute(query)
	return c.fetchone()
	
#METHOD: identifyFileName
#	Gets the file information from the file name
#	PARAMETERS:
#		targetFileName - The file name
#	RETURN:
#		The file information assigned to the file name
def identifyFileName(targetFileName):
	query = "SELECT * FROM Main WHERE File_name = ?"
	c.execute(query, targetFileName)
	return c.fetchone()

#METHOD: identifyFileID
#	Gets the file information from the file ID
#	PARAMETERS:
#		targetFileID - The file name
#	RETURN:
#		The file information assigned to the file ID
def identifyFileID(targetFileID):
	query = "SELECT * FROM Main WHERE File_ID = ?"
	c.execute(query, targetFileID)
	return c.fetchone()
	
#METHOD: wemToBnk
#	Gets the action type and bank number from a wem number
#	PARAMETERS:
#		targetFileID - The file ID
#		targetWemNumber - The wem number
#	RETURN:
#		The action type and bank number assigned to the wem number	
def wemToBnk(targetFileID, targetWemNumber):
	#TRY: getting the wem number's information
	try:
		query = "SELECT Action_type, Bank_number FROM " + targetFileID + " WHERE Wem_number = " + targetWemNumber
		c.execute(query)
		return c.fetchone()
	#EXCEPT: the targetFileID is currently unsupported
	except:
		print("\nERROR: One of the tables are unsupported")
		return None

#METHOD: bnkToWem
#	Gets the wem number from the action type and bank number
#	PARAMETERS:
#		targetFileID - The file ID
#		targetActionType - The action type
#		targetBankNumber - The bank number
#	RETURN:
#		The wem number assigned to the action type and bank number
def bnkToWem(targetFileID, targetActionType, targetBankNumber):
	#TRY: getting the wem number with the given information
	try:
		query = "SELECT Wem_number FROM " + targetFileID + " WHERE Action_type = ? AND Bank_number = ?"
		c.execute(query, (targetActionType, targetBankNumber))
		return c.fetchone()
	#EXCEPT: the targetFileID is currently unsupported
	except:
		print("\nERROR: One of the tables are unsupported")
		return None