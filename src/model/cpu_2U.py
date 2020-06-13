# Author: Olivier Lécluse
# Licence GPL-3

#
# Digirule CPU Core
#

#
# todo add symbol table attribute to better decode instructions
#

from PySide2.QtCore import Signal, Slot, QObject
from importlib import import_module
from random import randint

class Cpu(QObject):
    def __init__(self, sig_cpu_stopped = None, sig_cpu_speed = None):
        QObject.__init__(self)
        self.sig_cpu_stopped = sig_cpu_stopped
        self.sig_cpu_speed = sig_cpu_speed
        self.sig_CPU_comout = None # These signals are pushed 
        self.sig_CPU_comin  = None # by the serial controler

        # CPU configuration
        self.dr_model     = "2U"
        self.stack_size   = 16
        # attributes initialization
        self.ram = [0] * 256
        self.stack  = [0] * self.stack_size    # CPU Stack
        self.accu = 0          # Accumulator
        self.pc   = 0          # Program Counter
        self.sp   = 0          # Stack Pointer
        self.rx   = None       # Byte received or None
        self.tx   = None       # Byte to send of None
        self.run    = False    # Run mode flag
        self.speed  = 0        # speed attribute changed by the speed instruction
        # self.decoded_inst = "" 
        self.exception    = ""

        # Special RAM addresses
        self.REG_STATUS  = 252
        self.REG_BUTTON  = 253
        self.REG_ADDRLED = 254
        self.REG_DATALED = 255

        # Loading instruction set
        instruction_set = import_module("src.digirules.instructionset_" + self.dr_model)
        self.inst_dic = instruction_set.inst_dic

        # Building lookup table to access functions by opcodes
        # format : lookupTable [opcode] --> function
        self.lookup_table = [[self.inst_illegal, "illegal", 0] for _ in range(256)]
        for inst in self.inst_dic :
            opcode  = self.inst_dic[inst]["code"]
            opcount = self.inst_dic[inst]["operandCount"]
            self.lookup_table[opcode] = [eval("self.inst_"+inst), inst, opcount]

    #
    # Execution methods
    #
    def tick(self):
        """Executes one CPU cycle"""
        # Fetch
        opcode = self.ram[self.pc]
        # Decode
        execute, _, opcount = self.lookup_table [opcode]
        # self.decoded_inst = inst
        if self.pc + opcount > 255:
            self.do_halt("Illegal RAM access")
        else:
            # for i in range(opcount):
            #     self.decoded_inst += " " + str(self.ram[self.pc + 1 + i])
            # Execute
            inc_pc = execute()
            # increment Program Counter
            if inc_pc:
                # each instruction returns True if PC is to be incremented, False otherwise
                # jump functions will deal with PC themselves
                self.set_pc(self.pc + 1 + opcount)
    
    def decode(self, addr, symbols = None):
        """desassemble instruction at address addr
        try to resolve parameters usin assembler symbol table"""
        _, inst, opcount = self.lookup_table [self.ram[addr]]
        for i in range(opcount):
            # try to resolve the parameter in the symbol table
            param = self.ram[addr + 1 + i]
            if not ((i == 0 and inst[-2] == 'l' and inst != "call") or inst == "speed"):
                # dont resolve litteral parameters
                if symbols:
                    for key in symbols:
                        if symbols[key] == param:
                            param = key
                            break
            inst += " " + str(param)
        return inst

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
        # Emits stop signal
        if self.sig_cpu_stopped is not None:
            self.sig_cpu_stopped.emit(self.exception)

    #
    # RAM operations
    #
    def clear_ram(self):
        if self.run:
            self.do_halt("Clear RAM while running")
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
        # send signal to the controler
        self.sig_cpu_speed.emit(str(self.speed))
        return True
    def inst_copylr(self):
        arg1 = self.ram[self.pc + 1] 
        arg2 = self.ram[self.pc + 2] 
        self.ram[arg2] = arg1
        self.status_Z(arg1)
        return True
    def inst_copyla(self):
        self.accu = self.ram[self.pc + 1]
        self.status_Z(self.accu)
        return True
    def inst_copyar(self):
        arg1 = self.ram[self.pc + 1] 
        self.ram[arg1] = self.accu
        self.status_Z(self.accu)
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
    # indirect copy
    def inst_copyli(self):
        arg1 = self.ram[self.pc + 1] 
        arg2 = self.ram[self.pc + 2] 
        self.ram[self.ram[arg2]] = arg1
        self.status_Z(arg1)
        return True
    def inst_copyai(self):
        arg1 = self.ram[self.pc + 1] 
        self.ram[self.ram[arg1]] = self.accu
        self.status_Z(self.accu)
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
        return True
    def inst_randa(self):
        self.accu = randint(0, 255)
        return True
    #
    # 2U instructions
    #

    # Indirect jumps
    def inst_jumpi(self):
        arg1 = self.ram[self.pc + 1]
        self.set_pc(self.ram[arg1])
        return False
    def inst_calli(self):
        arg1 = self.ram[self.pc + 1]
        self.stack_in(self.pc + 2)
        self.set_pc(self.ram[arg1])
        return False
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
        mul = self.ram[arg1] * self.ram[arg2]
        self.ram[arg1] = mul % 256
        self.status_Z(self.ram[arg1])
        self.status_C(mul)
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
            self.status_Z(self.ram[arg1])
            if self.accu == 0:
                # Remainder is 0, we activate the Carry flag
                self.status_C(256)
            else:
                self.status_C(0)
        return True
    #
    # USB instructions
    #
    def inst_comout(self):
        self.tx = self.accu
        self.sig_CPU_comout.emit(self.accu)
        return True
    def inst_comin(self):
        if self.rx is None:
            # Waits for a character to come in
            return False
        self.accu = ord(self.rx)
        self.rx = None
        self.sig_CPU_comin.emit("Done")
        # Char is handled, we move on !
        return True
    def inst_comrdy(self):
        if self.rx is None:              
            self.status_Z(0)             # if no character awaits, sets the zeroflag
        else:
            self.status_Z(1)             # if a character is available, clears the zeroflag
        return True