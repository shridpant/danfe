import os
import subprocess
from datetime import datetime

class ErrorDetail:
    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message

class Logger:
    def __init__(self, verbose = None):
        self.fatal = 0
        self.verbose = verbose
        self.root_path = os.getcwd()
        self.log_path = self.root_path + "/log/" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".txt"
        subprocess.Popen(["touch", self.log_path], stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    def log(self, message, fatal=None):
        if fatal == 400:
            self.fatal = fatal
            message = "BAD REQUEST: " + message
        if self.verbose:
            print("message: ", message)
        with open(self.log_path, "a") as log_file:
            log_file.write(str(message) + "\n")