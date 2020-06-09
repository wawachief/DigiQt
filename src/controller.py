from configparser import ConfigParser
from PySide2.QtCore import Signal, Slot, QObject
from time import sleep
from threading import Thread

from src.model.cpu import Cpu
from src.model.assemble import Assemble
from src.view.MainApp import ExecutionFrame

CONFIG_FILE_PATH = 'src/config.ini'

class Controller(QObject):
    # Signals declarations
    sig_config_changed = Signal(str)
    sig_cpu_stopped = Signal(str)
    sig_cpu_tick  = Signal(bool)

    def __init__(self):
        QObject.__init__(self)

        # signals configuration
        self.sig_config_changed.connect(self.on_config_changed)
        self.sig_cpu_stopped.connect(self.on_cpu_stopped)
        self.sig_cpu_tick.connect(self.on_cpu_tick)

        # Read configuration
        self.config = ConfigParser()
        self.config.read(CONFIG_FILE_PATH)
        dr_model = self.config.get('digirule', 'DR_MODEL')
        
        # Controller attributes
        self.idle_data = 0
        self.idle_addr = 0
        self.load_mode = False
        self.save_mode = False
        self.show_run_adr = True 

        # Instanciate the view
        self.gui = ExecutionFrame(self.config, self.sig_config_changed)
        self.gui.dr_canvas.on_btn_power = self.do_quit
        self.gui.do_quit = self.do_quit

        # Instanciate the CPU
        self.cpu = Cpu(self.config, self.sig_cpu_stopped)

        # Sets idle mode by default
        self.set_idle_mode()

        # Launch the main CPU thread
        self.running = True
        self.cpu_run_thread = Thread(target = self.run_cpu, args = (self.sig_cpu_tick, ))
        self.cpu_run_thread.start()
    
    #
    # Run cpu thread
    #
    def run_cpu(self, tick_signal):
        while self.running:
            # update running LEDS
            if self.cpu.run:
                self.cpu.tick()
                tick_signal.emit(True)
                # 1 cyle every millisecond
                speed = 0.0001 * self.cpu.speed**2
                sleep(speed)

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

    @Slot(bool)
    def on_cpu_tick(self, b):
        if self.show_run_adr:
            if self.cpu.ram[self.cpu.REG_STATUS] & 4 ==0 :
                self.gui.dr_canvas.set_row_state(True, self.cpu.ram[self.cpu.pc], False)
            else:
                self.gui.dr_canvas.set_row_state(True, self.cpu.ram[self.cpu.REG_ADDRLED], False)
        self.gui.dr_canvas.set_row_state(False, self.cpu.ram[self.cpu.REG_DATALED], True)
    #
    # set modes
    #

    def set_idle_mode(self):
        # Stop the CPU
        self.cpu.run = False

        # configure the callbacks to the normal (stop) mode
        self.gui.dr_canvas.on_btn_load = self.cb_idle_load
        self.gui.dr_canvas.on_btn_save = self.cb_idle_save
        self.gui.dr_canvas.on_btn_store = self.cb_idle_store
        self.gui.dr_canvas.on_btn_goto = self.cb_idle_goto
        self.gui.dr_canvas.on_btn_run = self.cb_idle_run
        self.gui.dr_canvas.on_btn_next = self.cb_idle_next
        self.gui.dr_canvas.on_btn_prev = self.cb_idle_prev
        self.gui.dr_canvas.on_btn_clear = self.cb_idle_clear
        self.gui.dr_canvas.on_d = self.cb_idle_dx

        # update the control leds
        self.gui.dr_canvas.set_running_leds(False)



    def set_run_mode(self):
        # configure the callbacks to the normal mode
        self.gui.dr_canvas.on_btn_load = self.cb_run_load
        self.gui.dr_canvas.on_btn_save = self.cb_run_save
        self.gui.dr_canvas.on_btn_store = self.cb_run_store
        self.gui.dr_canvas.on_btn_goto = self.cb_run_goto
        self.gui.dr_canvas.on_btn_run = self.cb_run_run
        self.gui.dr_canvas.on_btn_next = self.cb_run_next
        self.gui.dr_canvas.on_btn_prev = self.cb_run_prev
        self.gui.dr_canvas.on_btn_clear = self.cb_run_clear
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
        self.do_progress()
    def cb_idle_save(self):
        """button in normal mode"""
        self.save_mode = True
        self.load_mode = False
        self.do_progress()
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
        self.cpu.pc = self.idle_addr
        self.set_run_mode()
    def cb_idle_next(self):
        """button in normal mode"""
        self.idle_addr = (self.idle_addr + 1) % 256
        self.update_idle_leds()
    def cb_idle_prev(self):
        """button in normal mode"""
        self.idle_addr = (self.idle_addr - 1) % 256
        self.update_idle_leds()
    def cb_idle_dx(self, btn, is_pressed):
        """Button Dx pressed in idle mode"""
        if is_pressed:
            if self.load_mode:
                self.load_ram(btn)
                self.load_mode = False
                self.idle_addr = 0
                self.update_idle_leds()
            elif self.save_mode:
                self.save_ram(btn)
                self.save_mode = False
                self.idle_addr = 0
                self.update_idle_leds()
            else:
                self.idle_data ^= 2**btn
                self.gui.dr_canvas.set_row_state(False, self.idle_data, True)
    def cb_idle_clear(self):
        """Button clear pressed in clear mode"""
        self.cpu.clear_ram()
        self.idle_addr = 0
        self.do_blink()
        self.update_idle_leds()

    #
    # run mode methods
    #

    def cb_run_load(self):
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
        self.gui.dr_canvas.set_row_state(True, 0, False)
        self.show_run_adr = not self.show_run_adr
    def cb_run_run(self):
        """button in run mode"""
        self.set_idle_mode()
        self.idle_addr = self.cpu.pc
        self.update_idle_leds()
    def cb_run_next(self):
        """button in run mode"""
        pass
    def cb_run_prev(self):
        """button in run mode"""
        pass
    def cb_run_dx(self, btn, is_pressed):
        """Button Dx pressed in run mode"""
        if is_pressed:
            self.cpu.ram[self.cpu.REG_BUTTON] = 2**btn
        else:
            self.cpu.ram[self.cpu.REG_BUTTON] = 0
        print(btn, is_pressed)
    def cb_run_clear(self):
        """Button clear pressed in run mode"""
        pass

    #
    # action methods
    #

    def do_blink(self):
        """
        Performs a blink 10 times on the 2 LEDs rows.

        85 represents 01010101
        170 represents 10101010
        """
        for i in range(1, 20):
            # self.set_running_leds(i % 2 != 0, False)  # Don't repaint yet
            self.gui.dr_canvas.set_row_state(True, 170 if i % 2 == 0 else 85, False)  # Don't repaint yet
            self.gui.dr_canvas.set_row_state(False, 85 if i % 2 == 0 else 170)
            sleep(.08)

    def do_progress(self):
        """
        make a progress bar with the data_leds
        """
        n = 0
        for i in range(8):
            n = 2*n + 1
            self.gui.dr_canvas.set_row_state(False, n)
            sleep(.1)

    def do_quit(self):
        # Kill the cpu thread and quit the app
        self.running = False
        sleep(0.1)
        self.gui.close()
        print("Bye")


    #
    # Other methods
    #

    def load_ram(self, i):   
        """loads a program (n°i) to the RAM from the flash memory """
        with open('src/flash_memory.txt', 'r', encoding='utf-8') as f:
            flash_memory = f.readlines() 
        start = 256*i # where the program n°i starts in the flash memory
        new_ram = []
        for j in range(start, start+256):
            new_ram.append(int(flash_memory[j][:-1]))
        self.cpu.set_ram(new_ram)

    def save_ram(self, i): 
        """ saves RAM to a program n°i on the flash memory"""
        with open('flash_memory.txt', 'r', encoding='utf-8') as f:
            flash_memory = f.readlines() 
        start = 256*i # where the program n°i starts in the flash memory
        with open('src/flash_memory.txt', 'w', encoding='utf-8') as f:
            for j in range(0, start):
                f.write(flash_memory[j])
            for j in range(start, start + 256):
                f.write(str(self.cpu.ram[j-start])+'\n')
            for j in range(start + 256, len(flash_memory)):
                f.write(flash_memory[j])
    