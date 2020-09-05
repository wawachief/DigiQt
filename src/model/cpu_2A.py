# Author: Olivier Lécluse
# License GPL-3

#
# Digirule CPU Core
#

from PySide2.QtCore import Signal, Slot, QObject
from src.model.cpu import Core


class Cpu(Core):
    def __init__(self, sig_cpu_stopped = None, sig_cpu_speed = None):
        super().__init__()
        self.sig_cpu_stopped = sig_cpu_stopped
        self.sig_cpu_speed = sig_cpu_speed

        # CPU configuration
        self.dr_model     = "2A"
        self.stack_size   = 4
        # attributes initialization
        self.stack  = [0] * self.stack_size    # CPU Stack

        self.make_lookup_table()


    #
    # Instructions Implementation
    # Arguments are arg_i = self.ram[self.pc + i] i>=1
    # Return True : lets ticks() increment the PC automatically
    # Return False : the method must deal with PC
    #

    # Some copy instruction don't affect Zero flag
    def inst_copylr(self):
        arg1 = self.ram[self.pc + 1] 
        arg2 = self.ram[self.pc + 2] 
        self.ram[arg2] = arg1
        return True
    def inst_copyla(self):
        self.accu = self.ram[self.pc + 1]
        return True
    def inst_copyar(self):
        arg1 = self.ram[self.pc + 1] 
        self.ram[arg1] = self.accu
        return True
    
    # ADD and SUB instructions are without carry
    def inst_addla(self):
        arg1 = self.ram[self.pc + 1]
        self.accu = self.status_C(self.accu + arg1)
        self.status_Z(self.accu)
        return True
    def inst_addra(self):
        arg1 = self.ram[self.pc + 1]
        self.accu = self.status_C(self.accu + self.ram[arg1])
        self.status_Z(self.accu)
        return True
    def inst_subla(self):
        arg1 = self.ram[self.pc + 1]
        self.accu = self.status_C(self.accu - arg1)
        self.status_Z(self.accu)
        return True
    def inst_subra(self):
        arg1 = self.ram[self.pc + 1]
        self.accu = self.status_C(self.accu - self.ram[arg1])
        self.status_Z(self.accu)
        return True

    # restore old bit instruction names
    inst_cbr = Core.inst_bclr
    inst_sbr = Core.inst_bset
    inst_bcrsc = Core.inst_btstsc
    inst_bcrss = Core.inst_btstss

    #
    # deactivating 2U instructions
    # not strictly necessary...
    #

    inst_mul  = Core.inst_illegal
    inst_div  = Core.inst_illegal
    inst_bchg  = Core.inst_illegal

    inst_copyli  = Core.inst_illegal
    inst_copyri  = Core.inst_illegal
    inst_copyir  = Core.inst_illegal
    inst_copyii  = Core.inst_illegal
    inst_copyai  = Core.inst_illegal
    inst_copyia  = Core.inst_illegal

    inst_jumpi  = Core.inst_illegal
    inst_calli  = Core.inst_illegal

    inst_swapra  = Core.inst_illegal
    inst_swaprr  = Core.inst_illegal

    inst_comin  = Core.inst_illegal
    inst_comout = Core.inst_illegal
    inst_comrdy = Core.inst_illegal
    
    inst_pinin = Core.inst_illegal
    inst_pinout = Core.inst_illegal
    inst_pindir = Core.inst_illegal