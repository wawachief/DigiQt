from configparser import ConfigParser
from PySide2.QtCore import Signal, Slot, QObject, QThread, QTimer, SIGNAL
from time import sleep
from threading import Thread

from src.model.cpu import Cpu
from src.model.assemble import Assemble
from src.debugger import Debug
from src.serialControler import SerialControl
from src.view.MainAppFrame import ExecutionFrame

CONFIG_FILE_PATH = 'src/config.ini'

class CpuThread(QThread):
    """Calls ticks the CPU all the time when CPU is in run mode"""
    def __init__(self, cpu, speed_fact=20, parent = None):
        QThread.__init__(self, parent)
        self.cpu        = cpu
        self.running    = True
        self.inst_timer = 0
        self.speed_factor = speed_fact

    def run(self):
        while self.running:
            if self.cpu.run:
                if self.inst_timer >= self.cpu.speed * self.speed_factor :
                    self.cpu.tick()
                    self.inst_timer = 0
                # 50000 cycles per second in speed 0 configuration
                # adjust speed with cpu.speed value
                sleep(0.00001)
                self.inst_timer += 1

class Controller(QObject):
    # Signals declarations
    sig_config_changed = Signal(str)
    sig_cpu_stopped = Signal(str)
    sig_cpu_speed = Signal(str)

    def __init__(self):
        QObject.__init__(self)

        # signals configuration
        self.sig_config_changed.connect(self.on_config_changed)
        self.sig_cpu_stopped.connect(self.on_cpu_stopped)
        self.sig_cpu_speed.connect(self.on_cpu_speed_chg)

        # Read configuration
        self.config = ConfigParser()
        self.config.read(CONFIG_FILE_PATH)
        self.dr_model = self.config.get('digirule', 'DR_MODEL')

        # Controller attributes
        self.idle_data = 0
        self.idle_addr = 0
        self.load_mode = False
        self.save_mode = False
        self.show_run_adr = True 
        self.symbol_table, self.labels_table = None, None
        # Animation attributes
        self.anim_boot   = 0   # boot animation
        self.anim_adrLED = 0   # LED address animation

        # Instanciate the view
        self.gui = ExecutionFrame(self.config, self.sig_config_changed)
        self.gui.dr_canvas.on_btn_power = self.do_quit
        self.gui.do_quit = self.do_quit

        self.cpu = None
        self.init_state()

        # Callbacks
        self.gui.editor_frame.assemble_btn.on_assemble = self.assemble_click
        self.gui.slider.value_changed = self.on_speedslider_change

        # Sets the initial state
        self.set_idle_mode()

        # run UI update timer
        self.ui_timer = QTimer(parent = self)
        self.connect(self.ui_timer, SIGNAL('timeout()'), self.update_ui)
        self.ui_timer.start(50) # ui refresh every 50 ms

    def init_state(self):
        """Instantiate the main compnents
        must be called when digirule changes"""
        
        # Instanciate the CPU
        self.cpu = Cpu(self.config, self.sig_cpu_stopped, self.sig_cpu_speed)
        #
        # Run cpu thread and UI update
        #
        self.cpu_thread = CpuThread(self.cpu, parent = None)
        self.cpu_thread.start()

        # Instanciate the debugger
        self.dbg = Debug(self.cpu, self.gui.ram_frame)

        # change attribute in editor for coloration
        self.gui.editor_frame.editor.highlight.init_rules(self.cpu.inst_dic)
        self.do_view_ram()

        # Instantiate the serial controler
        if self.dr_model == "2U":
            self.serialctl = SerialControl(self.cpu, self.gui.monitor_frame, self.gui.statusbar, self.config)
        else:
            self.serialctl = None

    def update_ui(self):
        """This method is responsible for updating the UI in run mode and
        for the animations in idle mode.
        Is is called every 50 ms by a timer"""
        if self.cpu is not None:
            if self.cpu.run == True:
                # we are in run mode, we handle the LEDs
                if self.show_run_adr:
                    if self.cpu.ram[self.cpu.REG_STATUS] & 4 ==0 :
                        self.gui.dr_canvas.set_row_state(True, self.cpu.ram[self.cpu.pc], False)
                    else:
                        self.gui.dr_canvas.set_row_state(True, self.cpu.ram[self.cpu.REG_ADDRLED], False)
                self.gui.dr_canvas.set_row_state(False, self.cpu.ram[self.cpu.REG_DATALED], True)
                self.do_view_ram()
            else:
                # we are in idle mode, we handle the animations
                if self.anim_boot != 0:
                    # Animation clear memory
                    if self.anim_boot % 2 ==0:
                        self.do_blink()
                    self.anim_boot -= 1
                    if self.anim_boot == 1:
                        # end animation
                        self.update_idle_leds()
                if self.anim_adrLED != 0:
                    # Animation de la barre de LED
                    if self.anim_adrLED % 2 ==0:
                        self.do_progress()
                    self.anim_adrLED -= 1
                    if self.anim_adrLED == 1:
                        # end animation
                        self.update_idle_leds()

    # 
    # Signals handling
    # 

    @Slot(str)
    def on_config_changed(self, new_value):
        """
        Updates the stored value for the current digirule model in the configuration file

        :param new_value: new digirule model value
        """
        if self.cpu is not None:
            # Stops the old CPU
            self.cpu_thread.running = False
            sleep(0.01)
        self.config.set('digirule', 'DR_MODEL', new_value)
        self.dr_model = new_value

        with open(CONFIG_FILE_PATH, 'w') as configfile:
            self.config.write(configfile)
        
        # Reinstatiate CPU and all the important stuff
        self.init_state()
    
    @Slot(str)
    def on_cpu_stopped(self, exception):
        self.set_idle_mode()
        self.idle_addr = self.cpu.pc
        self.update_idle_leds()
        self.do_view_ram()
        # display on statusbar
        self.gui.statusbar.sig_persistent_message.emit("CPU stopped : " + exception)

    @Slot(str)
    def on_cpu_speed_chg(self, new_speed):
        # Speed changed, update the speed scale
        self.gui.statusbar.sig_temp_message.emit("Change CPU speed : " + new_speed)
        self.gui.slider.setValue(int(new_speed))
    
    #
    # other events methods
    #
    def on_speedslider_change(self):
        """speed slider ha changed"""
        self.cpu.speed = self.gui.slider.value()
        self.gui.statusbar.sig_temp_message.emit("Change CPU speed : " + str(self.cpu.speed))

    #
    # set modes
    #

    def set_idle_mode(self):
        """The digirule enters idle mode. We reconfigure all the calbacks methods"""
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
        self.gui.dr_canvas.on_btn_ram = self.cb_idle_step

        # update the control leds
        self.gui.dr_canvas.set_running_leds(False)



    def set_run_mode(self):
        """The digirule enters run mode. We reconfigure all the calbacks methods"""
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
        self.gui.dr_canvas.on_btn_ram = self.do_view_ram

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
        self.do_view_ram()
    def cb_idle_load(self):
        """button in normal mode"""
        self.save_mode = False
        self.load_mode = True
        self.anim_adrLED = 16
    def cb_idle_save(self):
        """button in normal mode"""
        self.save_mode = True
        self.load_mode = False
        self.anim_adrLED = 16
    def cb_idle_store(self):
        """button in normal mode"""
        self.cpu.ram[self.idle_addr] = self.idle_data
        self.idle_addr = (self.idle_addr + 1) % 256
        self.update_idle_leds()
    def cb_idle_goto(self):
        """button in normal mode"""
        self.idle_addr = self.idle_data
        self.cpu.set_pc(self.idle_addr)
        self.update_idle_leds()
    def cb_idle_run(self):
        """button in normal mode"""
        self.gui.statusbar.sig_temp_message.emit("Entering run mode")
        self.set_run_mode()
    def cb_idle_next(self):
        """button in normal mode"""
        if self.save_mode:
            self.save_mode = False
            if self.serialctl is None:
                self.gui.statusbar.sig_temp_message.emit("No serial capability on this model")
            else:
                self.serialctl.to_digirule()
        else:
            self.idle_addr = (self.idle_addr + 1) % 256
            self.cpu.pc = self.idle_addr
            self.update_idle_leds()
    def cb_idle_prev(self):
        """button in normal mode"""
        if self.load_mode:
            self.cb_idle_clear()
            self.load_mode = False
        else:
            self.idle_addr = (self.idle_addr - 1) % 256
            self.cpu.pc = self.idle_addr
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
        self.gui.statusbar.sig_temp_message.emit("Memory clear")
        self.cpu.clear_ram()
        self.do_view_ram()
        self.idle_addr = 0
        self.cpu.pc = 0
        self.anim_boot = 40
        self.update_idle_leds()
    def cb_idle_step(self):
        """step by step button. Cycle the cpu once"""
        self.cpu.tick()
        self.idle_addr = self.cpu.pc
        instruction = self.cpu.decode(self.idle_addr, self.symbol_table)
        self.gui.statusbar.sig_persistent_message.emit(instruction)
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
        if self.show_run_adr :
            self.gui.statusbar.sig_temp_message.emit("Show Address LEDs")
        else:
            self.gui.statusbar.sig_temp_message.emit("Hide Address LEDs")
    def cb_run_run(self):
        """button in run mode"""
        self.set_idle_mode()
        self.idle_addr = self.cpu.pc
        self.gui.statusbar.sig_temp_message.emit("Leaving run mode")
        self.do_view_ram()
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
    def cb_run_clear(self):
        """Button clear pressed in run mode"""
        self.gui.statusbar.sig_temp_message.emit("Don't clear memory while running !!")
        self.do_view_ram()
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
        # self.set_running_leds(i % 2 != 0, False)  # Don't repaint yet
        self.gui.dr_canvas.set_row_state(True, 170 if (self.anim_boot//2) % 2 == 0 else 85, False)  # Don't repaint yet
        self.gui.dr_canvas.set_row_state(False, 85 if (self.anim_boot//2) % 2 == 0 else 170)

    def do_progress(self):
        """
        make a progress bar with the data_leds
        """
        n = 10 - self.anim_adrLED//2
        n = max(1, 2**n - 1)
        self.gui.dr_canvas.set_row_state(False, n)

    def do_quit(self):
        # Kill the cpu thread and quit the app
        self.cpu_thread.running = False
        sleep(0.1)
        self.gui.close()
        print("Bye")

    def do_view_ram(self):
        self.dbg.view_ram(0) # decmode

    #
    # Other methods
    #

    def load_ram(self, i):   
        """loads a program (n°i) to the RAM from the flash memory """

        self.gui.statusbar.sig_temp_message.emit("Loading program "+str(i))
        with open('src/flash_memory.txt', 'r', encoding='utf-8') as f:
            flash_memory = f.readlines() 
        start = 256*i # where the program n°i starts in the flash memory
        new_ram = []
        for j in range(start, start+256):
            new_ram.append(int(flash_memory[j][:-1]))
        self.cpu.set_ram(new_ram)
        self.cpu.set_pc(0)
        self.symbol_table = None
        self.do_view_ram()

    def save_ram(self, i): 
        """ saves RAM to a program n°i on the flash memory"""

        self.gui.statusbar.sig_temp_message.emit("Saving program "+str(i))
        with open('src/flash_memory.txt', 'r', encoding='utf-8') as f:
            flash_memory = f.readlines() 
        start = 256*i # where the program n°i starts in the flash memory
        with open('src/flash_memory.txt', 'w', encoding='utf-8') as f:
            for j in range(0, start):
                f.write(flash_memory[j])
            for j in range(start, start + 256):
                f.write(str(self.cpu.ram[j-start])+'\n')
            for j in range(start + 256, len(flash_memory)):
                f.write(flash_memory[j])
    
    def assemble_click(self):
        text = self.gui.editor_frame.retrieve_text()
        asm = Assemble(text,self.cpu.inst_dic)
        res = asm.parse()
        if res[0]:
            # Compilation success
            self.gui.statusbar.sig_temp_message.emit("Compilation Success. Occupation " + str(len(res[1])) + " / 252")
            self.symbol_table, self.labels_table = res[2], res[3]
            self.cpu.set_ram(res[1])
            self.update_idle_leds()
        else:
            # Compilation error
            self.gui.statusbar.sig_persistent_message.emit(res[1])
            self.symbol_table, self.labels_table = None, None
        self.cpu.set_pc(0)
        self.do_view_ram()
    