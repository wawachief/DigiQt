# Author: Olivier Lécluse
# Licence GPL-3

#
# Digirule CPU Core
#

#
# todo add symbol table attribute to better decode instructions
#

from importlib import import_module
from random import randint

class Cpu:
    def __init__(self, stack_size=16, sstack_size=64, dr_model="2U"):
        self.ram = [0] * 256
        self.accu = 0          # Accumulator
        self.pc   = 0          # Program Counter
        self.sp   = 0          # Stack Pointer
        self.ssp  = 0          # Software Pointer
        self.rx   = None       # Byte received or None
        self.tx   = None       # Byte to send of None
        self.stack  = [0] * stack_size    # CPU Stack
        self.sstack = [0] * sstack_size   # Software stack
        self.run    = False
        self.speed  = 0        # speed attribute changed by the speed instruction
        self.dr_model     = dr_model
        self.stack_size   = stack_size
        self.sstack_size  = sstack_size
        self.decoded_inst = "" 
        self.exception    = ""

        # Special RAM addresses
        self.REG_STATUS  = 252
        self.REG_BUTTON  = 253
        self.REG_ADDRLED = 254
        self.REG_DATALED = 255

        # Loading instruction set
        instruction_set = import_module("src.digirules.instructionset_" + dr_model)
        self.inst_dic = instruction_set.inst_dic

        # Building lookup table to access functions by opcodes
        # format : lookupTable [opcode] --> function
        self.lookup_table = [self.inst_illegal] * 256
        for inst in self.inst_dic :
            opcode  = self.inst_dic[inst]["code"]
            opcount = self.inst_dic[inst]["operandCount"]
            self.lookup_table[opcode] = [eval("self.inst_"+inst), inst, opcount]

    #
    # Execution methods
    #
    def tick(self):
        """Executes one CPU cycle"""
        if self.run:
            # Fetch
            opcode = self.ram[self.pc]
            # Decode
            execute, inst, opcount = self.lookup_table [opcode]
            self.decoded_inst = inst
            for i in range(opcount):
                self.decoded_inst += " " + str(self.ram[self.pc + 1 + i])
            # Execute
            inc_pc = execute()
            # increment Program Counter
            if inc_pc:
                # each instruction returns True if PC is to be incremented, False otherwise
                # jump functions will deal with PC themselves
                self.set_pc(self.pc + 1 + opcount)

    def set_pc(self, new_pc):
        """Changes Program Counter"""
        if 0 <= new_pc <= 255:
            self.pc = new_pc
        else:
            self.do_halt("Illegal PC value")

    def do_halt(self, exception_msg=""):
        """Stops the program and updates exception attribute"""
        self.exception = exception_msg
        self.run = False

    #
    # RAM operations
    #
    def clear_ram(self):
        self.ram = [0] * 256

    def set_ram(self, new_ram):
        self.clear_ram()
        for i, r in enumerate(new_ram):
            self.ram [i] = r
    #
    # Status register methods
    #
    def status_Z(self, n):
        """ toggles the Zero bit (bit 0) on the status register if necessary """
        if n == 0:
            self.ram[self.REG_STATUS] |= 1 # sets Zero bit to 1
            return True
        self.ram[self.REG_STATUS] &= 254   # sets Zero bit to 0
        return False
    
    def status_C(self, n, way_up=True):
        """ toggles the Carry bit (bit 1) on the status register if necessary """
        if (n > 255 and way_up) or (n < 0 and not way_up):
            self.ram[self.REG_STATUS] |= 2 # sets Carry bit to 1
            return True
        self.ram[self.REG_STATUS] &= 253   # sets Carry bit to 0
        return False

    #
    # Stack methods
    #
    def stack_in(self, p):
        """saves the address where to go after the next RETURN or RETLA"""
        if self.sp >= self.stack_size:
        	self.do_halt("Stack Overflow")
        else:
            self.stack[self.sp] = p
            self.sp += 1 
        
    def stack_out(self):
        if self.sp == 0:
            self.do_halt("Stack Underflow")
            return 0
        else:
            self.sp -= 1
            return self.stack[self.sp]

    #
    # Instructions Implementation
    # Arguments are arg_i = self.ram[self.pc + i] i>=1
    # Return True : lets ticks() increment the PC automatically
    # Return False : the method must deal with PC
    #
    def inst_illegal(self):
        self.do_halt("Illegal instruction")
        return False
    def inst_halt(self):
        self.do_halt("Program Halted")
        self.run = False
        return True
    def inst_nop(self):
        return True
    def inst_speed(self):
        self.speed = self.ram[self.pc + 1]
        return True
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
    def inst_copyra(self):
        arg1 = self.ram[self.pc + 1] 
        self.accu = self.ram[arg1]
        self.status_Z(self.accu)
        return True
    def inst_copyrr(self):
        arg1 = self.ram[self.pc + 1] 
        arg2 = self.ram[self.pc + 2] 
        self.ram[arg2] = self.ram[arg1]
        self.status_Z(self.ram[arg1])
        return True
    def inst_addla(self):
        arg1 = self.ram[self.pc + 1]
        if self.status_C(self.accu + arg1):
            self.accu += arg1 - 256
        else:
            self.accu += arg1
        self.status_Z(self.accu)
        return True
    def inst_addra(self):
        arg1 = self.ram[self.pc + 1]
        if self.status_C(self.accu + self.ram[arg1]):
            self.accu += self.ram[arg1] - 256
        else:
            self.accu += self.ram[arg1]
        self.status_Z(self.accu)
        return True
    def inst_subla(self):
        arg1 = self.ram[self.pc + 1]
        if self.status_C(self.accu - arg1, False):
            self.accu += 256 - arg1
        else:
            self.accu -= arg1
        self.status_Z(self.accu)
        return True
    def inst_subra(self):
        arg1 = self.ram[self.pc + 1]
        if self.status_C(self.accu - self.ram[arg1], False):
            self.accu += 256 - self.ram[arg1]
        else:
            self.accu -= self.ram[arg1]
        self.status_Z(self.accu)
        return True
    def inst_andla(self):
        self.accu &= self.ram[self.pc + 1]
        self.status_Z(self.accu)
        return True
    def inst_andra(self):
        self.accu &= self.ram[self.ram[self.pc + 1]]
        self.status_Z(self.accu)
        return True
    def inst_orla(self):
        self.accu |= self.ram[self.pc + 1]
        self.status_Z(self.accu)
        return True
    def inst_orra(self):
        self.accu |= self.ram[self.ram[self.pc + 1]]
        self.status_Z(self.accu)
        return True
    def inst_xorla(self):
        self.accu ^= self.ram[self.pc + 1]
        self.status_Z(self.accu)
        return True
    def inst_xorra(self):
        self.accu ^= self.ram[self.ram[self.pc + 1]]
        self.status_Z(self.accu)
        return True
    def inst_decr(self):
        arg1 = self.ram[self.pc + 1]
        self.ram[arg1]  = (-1 + self.ram[arg1]) % 256
        self.status_Z(self.ram[arg1])
        return True
    def inst_incr(self):
        arg1 = self.ram[self.pc + 1]
        self.ram[arg1]  = (1 + self.ram[arg1]) % 256
        self.status_Z(self.ram[arg1])
        return True
    def inst_decrjz(self):
        arg1 = self.ram[self.pc + 1]
        self.ram[arg1]  = (-1 + self.ram[arg1]) % 256
        if self.status_Z(self.ram[arg1]):
            self.set_pc(self.pc + 4)
        else:
            self.set_pc(self.pc + 2)
        return False
    def inst_incrjz(self):
        arg1 = self.ram[self.pc + 1]
        self.ram[arg1]  = (1 + self.ram[arg1]) % 256
        if self.status_Z(self.ram[arg1]):
            self.set_pc(self.pc + 4)
        else:
            self.set_pc(self.pc + 2)
        return False
    def inst_shiftrl(self):
        arg1 = self.ram[self.pc + 1]
        self.ram[arg1] <<= 1                              # shifts whitout taking care of the previous Carry bit
        carry = 1 if self.ram[self.REG_STATUS] & 2 else 0 # gets the previous Carry bit on the status register
        self.ram[arg1] += carry                           # sets the LSB equals to the previous Carry bit
        if self.status_C(self.ram[arg1]):
            self.ram[arg1] -= 256
        return True
    def inst_shiftrr(self):
        arg1 = self.ram[self.pc + 1]
        carry = 1 if self.ram[self.REG_STATUS] & 2 else 0 # gets the previous Carry bit on the status register
        if self.ram[arg1] % 2 == 1:                       # if odd value => raises a new Carry
            self.status_C(256)                            # sets Carry bit to 1
        else:
            self.status_C(0)                              # sets Carry bit to 0
        self.ram[arg1] >>= 1                              # shifts whitout taking care of the previous Carry bit
        self.ram[arg1] += 128 * carry                     # sets the MSB equals to the previous Carry bit
        return True
    def inst_cbr(self):
        arg1 = self.ram[self.pc + 1]
        arg2 = self.ram[self.pc + 2]
        self.ram[arg2] &= (255-2**arg1)                   # sets the specified bit to 0
        return True
    def inst_sbr(self):
        arg1 = self.ram[self.pc + 1]
        arg2 = self.ram[self.pc + 2]
        self.ram[arg2] |= 2**arg1                         # sets the specified bit to 0
        return True
    def inst_bcrsc(self):                                 # Bit Check Ram Skip if Cleared
        arg1 = self.ram[self.pc + 1]
        arg2 = self.ram[self.pc + 2]
        if (self.ram[arg2] & 2**arg1) == 0:
            self.set_pc(self.pc + 5)
        else:
            self.set_pc(self.pc + 3)
        return False
    def inst_bcrss(self):                                 # Bit Check Ram Skip if Set
        arg1 = self.ram[self.pc + 1]
        arg2 = self.ram[self.pc + 2]
        if (self.ram[arg2] & 2**arg1) != 0:
            self.set_pc(self.pc + 5)
        else:
            self.set_pc(self.pc + 3)
        return False
    def inst_jump(self):
        arg1 = self.ram[self.pc + 1]
        self.set_pc(arg1)
        return False
    def inst_call(self):
        arg1 = self.ram[self.pc + 1]
        self.stack_in(self.pc + 2)
        self.set_pc(arg1)
        return False
    def inst_return(self):
        self.set_pc(self.stack_out())
        return False
    def inst_retla(self):
        arg1 = self.ram[self.pc + 1]
        self.accu = arg1
        self.set_pc(self.stack_out())
        return False
    def inst_addrpc(self):
        arg1 = self.ram[self.pc + 1]
        self.set_pc(self.pc + 2 + self.ram[arg1])
        return False
    def inst_initsp(self):
        self.sp = 0
        self.ssp = 0
        return True
    def inst_randa(self):
        self.accu = randint(0, 255)
        return True
    #
    # 2U instructions
    #
    def inst_swapra(self):
        arg1 = self.ram[self.pc + 1]
        self.accu, self.ram[arg1] = self.ram[arg1], self.accu
        return True
    def inst_swaprr(self):
        arg1 = self.ram[self.pc + 1]
        arg2 = self.ram[self.pc + 2]
        self.ram[arg1], self.ram[arg2] = self.ram[arg2], self.ram[arg1]
        return True
    def inst_mul(self):                  # on entry arg1 = @multiplicand and arg2 = m@ultiplier; 
        arg1 = self.ram[self.pc + 1]     # on exit arg1 = @product
        arg2 = self.ram[self.pc + 2]
        self.ram[arg1] = self.ram[arg1] * self.ram[arg2]
        return True
    def inst_div(self):                  # on entry arg1 = @dividend and arg2 = @divisor; 
        arg1 = self.ram[self.pc + 1]     # on exit arg1 = @quotient and accumulator = remainder
        arg2 = self.ram[self.pc + 2]
        dividend, divisor = self.ram[arg1], self.ram[arg2]
        if divisor == 0:
            self.do_halt("division by 0")
        else:
            self.ram[arg1] = dividend // divisor
            self.accu = dividend % divisor
        return True
    #
    # USB instructions
    #
    def inst_comout(self):
        self.tx = self.accu
        return True
    def inst_comin(self):
        return self.rx is not None
    def inst_comrdy(self):
        if self.rx is None:              
            self.status_Z(0)             # if no character awaits, sets the zeroflag
        else:
            self.status_Z(1)             # if a character is available, clears the zeroflag
        return True
    #
    # 2B experimental instructions
    #
    def inst_copyli(self):
        arg1 = self.ram[self.pc + 1] 
        arg2 = self.ram[self.pc + 2] 
        self.ram[self.ram[arg2]] = arg1
        return True
    def inst_copyai(self):
        arg1 = self.ram[self.pc + 1] 
        self.ram[self.ram[arg1]] = self.accu
        return True
    def inst_copyia(self):
        arg1 = self.ram[self.pc + 1] 
        self.accu = self.ram[self.ram[arg1]]
        self.status_Z(self.accu)
        return True
    def inst_copyri(self):
        arg1 = self.ram[self.pc + 1] 
        arg2 = self.ram[self.pc + 2] 
        self.ram[self.ram[arg2]] = self.ram[arg1]
        self.status_Z(self.ram[arg1])
        return True
    def inst_copyir(self):
        arg1 = self.ram[self.pc + 1] 
        arg2 = self.ram[self.pc + 2] 
        self.ram[arg2] = self.ram[self.ram[arg1]]
        self.status_Z(self.ram[arg2])
        return True
    def inst_copyii(self):
        arg1 = self.ram[self.pc + 1] 
        arg2 = self.ram[self.pc + 2] 
        self.ram[self.ram[arg2]] = self.ram[self.ram[arg1]]
        self.status_Z(self.ram[self.ram[arg2]])
        return True
    def inst_shiftar(self):
        carry = 1 if self.ram[self.REG_STATUS] & 2 else 0 # gets the previous Carry bit on the status register
        if self.accu % 2 == 1:                            # if odd value => raises a new Carry
            self.status_C(256)                            # sets Carry bit to 1
        else:
            self.status_C(0)                              # sets Carry bit to 0
        self.accu >>= 1                                   # shifts whitout taking care of the previous Carry bit
        self.accu += 128 * carry                          # sets the MSB equals to the previous Carry bit
        return True
    def inst_shiftal(self):
        self.accu <<= 1                                   # shifts whitout taking care of the previous Carry bit
        carry = 1 if self.ram[self.REG_STATUS] & 2 else 0 # gets the previous Carry bit on the status register
        self.accu += carry                           # sets the LSB equals to the previous Carry bit
        if self.status_C(self.accu):
            self.accu -= 256
        return True
    def inst_jumpi(self):
        arg1 = self.ram[self.pc + 1]
        self.set_pc(self.ram[arg1])
        return False
    def inst_calli(self):
        arg1 = self.ram[self.pc + 1]
        self.stack_in(self.pc + 2)
        self.set_pc(self.ram[arg1])
        return False
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
