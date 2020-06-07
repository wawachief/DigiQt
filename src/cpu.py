from importlib import import_module

class Cpu:
    def __init__(self, stack_size=16, sstack_size=64, dr_model="2U"):
        self.ram = [0] * 256
        self.accu = 0          # Accumulator
        self.pc   = 0          # Program Counter
        self.sp   = 0          # Stack Pointer
        self.ssp  = 0          # Software Pointer
        self.stack  = [0] * stack_size    # CPU Stack
        self.sstack = [0] * sstack_size   # Software stack
        self.run    = False
        self.dr_model    = dr_model
        self.stack_size  = stack_size
        self.sstack_size = sstack_size

        # Loading instruction set
        instruction_set = import_module("src.digirules.instructionset_" + dr_model)
        self.inst_dic = instruction_set.inst_dic

        # Building lookup table to access functions by opcodes
        # format : lookupTable [opcode] --> function
        self.lookup_table = [self.inst_illegal] * 256
        for inst in self.inst_dic:
            opcode = self.inst_dic[inst]["code"]
            self.lookup_table[opcode] = eval("self.inst_" + inst)


    def tick(self):
        """Executes one CPU cycle"""
        self.lookup_table[0]()

    def inst_illegal(self):
        self.inst_halt()
    def inst_halt(self):
        print("Halt")
    def inst_nop(self):
        pass
    def inst_speed(self):
        pass
    def inst_copylr(self):
        pass
    def inst_copyla(self):
        pass
    def inst_copyar(self):
        pass
    def inst_copyra(self):
        pass
    def inst_copyrr(self):
        pass
    def inst_addla(self):
        pass
    def inst_addra(self):
        pass
    def inst_subla(self):
        pass
    def inst_subra(self):
        pass
    def inst_andla(self):
        pass
    def inst_andra(self):
        pass
    def inst_orla(self):
        pass
    def inst_orra(self):
        pass
    def inst_xorla(self):
        pass
    def inst_xorra(self):
        pass
    def inst_decr(self):
        pass
    def inst_incr(self):
        pass
    def inst_decrjz(self):
        pass
    def inst_incrjz(self):
        pass
    def inst_shiftrl(self):
        pass
    def inst_shiftrr(self):
        pass
    def inst_cbr(self):
        pass
    def inst_sbr(self):
        pass
    def inst_bcrsc(self):
        pass
    def inst_bcrss(self):
        pass
    def inst_jump(self):
        pass
    def inst_call(self):
        pass
    def inst_return(self):
        pass
    def inst_retla(self):
        pass
    def inst_addrpc(self):
        pass
    def inst_initsp(self):
        pass
    def inst_randa(self):
        pass
    #
    # 2U instructions
    #
    def inst_swapra(self):
        pass
    def inst_swaprr(self):
        pass
    def inst_mul(self):
        pass
    def inst_div(self):
        pass
    #
    # USB instructions
    #
    def inst_comout(self):
        pass
    def inst_comin(self):
        pass
    def inst_comrdy(self):
        pass
    #
    # 2B experimental instructions
    #
    def inst_copyli(self):
        pass
    def inst_copyai(self):
        pass
    def inst_copyia(self):
        pass
    def inst_copyri(self):
        pass
    def inst_copyir(self):
        pass
    def inst_copyii(self):
        pass
    def inst_shiftar(self):
        pass
    def inst_shiftal(self):
        pass
    def inst_jumpi(self):
        pass
    def inst_calli(self):
        pass
    def inst_sspush(self):
        pass
    def inst_sspop(self):
        pass
    def inst_sspushr(self):
        pass
    def inst_sspopr(self):
        pass
    def inst_sspushi(self):
        pass
    def inst_sspopi(self):
        pass
    def inst_sshead(self):
        pass
    def inst_ssdepth(self):
        pass
