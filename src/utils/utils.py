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

import os, subprocess

class ErrorHandler(Exception):
    def __init__(self, code, *args):
        self.code = code
        self.args = args

    def __str__(self):
        return ('Error: %s\n:' % self.code) + str(self.args)

class Save():
    def __init__(self, result, location, convert_to, logger):
        self.result = result 
        self.location = location 
        self.convert_to = convert_to
        self.logger = logger
        self.logger.log(Save.__name__)

    def save(self):
        try:
            if self.convert_to != "json" and self.convert_to != "csv":
                self.convert_to = ""
            else:
                self.convert_to = "." + self.convert_to
            if os.path.isdir(self.location):
                self.location = self.location + "/output" + self.convert_to
            subprocess.Popen(["touch", self.location], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            with open(self.location, 'w') as output:
                output.write(str(self.result))
            self.logger.log(">> output file at " + self.location, 0, Save.save.__name__, 0, display=True)
        except Exception as e:
            self.logger.log(str(e), 500, Save.save.__name__, -1)