#!/usr/bin/env python3

#To execute: ./main.py -v sample-files/sample.json

import os
import sys
import argparse
from src.parser import Parser
from src.logger import Logger

def main():
    file_path, verbose, convert_to = parse_arguments()
    parser_logger = Logger(verbose)
    file_object = Parser(file_path, parser_logger)
    result = convert_file(file_object, convert_to, parser_logger)
    print(result)
    input("Press enter to continue ...")

def convert_file(file_to_parse, convert_to, logger):
    if convert_to == "list":
        parsed_file = file_to_parse.to_list()
    else:
        logger.log("Unknown file option", 400)
        parsed_file = None
    return parsed_file

def parse_arguments():
    PARSER = argparse.ArgumentParser(description='Parse files from the command line.')
    PARSER.add_argument("filename", help="absolute or relative path to the argument file")
    PARSER.add_argument("convert", metavar="convert-type", help="filetype to convert into (list, dictionary, json or csv)")
    PARSER.add_argument("-v", "--verbose", help="enable verbose", action="store_true")
    ARGV = PARSER.parse_args()
    if not os.path.isabs(ARGV.filename):
        root_path = os.getcwd()
        ARGV.filename = root_path + "/" + ARGV.filename
    return ARGV.filename, ARGV.verbose, ARGV.convert

if __name__ == '__main__' :
    main()