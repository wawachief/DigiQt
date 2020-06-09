#!/usr/bin/python3

# Olivier Lecluse
# Command line execution
# Usage : exec.py file_to_assemble.asm
# Returns the RAM after execution and number of steps

import sys
sys.path.append("..") 
from src.model.assemble import Assemble
from src.model.cpu import Cpu
from src.digirules.instructionset_2U import inst_dic
from configparser import ConfigParser

CONFIG_FILE_PATH = '../src/config.ini'

with open(sys.argv[1], "r") as f:
    text = ""
    for l in f.readlines():
        text += l
    asm = Assemble(text,inst_dic)
    res = asm.parse()

if res[0]:
    config = ConfigParser()
    config.read(CONFIG_FILE_PATH)
    print (config.get('digirule', 'DR_MODEL'))
    dr_cpu = Cpu(config)
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
