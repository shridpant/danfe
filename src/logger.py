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
import subprocess
import tempfile
from datetime import datetime

class Logger:
    def __init__(self, verbose = None):
        self.verbose = verbose
        self.root_path = tempfile.mkdtemp()
        self.log_path = str(self.root_path) + "/" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".txt"
        self.make_log()

    def log(self, message, fatal=None, display=False):
        message = str(message)
        if fatal == 400:
            message = "BAD REQUEST: " + message
        if fatal == 500:
            message = "FATAL: " + message
        if self.verbose or fatal:
            print("message:", message)
        elif display == True:
            print(message)
        with open(self.log_path, "a") as log_file:
            log_file.write(message + "\n")

    def make_log(self):
        subprocess.Popen(["touch", self.log_path], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        self.log(">> logs stored at: " + self.log_path, display=True)
