#!/usr/bin/python3

# Olivier Lecluse
# Command line execution
# Usage : exec.py file_to_assemble.asm
# Returns the RAM after execution and number of steps

import sys
sys.path.append("..") 
from src.model.assemble import Assemble
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

## TODO

with open(sys.argv[1], "r") as f:
    text = ""
    for l in f.readlines():
        text += l
    asm = Assemble(text,inst_dic.inst_dic)
    res = asm.parse()

    CpuModule = import_module("src.model.cpu_" + dr_model)
    dr_cpu = CpuModule.Cpu()
    dr_cpu.set_ram(res[1])
    dr_cpu.run = True
    n = 0
    while dr_cpu.run:
        dr_cpu.tick()
        # print(dr_cpu.decoded_inst)
        n += 1
    print("RAM: ", dr_cpu.ram)
    print("ACC: ", dr_cpu.accu)
    print("Nb cycles : ", n)
