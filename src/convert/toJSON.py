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

import csv, json, re, ast
from xml.etree import ElementTree as ET

class ToJSON():
    def __init__(self, file_path, file_extension, logger):
        self.file_path = file_path
        self.file_extension = file_extension
        self.logger = logger
        self.logger.log(ToJSON.__name__)

    def convert(self):
        try:
            converted_file = {}
            with open(self.file_path,'r') as file_to_open:
                if self.file_extension == "csv":
                    file_contents = csv.DictReader(file_to_open)
                    counter = 0
                    for row in file_contents:
                        each_row = {}
                        for key, value in row.items():
                            each_row[key] = value
                        converted_file[counter] = each_row
                        counter += 1
                    converted_file = json.dumps(converted_file)
                elif self.file_extension == "ora":
                    file_contents = file_to_open.read()
                    configRegX = re.compile(r"\*\..+=.+")
                    for match in configRegX.finditer(file_contents):
                        key_parameter = match.group().split('=')[0].lstrip('*\.')
                        value_parameter = {name.strip('\'') for name in match.group().split('=')[1].split(',')}
                        converted_file[key_parameter] =  value_parameter
                elif self.file_extension == "json":
                    converted_file = json.load(file_to_open)
                elif self.file_extension == "xml":
                    file_contents = ET.parse(file_to_open)
                    root_element = file_contents.getroot()
                    converted_file = self.convert_helper(root_element)
                else:
                    file_contents = ast.literal_eval(file_to_open.read())
                    if isinstance(file_contents, dict):
                        counter = 0
                        for row in file_contents:
                            each_row = {}
                            for key, value in row.items():
                                each_row[key] = value
                            converted_file[counter] = each_row
                            counter += 1
                        converted_file = json.dumps(converted_file)
                    elif isinstance(file_contents, list):
                        converted_file = self.convert_helper(file_contents)
                    else:
                        self.logger.log("Unsupported file/data type", 400, ToJSON.convert.__name__, -1)
                        return None
            self.logger.log(status_message = ToJSON.convert.__name__, status_code = 0)
            return converted_file
        except Exception as e:
            self.logger.log(str(e), 500, ToJSON.convert.__name__, -1)

    def convert_helper(self, data_structure):
        try:
            result_json = {}
            if isinstance(data_structure, list):
                for key, value in list:
                    if isinstance(value, list):
                        value = self.convert_helper(value)
                    result_json[key] = value
                result_json = json.dumps(result_json)
            elif isinstance(data_structure, ET.Element):
                def xml_helper(node, numbering_path="", numbering_helper=None):
                    return_json = {}
                    if numbering_helper == None:
                        numbering_helper = {}
                    name_prefix = numbering_path + ("/" if numbering_path else "") + node.tag
                    numbers = list()
                    for similar_name in numbering_helper.keys():
                        if similar_name.startswith(name_prefix):
                            numbers.append(int(similar_name[len(name_prefix):].split("/")[0]))
                    if not numbers:
                        numbers.append(0)
                    name_prefix = name_prefix + str(max(numbers) + 1)
                    numbering_helper[name_prefix] = node.text
                    key_name = node.tag + str(max(numbers) + 1)
                    for childnode in list(node):
                        return_json.setdefault(key_name, []).append(xml_helper(childnode, name_prefix, numbering_helper))
                    if not list(node):
                        return_json.setdefault(key_name, []).append(node.text.strip("\""))
                    return return_json
                result_json = json.dumps(xml_helper(data_structure))
            else:
                result_json = None
            return result_json
        except Exception as e:
            self.logger.log(str(e), 500, ToJSON.convert_helper.__name__, -1)
            return None