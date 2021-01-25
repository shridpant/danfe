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

import json
import tempfile
import subprocess
from datetime import datetime

class Logger:
    def __init__(self, verbose = None):
        self.verbose = verbose
        self.root_path = tempfile.mkdtemp()
        self.file_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.log_path = str(self.root_path) + "/log_" + self.file_name + ".txt"
        self.status_path = str(self.root_path) + "/status_" + self.file_name + ".json"
        self.status_message = []
        self.make_files()

    def log(self, log_message=None, log_code=None, status_message=None, status_code=None, display=False):
        if status_code or status_message:
            self.status(status_message, status_code)
        if log_message:
            log_message = self.append_message(log_message, log_code)
            if display == True:
                print(log_message)            
            elif self.verbose or log_code:
                print(log_message)
            with open(self.log_path, "a") as log_file:
                log_file.write(log_message + "\n")

    def status(self, key, code):
        message = {str(key):code}
        self.status_message.append(message)
        if key == "__main__":
            with open(self.status_path, "w", encoding='utf-8') as status_file:
                json.dump(self.status_message, status_file)

    def append_message(self, message, log_code=None):
        message = str(message)
        if log_code == 400:
            message = "BAD REQUEST: " + message
        elif log_code == 500:
            message = "FATAL: " + message
        elif self.verbose:
            message = "(message:) " + message
        return message

    def make_files(self):
        subprocess.Popen(["touch", self.log_path], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        subprocess.Popen(["touch", self.status_path], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        self.log(">> logs & status stored at: " + self.root_path, display=True)