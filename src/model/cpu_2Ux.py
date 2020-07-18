# Author: Olivier Lécluse
# License GPL-3

#
# Digirule CPU Core
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
        self.dr_model     = "2Ux"
        self.stack_size   = 64
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
        self.exception    = ""
        self.serial_enable = True # enable Serial capability
        self.brk_PC = []       # Breakpoints
        self.pin = [[0,0], [0,0]] # [PIN0, PIN1] Pin=(dir, value)

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
            if "alias" not in self.inst_dic[inst].keys():
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
            if self.run and self.pc in self.brk_PC :
                self.do_halt("Hit Breakpoint !")
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
        self.brk_PC = []

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
    
    def status_C(self, n):
        """ toggles the Carry bit (bit 1) on the status register if necessary """
        if (0 <= n <= 255):
            self.ram[self.REG_STATUS] &= 253 # sets Carry bit to 0
            return n
        else:
            self.ram[self.REG_STATUS] |= 2   # sets Carry bit to 1
            return n%256

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
        carry = (self.ram[self.REG_STATUS] & 2) // 2 # 0 or 1
        self.accu = self.status_C(self.accu + arg1 + carry)
        self.status_Z(self.accu)
        return True
    def inst_addra(self):
        arg1 = self.ram[self.pc + 1]
        carry = (self.ram[self.REG_STATUS] & 2) // 2 # 0 or 1
        self.accu = self.status_C(self.accu + self.ram[arg1] + carry)
        self.status_Z(self.accu)
        return True
    def inst_subla(self):
        # Carry = borrow
        arg1 = self.ram[self.pc + 1]
        borrow = (self.ram[self.REG_STATUS] & 2) // 2
        self.accu = self.status_C(self.accu - arg1 - borrow)
        self.status_Z(self.accu)
        return True
    def inst_subra(self):
        # Carry = borrow
        arg1 = self.ram[self.pc + 1]
        borrow = (self.ram[self.REG_STATUS] & 2) // 2
        self.accu = self.status_C(self.accu - self.ram[arg1] - borrow)
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
        carry = (self.ram[self.REG_STATUS] & 2) // 2      # 0 or 2 # gets the previous Carry bit on the status register
        self.ram[arg1] += carry                           # sets the LSB equals to the previous Carry bit
        self.ram[arg1] = self.status_C(self.ram[arg1])
        return True
    def inst_shiftrr(self):
        arg1 = self.ram[self.pc + 1]
        carry = (self.ram[self.REG_STATUS] & 2) // 2      # gets the previous Carry bit on the status register
        if self.ram[arg1] % 2 == 1:                       # if odd value => raises a new Carry
            self.status_C(256)                            # sets Carry bit to 1
        else:
            self.status_C(0)                              # sets Carry bit to 0
        self.ram[arg1] >>= 1                              # shifts whitout taking care of the previous Carry bit
        self.ram[arg1] += 128 * carry                     # sets the MSB equals to the previous Carry bit
        return True
    def inst_bclr(self):
        arg1 = self.ram[self.pc + 1]
        arg2 = self.ram[self.pc + 2]
        self.ram[arg2] &= (255-2**(arg1&7))               # sets the specified bit to 0
        return True
    def inst_bset(self):
        arg1 = self.ram[self.pc + 1]
        arg2 = self.ram[self.pc + 2]
        self.ram[arg2] |= 2**(arg1&7)                     # sets the specified bit to 0
        return True
    def inst_bchg(self):                                  # toggle bit in ram
        arg1 = self.ram[self.pc + 1]
        arg2 = self.ram[self.pc + 2]
        self.ram[arg2] ^= 2**(arg1&7)         
        return True
    def inst_btstsc(self):                                 # Bit Check Ram Skip if Cleared
        arg1 = self.ram[self.pc + 1]
        arg2 = self.ram[self.pc + 2]
        if (self.ram[arg2] & 2**(arg1&7)) == 0:
            self.set_pc(self.pc + 5)
        else:
            self.set_pc(self.pc + 3)
        return False
    def inst_btstss(self):                                 # Bit Check Ram Skip if Set
        arg1 = self.ram[self.pc + 1]
        arg2 = self.ram[self.pc + 2]
        if (self.ram[arg2] & 2**(arg1&7)) != 0:
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
        self.ram[arg1] = self.status_C(self.ram[arg1] * self.ram[arg2])
        self.status_Z(self.ram[arg1])
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
        self.sig_CPU_comout.emit(chr(self.accu))
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

    #
    # Ux instructions
    #

    # Pin instructions
    def inst_pinin(self):                      # PININ no_pin ==> result 0 or 1 in ACCUM
        def p_i(pin):
            if self.pin[0] == 1:
                self.accu = pin[1]
        arg1 = self.ram[self.pc + 1]
        p_i(self.pin[arg1&1])
        return True
    def inst_pinout(self):                     # PINOUT no_pin 0/1
        def p_o(pin, val):
            if self.pin[0] == 0:
                pin[1] = val&1
        arg1 = self.ram[self.pc + 1]
        arg2 = self.ram[self.pc + 2]
        p_o(self.pin[arg1&1], arg2)
        return True
    def inst_pindir(self):                     # PINDIR no_pin 0/1 ==> 0 = OUTPUT, 1 = INPUT
        def p_d(pin, val):
            val &= 1
            pin[0] = val
        arg1 = self.ram[self.pc + 1]
        arg2 = self.ram[self.pc + 2]
        p_d(self.pin[arg1&1], arg2)
        return True

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