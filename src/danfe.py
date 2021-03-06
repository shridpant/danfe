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
from src.convert.toList import ToList
from src.convert.toDict import ToDict
from src.convert.toJSON import ToJSON
from src.convert.toCSV import ToCSV

class Danfe():
	def __init__(self, file_path, logger):
		self.logger = logger
		self.file_path = file_path
		self.file_extension = self.find_extension()
		self.logger.log(Danfe.__name__)

	def find_extension(self):
		filename, file_extension = os.path.splitext(self.file_path)
		return file_extension.lower().lstrip(".")
	
	def file_existence(self):
		if os.path.exists(self.file_path):
			self.logger.log("File exists at " + self.file_path, 0, Danfe.file_existence.__name__, 0)
			return True
		else:
			self.logger.log("File doesn't exist", 400, Danfe.file_existence.__name__, -1)
			return False

	def to_list(self):
		if self.file_existence():
			convert_to_list = ToList(self.file_path, self.file_extension, self.logger)
			converted_file = convert_to_list.convert()
			if not converted_file:
				self.logger.log("List conversion failed", 500, Danfe.to_list.__name__, -1)
				return None
			self.logger.log("List conversion successful", 0, Danfe.to_list.__name__, 0)
			return converted_file
		else:
			self.logger.log("File couldn't be read", 400, Danfe.to_list.__name__, -1)
			return None

	def to_dict(self):
		if self.file_existence():
			convert_to_dict = ToDict(self.file_path, self.file_extension, self.logger)
			converted_file = convert_to_dict.convert()
			if not converted_file:
				self.logger.log("Dictionary conversion failed", 500, Danfe.to_dict, -1)
				return None
			self.logger.log("Dictionary conversion successful", 0, Danfe.to_dict.__name__, 0)
			return converted_file
		else:
			self.logger.log("File couldn't be read", 400, Danfe.to_dict.__name__, -1)
			return None

	def to_JSON(self):
		if self.file_existence():
			convert_to_JSON = ToJSON(self.file_path, self.file_extension, self.logger)
			converted_file = convert_to_JSON.convert()
			if not converted_file:
				self.logger.log("JSON conversion failed", 500, Danfe.to_JSON.__name__, -1)
				return None
			self.logger.log("JSON conversion successful", 0, Danfe.to_JSON.__name__, 0)
			return converted_file
		else:
			self.logger.log("File couldn't be read", 400, Danfe.to_JSON.__name__, -1)
			return None

	def to_CSV(self):
		if self.file_existence():
			convert_to_CSV = ToCSV(self.file_path, self.file_extension, self.logger)
			converted_file = convert_to_CSV.convert()
			if not converted_file:
				self.logger.log("CSV conversion failed", 500, Danfe.to_CSV.__name__, -1)
				return None
			self.logger.log("CSV Conversion successful", 0, Danfe.to_CSV.__name__, 0)
			return converted_file
		else:
			self.logger.log("File couldn't be read", 400, Danfe.to_CSV.__name__, -1)
			return None