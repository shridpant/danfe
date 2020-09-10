# To support- json, csv, xml
# To add a logger
import os
import re
import json
import datetime
import subprocess

def init():
	global logPath
	now = datetime.datetime.now()
	logPath = "log/" + str(now) + ".txt"
	subprocess.Popen(["touch", logPath], stdout=subprocess.PIPE)

def logger(message1, message2 = None, message3 = None):
	with open(logPath, "a") as logFile:
		logFile.write(str(message1) + "\n")

def fileExistence():
	if os.path.exists(filePath):
		logger("File Exists", filePath)
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
			parsedFile = json.loads(fileContents)
		else:
			configRegX = re.compile(r"\*\..+=.+")
			for match in configRegX.finditer(fileContents):
		            keyParameter = match.group().split('=')[0].lstrip('*\.')
		            valueParameter = [name.strip('\'') for name in match.group().split('=')[1].split(',')]
		            parsedFile[keyParameter] = valueParameter
		return parsedFile
	else:
		logger("Error")
		print("Error")
		return None
# INIT global/main variables
init()
rootPath="/home/shrid/Documents/bash-parsers/sample-files/"
filePath = rootPath + "sample.json"
# calling the parsing function
parsedFile = fileParser("json")
# displaying the output
logger(parsedFile)
print(parsedFile)


