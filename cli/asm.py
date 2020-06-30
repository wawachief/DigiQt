#!/usr/bin/python3

# Olivier Lecluse
# Command line assembler
# Usage : asm.py file_to_assemble.asm
# Returns a list of bytes

import sys
sys.path.append("..") 
from src.model.assemble import Assemble
from src.digirules.instructionset_2U import inst_dic

def ram2hex(ram):
    """converts the content of the ram into hex format"""
    def tohex(i):
        """converts an integer into hexadecimal on 2 caracters
        ex : tohex(8) -> '08' ; tohex(12) -> '0C'
        """
        return hex(i)[2:].rjust(2,'0').upper()

    hexdump = ""
    for line in range(16):
        nbcol = 12 if line == 15 else 16
        # Line header : nbcol (2 bytes) + address (2 bytes)
        newline = ':' + tohex(nbcol) + '00' + tohex(line * 16) + '00'
        control = nbcol + line * 16
        for col in range(nbcol):
            r = ram[line*16+col]
            control += r
            newline += tohex(r)
        newline += tohex((256-control)%256)
        hexdump += newline + '\n'
    hexdump += ":00000001FF"
    return hexdump


with open(sys.argv[1], "r") as f:
    text = ""
    for l in f.readlines():
        text += l
    asm = Assemble(text, inst_dic)
    res = asm.parse()
    ram = [0] * 256
    for i, r in enumerate(res[1]):
        ram[i]=r
    print(res[1])
    print("HEX DUMP")
    print(ram2hex(ram))
