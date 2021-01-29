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

import json, csv, re, io, ast
from xml.etree import ElementTree as ET

class ToCSV():
    def __init__(self, file_path, file_extension, logger):
        self.file_path = file_path
        self.file_extension = file_extension
        self.logger = logger
        self.logger.log(ToCSV.__name__)

    def convert(self):
        try:
            converted_file = io.StringIO()
            with open(self.file_path,'r') as file_to_open:
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
                elif self.file_extension == "xml":
                    file_contents = ET.parse(file_to_open)
                    root_element = file_contents.getroot()
                    converted_file = self.convert_helper(root_element)
                else:
                    file_contents = ast.literal_eval(file_to_open.read())
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
                        self.logger.log("Unsupported file/data type", 400, ToCSV.convert.__name__, -1)
                        return None    
            self.logger.log(status_message = ToCSV.convert.__name__, status_code = 0)
            return converted_file.getvalue()   
        except Exception as e:
            self.logger.log(str(e), 500, ToCSV.convert.__name__, -1) 
            return None      

    def convert_helper(self, data_structure):
        try:
            result_csv = io.StringIO()
            csv_writer = csv.writer(result_csv)
            if isinstance(data_structure, ET.Element):
                def xml_helper(node, numbering_path="", return_dict=None):
                    if return_dict == None:
                        return_dict = {}
                    name_prefix = numbering_path + ("/" if numbering_path else "") + node.tag
                    numbers = list()
                    for similar_name in return_dict.keys():
                        if similar_name.startswith(name_prefix):
                            numbers.append(int(similar_name[len(name_prefix):].split("/")[0]))
                    if not numbers:
                        numbers.append(0)
                    key_name = name_prefix + str(max(numbers) + 1)
                    return_dict[key_name] = "" if node.text.isspace() else node.text.strip("\"")
                    for childnode in list(node):
                        xml_helper(childnode, key_name, return_dict)
                    return return_dict
                result_dict = xml_helper(data_structure)
                csv_writer.writerow(result_dict.keys())
                csv_writer.writerow(result_dict.values())
            else:
                result_csv = None
            return result_csv
        except Exception as e:
            self.logger.log(str(e), 500, ToCSV.convert_helper.__name__, -1)
            return None 
