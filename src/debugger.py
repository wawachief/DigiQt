from PySide2.QtCore import QObject, Signal, Slot

class Debug(QObject): 
    sig_hexa_mode = Signal(bool)
    def __init__(self, cpu, ram_frame):
        QObject.__init__(self)

        self.cpu = cpu
        self.ram_frame = ram_frame
        self.text_ram = ""
        self.hexmode = False

        # Checkbox Signal
        self.sig_hexa_mode.connect(self.on_hexa_change)
        self.ram_frame.sig_hexa_mode = self.sig_hexa_mode
    
    #
    # Signal
    #
    
    @Slot(bool)
    def on_hexa_change(self, mode):
        self.hexmode = mode
        self.view_ram()

    #
    # Debugger
    #

    def view_ram(self):
        """Displays RAM dump into ram_frade edit field
        and register values into label fields"""
        self.text_ram = ""
        
        for l in range(32):
            line = self.d2h(l*8) + ":  "
            for c in range(8):
                line += self.d2h(self.cpu.ram[l*8+c]) + " "
            if l < 31:
                line += "\n"
            self.text_ram += line

        # Displays the registers values
        hexmode_str = "hex" if self.hexmode else "dec"

        # Update the RAM text field
        self.ram_frame.set_ram_content(self.text_ram)
        self.ram_frame.set_pc(f"{self.d2b(self.cpu.pc)} ({hexmode_str} : {self.d2h(self.cpu.pc)})")
        self.ram_frame.set_ac(f"{self.d2b(self.cpu.accu)} (dec : {str(self.cpu.accu)})")
        stack_str = ""
        for i in range(self.cpu.sp):
            stack_str += self.d2h(self.cpu.stack[i]) + " "
        self.ram_frame.set_stack(stack_str)
        self.ram_frame.set_st(f"{self.d2b(self.cpu.ram[self.cpu.REG_STATUS])}")

        # Highlight PC position

        # computes the current PC position
        lpc = self.cpu.pc // 8
        cpc = self.cpu.pc % 8
        self.ram_frame.ram_content.select(lpc, cpc, "ram_pc")

    #
    # Conversion methods
    #

    def b2d(self, b):
        """ convertit une chaine de 8 bits en nb décimal 
        entrée : b = chaine de 8 caractères ('0' ou '1') 
        sortie : d = nb entier (base décimale) """
        d = 0
        for i,n in enumerate(b):
            d += 2**(7-i) * int(n)
        return d
        
    def d2b(self, d):
        """ convertit un entier en une chaine de 8 bits 
        entrée : d = nb entier (base décimale)
        sortie : chaine de 8 caractères ('0' ou '1')  """
        return bin(d)[2:].rjust(8, '0')


    def d2h(self, d):
        """ convertit un entier en une chaine de 2 caractères hexadécimaux 
        entrée : d = nb entier (base décimale), hexmode = True pour hexa
        sortie : chaine de 2 caractères ('0' à 'F')  """
        if self.hexmode:
            return hex(d)[2:].rjust(2, '0').upper()
        else:
            return str(d).rjust(3, '0')
