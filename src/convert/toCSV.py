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
import json, csv, re, io, ast

class ToCSV():
    def __init__(self, file_path, file_extension, logger):
        self.file_path = file_path
        self.file_extension = file_extension
        self.logger = logger
        self.logger.log("Inside toCSV.py")

    def convert(self):
        converted_file = io.StringIO()
        with open(self.file_path,'r') as file_to_open:
            try:
                if self.file_extension == "json":
                    file_contents = json.load(file_to_open)
                    csv_writer = csv.writer(converted_file)
                    csv_writer.writerow(file_contents[0].keys())
                    for each_row in file_contents:
                        csv_writer.writerow(each_row.values())
                elif self.file_extension == "csv":
                    file_contents = csv.reader(file_to_open)
                    csv_writer = csv.writer(converted_file)
                    for each_row in file_contents:
                        csv_writer.writerow(each_row)
                elif self.file_extension == "ora":
                    csv_writer = csv.writer(converted_file)
                    file_contents = file_to_open.read()
                    configRegX = re.compile(r"\*\..+=.+")
                    data_keys = []
                    data_values = []
                    for match in configRegX.finditer(file_contents):
                        data_keys.append(match.group().split('=')[0].lstrip('*\.'))
                        data_values.append(";".join([name.strip('\'') for name in match.group().split('=')[1].split(',')]))
                    csv_writer.writerow(data_keys)
                    csv_writer.writerow(data_values)
                else:
                    file_contents = file_to_open.read()
                    try:
                        file_contents = ast.literal_eval(file_contents)
                    except Exception as e:
                        self.logger.log(str(e), 500)
                    if isinstance(file_contents, list):
                        csv_writer = csv.writer(converted_file)
                        for each_row in file_contents:
                            csv_writer.writerow(each_row)
                    elif isinstance(file_contents, dict):
                        csv_writer = csv.writer(converted_file)
                        csv_writer.writerow(file_contents[0].keys())
                        for each_row in file_contents:
                            csv_writer.writerow(each_row.values())
                    else:
                        self.logger.log("Unsupported file type", 400)
                        return None       
            except Exception as e:
                self.logger.log(str(e)) 
                self.logger.log("CSV conversion error") 
                return None       
        return converted_file.getvalue()
