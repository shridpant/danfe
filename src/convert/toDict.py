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

class ToDict():
    def __init__(self, file_path, file_extension, logger):
        self.file_path = file_path
        self.file_extension = file_extension
        self.logger = logger
        self.logger.log("Inside toDict.py")

    def convert(self):
        converted_file = {}
        with open(self.file_path,'r') as file_to_open:
            if self.file_extension == "json":
                file_contents = file_to_open.read()
                converted_file = json.loads(file_contents)
            elif self.file_extension == "csv":
                file_contents = csv.DictReader(file_to_open)
                counter = 0
                for row in file_contents:
                    each_row = {}
                    for key, value in row.items():
                        each_row[key] = value
                    converted_file[counter] = each_row
                    counter += 1
            elif self.file_extension == "ora":
                file_contents = file_to_open.read()
                configRegX = re.compile(r"\*\..+=.+")
                for match in configRegX.finditer(file_contents):
                    key_parameter = match.group().split('=')[0].lstrip('*\.')
                    value_parameter = {name.strip('\'') for name in match.group().split('=')[1].split(',')}
                    converted_file[key_parameter] =  value_parameter
            else:
                self.logger.log("Unsupported file type", 400)
                return None
        return converted_file

    def convert_helper(self, data_structure):
        result_dict = {}
        if isinstance(data_structure, list):
            try:
                for key, value in list:
                    if isinstance(value, list):
                        value = self.convert_helper(value)
                    result_dict[key] = value
            except:
                self.logger.log("List values aren't in pairs", 500)
                return None
        return result_dict