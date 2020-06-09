from src.model.cpu import Cpu
from src.model.assemble import Assemble
from configparser import ConfigParser
from src.view.MainApp import ExecutionFrame

from PySide2.QtCore import Signal, Slot, QObject

CONFIG_FILE_PATH = 'src/config.ini'

class Controller(QObject):
    # Signals declarations
    sig_config_changed = Signal(str)
    sig_cpu_stopped = Signal(str)

    def __init__(self):
        QObject.__init__(self)

        # signals configuration
        self.sig_config_changed.connect(self.on_config_changed)
        self.sig_cpu_stopped.connect(self.on_cpu_stopped)

        # Read configuration
        self.config = ConfigParser()
        self.config.read(CONFIG_FILE_PATH)
        dr_model = self.config.get('digirule', 'DR_MODEL')
        
        # Controller attributes
        self.idle_data = 0
        self.idle_addr = 0
        self.load_mode = False
        self.save_mode = False

        # Instanciate the view
        self.gui = ExecutionFrame(self.config, self.sig_config_changed)

        # Instanciate the CPU
        self.cpu = Cpu(self.config, self.sig_cpu_stopped)

        # Sets idle mode by default
        self.set_idle_mode()
    
    # 
    # Signals handling
    # 

    @Slot(str)
    def on_config_changed(self, new_value):
        """
        Updates the stored value for the current digirule model in the configuration file

        :param new_value: new digirule model value
        """
        self.config.set('digirule', 'DR_MODEL', new_value)

        with open(CONFIG_FILE_PATH, 'w') as configfile:
            self.config.write(configfile)
        
        # Instanciate a new CPU
        self.cpu = Cpu(self.config, self.sig_cpu_stopped)
    
    @Slot(str)
    def on_cpu_stopped(self, exception):
        self.set_idle_mode()
        # display on statusbar
        self.gui.statusbar.set_status_message("CPU stopped : " + exception)

    #
    # set modes
    #

    def set_idle_mode(self):
        # configure the callbacks to the normal (stop) mode
        self.gui.dr_canvas.on_btn_load = self.cb_idle_load
        self.gui.dr_canvas.on_btn_save = self.cb_idle_save
        self.gui.dr_canvas.on_btn_store = self.cb_idle_store
        self.gui.dr_canvas.on_btn_goto = self.cb_idle_goto
        self.gui.dr_canvas.on_btn_run = self.cb_idle_run
        self.gui.dr_canvas.on_btn_next = self.cb_idle_next
        self.gui.dr_canvas.on_btn_prev = self.cb_idle_prev
        self.gui.dr_canvas.on_d = self.cb_idle_dx

        # update the control leds
        self.gui.dr_canvas.set_running_leds(False)

        # Run the CPU
        self.cpu.run = False


    def set_run_mode(self):
        # configure the callbacks to the normal mode
        self.gui.dr_canvas.on_btn_load = self.cb_run_load
        self.gui.dr_canvas.on_btn_save = self.cb_run_save
        self.gui.dr_canvas.on_btn_store = self.cb_run_store
        self.gui.dr_canvas.on_btn_goto = self.cb_run_goto
        self.gui.dr_canvas.on_btn_run = self.cb_run_run
        self.gui.dr_canvas.on_btn_next = self.cb_run_next
        self.gui.dr_canvas.on_btn_prev = self.cb_run_prev
        self.gui.dr_canvas.on_d = self.cb_run_dx

        # update the control leds
        self.gui.dr_canvas.set_running_leds(True)

        # Run the CPU
        self.cpu.run = True
    
    #
    # idle mode methods
    #
    def update_idle_leds(self):
        self.idle_data = self.cpu.ram[self.idle_addr]
        self.gui.dr_canvas.set_row_state(True, self.idle_addr, False)
        self.gui.dr_canvas.set_row_state(False, self.idle_data, True)
    def cb_idle_load(self):
        """button in normal mode"""
        self.save_mode = False
        self.load_mode = True
    def cb_idle_save(self):
        """button in normal mode"""
        self.save_mode = True
        self.load_mode = False
    def cb_idle_store(self):
        """button in normal mode"""
        self.cpu.ram[self.idle_addr] = self.idle_data
        self.idle_addr = (self.idle_addr + 1) % 256
        self.update_idle_leds()
    def cb_idle_goto(self):
        """button in normal mode"""
        self.idle_addr = self.idle_data
        self.update_idle_leds()
    def cb_idle_run(self):
        """button in normal mode"""
        self.set_run_mode()
    def cb_idle_next(self):
        """button in normal mode"""
        self.idle_addr = (self.idle_addr + 1) % 256
        self.update_idle_leds()
    def cb_idle_prev(self):
        """button in normal mode"""
        self.idle_addr = (self.idle_addr - 1) % 256
        self.update_idle_leds()
    def cb_idle_dx(self, btn):
        """Button Dx pressed in idle mode"""
        self.idle_data ^= 2**btn
        self.gui.dr_canvas.set_row_state(False, self.idle_data, True)

    #
    # run mode methods
    #

    def cb_run_load():
        """button in run mode"""
        pass
    def cb_run_save(self):
        """button in run mode"""
        pass
    def cb_run_store(self):
        """button in run mode"""
        pass
    def cb_run_goto(self):
        """button in run mode"""
        pass
    def cb_run_run(self):
        """button in run mode"""
        self.set_idle_mode()
    def cb_run_next(self):
        """button in run mode"""
        pass
    def cb_run_prev(self):
        """button in run mode"""
        pass
    def cb_run_dx(self, btn):
        """Button Dx pressed in normal mode"""
        pass

    #
    # Action button methods
    #

    def load_ram(i):   
        """loads a program (n°i) to the RAM from the flash memory """
        with open('flash_memory.txt', 'r', encoding='utf-8') as f:
            flash_memory = f.readlines() 
        start = 256*i # where the program n°i starts in the flash memory
        new_ram = []
        for j in range(start, start+256):
            new_ram.append(int(flash_memory[j][:-1]))
        cpu.set_ram(new_ram)

    def save_ram(i): 
        """ saves RAM to a program n°i on the flash memory"""
        with open('flash_memory.txt', 'r', encoding='utf-8') as f:
            flash_memory = f.readlines() 
        start = 256*i # where the program n°i starts in the flash memory
        with open('flash_memory.txt', 'w', encoding='utf-8') as f:
            for j in range(0, start):
                f.write(flash_memory[j])
            for j in range(start, start + 256):
                f.write(str(cpu.ram[j-start])+'\n')
            for j in range(start + 256, len(flash_memory)):
                f.write(flash_memory[j])