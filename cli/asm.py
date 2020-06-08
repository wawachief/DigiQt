#!/usr/bin/python3

# Olivier Lecluse
# Command line assembler
# Usage : asm.py file_to_assemble.asm
# Returns a list of bytes

import sys
sys.path.append("..") 
from src.model.assemble import Assemble
from src.digirules.instructionset_2U import inst_dic
with open(sys.argv[1], "r") as f:
    text = ""
    for l in f.readlines():
        text += l
    asm = Assemble(text, inst_dic)
    res = asm.parse()
    print(res[1:])