import os
from src.conversion.toList import ToList

class Parser():
	def __init__(self, file_path, logger):
		self.logger = logger
		self.file_path = file_path
		self.file_extension = self.find_extension()
		self.logger.log("In parser.py")

	def find_extension(self):
		filename, file_extension = os.path.splitext(self.file_path)
		return file_extension.lower().lstrip(".")
	
	def file_existence(self):
		if os.path.exists(self.file_path):
			self.logger.log("File exists at " + self.file_path)
			return True
		else:
			self.logger.log("File doesn't exist")
			return False

	def to_list(self):
		if self.file_existence():
			convert_to_list = ToList(self.file_path, self.file_extension, self.logger)
			parsed_file = convert_to_list.convert()
			if not parsed_file:
				self.logger.log("List conversion failed")
			return parsed_file
		else:
			self.logger.log("Parsing failed")
			return None