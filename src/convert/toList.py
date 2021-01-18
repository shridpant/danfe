# Danfe- One stop solution to all your file transformation needs!
# Copyright (C) 2020-2021  Shrid Pant

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>

import os
import json, csv, re

class ToList():
	def __init__(self, file_path, file_extension, logger):
		self.file_path = file_path
		self.file_extension = file_extension
		self.logger = logger
		self.logger.log("Inside toList.py")

	def convert(self):
		converted_file = []
		with open(self.file_path,'r') as file_to_open:
			if self.file_extension == "json":
				file_contents = file_to_open.read()
				json_dict = json.loads(file_contents)
				converted_file = self.convert_helper(json_dict)
			elif self.file_extension == "csv":
				file_contents = csv.DictReader(file_to_open)
				for row in file_contents:
					each_row = []
					for key, value in row.items():
						each_row.append([key, value])
					converted_file.append(each_row)
			elif self.file_extension == "ora":
				file_contents = file_to_open.read()
				configRegX = re.compile(r"\*\..+=.+")
				for match in configRegX.finditer(file_contents):
					keyParameter = match.group().split('=')[0].lstrip('*\.')
					valueParameter = [name.strip('\'') for name in match.group().split('=')[1].split(',')]
					converted_file.append([keyParameter, valueParameter])
			else:
				self.logger.log("Unsupported file type", 400)
				converted_file = None
		return converted_file

	def convert_helper(self, data_structure):
		result_list = []
		if isinstance(data_structure, dict):
			try:
				for key, value in data_structure.items():
					if isinstance(value, dict):
						value = self.convert_helper(value)
					result_list.append([key, value])
			except:
				self.logger.log("Dict to list conversion error", 500)
				return None
		return result_list