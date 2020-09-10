# To support- json, csv, xml
# To add a logger
import os
import re
import json
import csv
from datetime import datetime
import subprocess

def init():
	global filePath
	global logPath
	rootPath = os.getcwd()
	filePath = rootPath + "/sample-files/" + "sample.csv"
	now = datetime.now()
	logPath = rootPath + "/log/" + now.strftime("%Y-%m-%m-%H-%M") + ".txt"
	subprocess.Popen(["touch", logPath], stdout=subprocess.PIPE, stdin=subprocess.PIPE)

def logger(message1, message2 = None, message3 = None):
	with open(logPath, "a") as logFile:
		logFile.write(str(message1) + "\n")

def fileExistence():
	if os.path.exists(filePath):
		logger("File Exists at " + filePath)
		return True
	else:
		logger("File doesn't exist")
		return False

def fileParser(fileType):
	parsedFile = {}
	if fileExistence():
		fileToOpen = open(filePath, 'r')
		fileContents = fileToOpen.read()
		if fileType == "json":
			fileContents = fileToOpen.read()
			parsedFile = json.loads(fileContents)
		elif fileType == "csv": #todo
			fileContents = csv.DictReader(fileToOpen)
			print(fileContents)
			for row in fileContents:
				for column, value in row.items():
					parsedFile.setdefault(column, []).append(value)
		else:
			fileContents = fileToOpen.read()
			configRegX = re.compile(r"\*\..+=.+")
			for match in configRegX.finditer(fileContents):
		            keyParameter = match.group().split('=')[0].lstrip('*\.')
		            valueParameter = [name.strip('\'') for name in match.group().split('=')[1].split(',')]
		            parsedFile[keyParameter] = valueParameter
		return parsedFile
	else:
		logger("Error")
		return None

# INIT global/main variables
init()
# calling the parsing function
parsedFile = fileParser("csv")
# display the output
logger(parsedFile)
print(parsedFile)
