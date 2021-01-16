import os
import json, csv, re

class ToList():
	def __init__(self, file_path, file_extension, logger):
		self.file_path = file_path
		self.file_extension = file_extension
		self.logger = logger
		self.logger.log("Inside toList.py")

	def convert(self):
		parsed_file = []
		with open(self.file_path,'r') as file_to_open:
			if self.file_extension == "json":
				file_contents = file_to_open.read()
				json_dict = json.loads(file_contents)
				parsed_file = self.convert_helper(json_dict, "list")
			elif self.file_extension == "csv":
				file_contents = csv.DictReader(file_to_open)
				for row in file_contents:
					each_row = {}
					for key, value in row.items():
						each_row[key] = value
					parsed_file.append(each_row)
			elif self.file_extension == "ora":
				file_contents = file_to_open.read()
				configRegX = re.compile(r"\*\..+=.+")
				for match in configRegX.finditer(file_contents):
					keyParameter = match.group().split('=')[0].lstrip('*\.')
					valueParameter = [name.strip('\'') for name in match.group().split('=')[1].split(',')]
					parsed_file.append([keyParameter, valueParameter])
			else:
				self.logger.log("Unknown file type", 400)
				parsed_file = None
		self.logger.log(parsed_file)
		return parsed_file

	def convert_helper(self, data_structure, return_type):
		if (return_type == "list"):
			result_list = []
			if isinstance(data_structure, dict):
				for key, value in data_structure.items():
					if isinstance(value, dict):
						value = self.convert_helper(value, "list")
					result_list.append([key, value])
			return result_list
		if (return_type == "dict"):
			return_dict = {}
			try:
				if isinstance(data_structure, list):
					for key, value in list:
						if isinstance(value, list):
							value = self.convert_helper(value, "dict")
						return_dict[key] = value
					return return_dict
			except:
				self.logger.log("List values aren't in pairs", 400)
				return None
		else:
			pass