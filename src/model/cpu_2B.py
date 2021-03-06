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
        self.dr_model     = "2B"
        self.stack_size   = 64
        self.sstack_size  = 256
        # attributes initialization
        self.stack  = [0] * self.stack_size    # CPU Stack
        self.sstack = [0] * self.sstack_size   # Software stack
        
        self.make_lookup_table()

    def inst_shiftal(self):
        self.accu <<= 1                                   # shifts whitout taking care of the previous Carry bit
        carry = (self.ram[self.REG_STATUS] & 2) // 2      # 0 or 2 # gets the previous Carry bit on the status register
        self.accu += carry                                # sets the LSB equals to the previous Carry bit
        self.accu = self.status_C(self.accu)
        return True
    def inst_shiftar(self):
        carry = (self.ram[self.REG_STATUS] & 2) // 2      # gets the previous Carry bit on the status register
        if self.accu % 2 == 1:                            # if odd value => raises a new Carry
            self.status_C(256)                            # sets Carry bit to 1
        else:
            self.status_C(0)                              # sets Carry bit to 0
        self.accu >>= 1                                   # shifts whitout taking care of the previous Carry bit
        self.accu += 128 * carry                          # sets the MSB equals to the previous Carry bit
        return True

    def inst_initsp(self):
        self.sp = 0
        self.ssp = 0 # Reinitialize software stack pointer
        return True

    # Logical operations with RAM
    def inst_andlr(self):
        arg1 = self.ram[self.pc + 1]
        arg2 = self.ram[self.pc + 2]
        self.ram[arg2] &= arg1
        self.status_Z(self.ram[arg2])
        return True
    def inst_andrr(self):
        arg1 = self.ram[self.pc + 1]
        arg2 = self.ram[self.pc + 2]
        self.ram[arg2] &= self.ram[arg1]
        self.status_Z(self.ram[arg2])
        return True
    def inst_orlr(self):
        arg1 = self.ram[self.pc + 1]
        arg2 = self.ram[self.pc + 2]
        self.ram[arg2] |= arg1
        self.status_Z(self.ram[arg2])
        return True
    def inst_orrr(self):
        arg1 = self.ram[self.pc + 1]
        arg2 = self.ram[self.pc + 2]
        self.ram[arg2] |= self.ram[arg1]
        self.status_Z(self.ram[arg2])
        return True
    def inst_xorlr(self):
        arg1 = self.ram[self.pc + 1]
        arg2 = self.ram[self.pc + 2]
        self.ram[arg2] ^= arg1
        self.status_Z(self.ram[arg2])
        return True
    def inst_xorrr(self):
        arg1 = self.ram[self.pc + 1]
        arg2 = self.ram[self.pc + 2]
        self.ram[arg2] ^= self.ram[arg1]
        self.status_Z(self.ram[arg2])
        return True
    
    # Jump and test 0 instructions
    def inst_jumpznz(self, z):
        if self.ram[self.REG_STATUS] & 1 == z:
            arg1 = self.ram[self.pc + 1]
            self.set_pc(arg1)
            return False
        return True
    def inst_jumpnz(self):
        return self.inst_jumpznz(0)
    def inst_jumpz(self):
        return self.inst_jumpznz(1)

    # Software stack
    def inst_sspush(self):
        if self.ssp >= self.sstack_size:
        	self.do_halt("Software Stack Overflow")
        else: 
            self.sstack[self.ssp] = self.accu
            self.ssp += 1 
        return True
    def inst_sspop(self):
        if self.ssp == 0:
            self.do_halt("Software Stack Underflow")
        else:
            self.ssp -= 1
            self.accu = self.sstack[self.ssp]
            self.status_Z(self.accu)
        return True
    def inst_sspushr(self):
        arg1 = self.ram[self.pc + 1]
        if self.ssp >= self.sstack_size:
        	self.do_halt("Software Stack Overflow")
        else: 
            self.sstack[self.ssp] = self.ram[arg1]
            self.ssp += 1 
        return True
    def inst_sspopr(self):
        arg1 = self.ram[self.pc + 1]
        if self.ssp == 0:
            self.do_halt("Software Stack Underflow")
        else:
            self.ssp -= 1
            self.ram[arg1] = self.sstack[self.ssp]
            self.status_Z(self.ram[arg1])
        return True
    def inst_sspushi(self):
        arg1 = self.ram[self.pc + 1]
        if self.ssp >= self.sstack_size:
        	self.do_halt("Software Stack Overflow")
        else: 
            self.sstack[self.ssp] = self.ram[self.ram[arg1]]
            self.ssp += 1 
        return True
    def inst_sspopi(self):
        arg1 = self.ram[self.pc + 1]
        if self.ssp == 0:
            self.do_halt("Software Stack Underflow")
        else:
            self.ssp -= 1
            self.ram[self.ram[arg1]] = self.sstack[self.ssp]
            self.status_Z(self.ram[self.ram[arg1]])
        return True
    def inst_sshead(self):
        if self.ssp == 0:
            self.do_halt("Software Stack Underflow")
        else:
            self.accu = self.sstack[self.ssp - 1]
            self.statu_Z(self.accu)
        return True
    def inst_ssdepth(self):
        self.accu = self.ssp
        self.status_Z(self.accu)
        return True

    #
    # deactivating 2U instructions
    # not strictly necessary...
    #

    inst_comin  = Core.inst_illegal
    inst_comout = Core.inst_illegal
    inst_comrdy = Core.inst_illegal
    
    inst_pinin = Core.inst_illegal
    inst_pinout = Core.inst_illegal
    inst_pindir = Core.inst_illegal