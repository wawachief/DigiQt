#!/usr/bin/python3

# Olivier Lecluse
# Command line assembler
# Usage : asm.py file_to_assemble.asm
# Returns a list of bytes

import sys
sys.path.append("..") 
from src.model.assemble import Assemble
from src.digirules.instructionset_2U import inst_dic
from src.hex_utils import ram2hex
from configparser import ConfigParser
from importlib import import_module
from os import path
import shutil

CONFIG_FILE_PATH = '../src/config.ini'

# Read configuration
# Copy config file into home directory
config_path = path.expanduser("~/.DigiQtrc")
if not path.exists(config_path):
    shutil.copyfile(CONFIG_FILE_PATH, config_path)
# Compare local version with app version
config_ori = ConfigParser()
config_ori.read(CONFIG_FILE_PATH)
config = ConfigParser()
config.read(config_path)
if config_ori.get('main', 'app_version') != config.get('main', 'app_version'):
    # .DigiQtrc is obsolete, We overwrite the config file
    shutil.copyfile(CONFIG_FILE_PATH, config_path)
    config.read(config_path)

dr_model = config.get('digirule', 'dr_model')
inst_dic = import_module("src.digirules.instructionset_" + dr_model)
print (f"Assemble for model {dr_model}")
with open(sys.argv[1], "r") as f:
    text = ""
    for l in f.readlines():
        text += l
    asm = Assemble(text, inst_dic.inst_dic)
    res = asm.parse()
    ram = [0] * 256
    for i, r in enumerate(res[1]):
        ram[i]=r
    print(res[1])
    print("HEX DUMP")
    print(ram2hex(ram))
