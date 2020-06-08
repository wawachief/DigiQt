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

with open(sys.argv[1], "r") as f:
    text = ""
    for l in f.readlines():
        text += l
    asm = Assemble(text,inst_dic)
    res = asm.parse()

if res[0]:
    dr_cpu = Cpu(dr_model = "2U")
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
