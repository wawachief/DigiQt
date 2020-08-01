# Author: Olivier Lécluse
# License GPL-3

#
# Digirule CPU Core
#

import serial
import serial.tools.list_ports as list_ports
from PySide2.QtCore import QObject, QThread, Signal, Slot, QTimer, QProcess
from time import sleep
from src.hex_utils import ram2hex, hex2ram
import queue as Queue
import sys

NO_SERIAL = "No serial available"
SELECT_SERIAL = "Select..."


class InitSerialThread(QThread):
    """Initialize the serial port in background"""
    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.parent = parent

        # Serial port configuration
        dr_model = parent.config.get('digirule', 'dr_model')
        self.port      = parent.config.get("serial","port")
        self.baudrate  = int(parent.config.get(dr_model,"baudrate"))
        self.timeout   = parent.config.getfloat("serial","timeout")
        self.update_combo = None # pushed by controler
        self.do_refresh = False  # we hit refresh button

    def run(self):
        list_available_ports = [p.device for p in list_ports.comports()]
        if not list_available_ports:
            list_available_ports = [NO_SERIAL]
        else:
            list_available_ports.insert(0, SELECT_SERIAL)
        if self.do_refresh:
            self.update_combo(list_available_ports)
            self.do_refresh = False
        if self.port in list_available_ports and self.port not in (NO_SERIAL, SELECT_SERIAL):
            self.update_combo(None, self.port)
            self.parent.ser_port = serial.Serial(timeout=self.timeout)
            self.parent.ser_port.baudrate = self.baudrate
            self.parent.ser_port.port = self.port
            self.parent.init_OK()
        else:
            self.parent.ser_port = None


class FromDigiruleThread(QThread):
    """Receive memory dump from Digirule"""
    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.parent = parent
        self.running = True

    def run(self):
        try:
            self.parent.ser_port.open()
        except serial.serialutil.SerialException as ex:
            self.parent.statusbar.sig_temp_message.emit(ex.strerror)
        else:
            # Serial port is open
            while (self.parent.ser_port.in_waiting == 0) and self.running:
                # Wait for incoming transmission
                pass
            if self.running:
                self.parent.cpu.run = False
                self.parent.statusbar.sig_temp_message.emit("Digirule is transmitting")
                listdump = self.parent.ser_port.readlines()
                hexdump = ""
                # Decoding hexdump
                for line in listdump:
                    hexdump += line.decode('utf-8')
                try:
                    newram = hex2ram(hexdump)
                except ValueError:
                    self.parent.statusbar.sig_temp_message.emit("Checksum error")
                else:
                    # Ram is received and no checksum error
                    # writing newram in RAM
                    self.parent.statusbar.sig_temp_message.emit("Memory received")
                    for i, r in enumerate(newram):
                        self.parent.cpu.ram[i] = r
                    self.parent.sig_update.emit("from digirule complete")
            else:
                self.parent.statusbar.sig_temp_message.emit("Abort receive")
            self.parent.ser_port.close()


# Thread to handle terminal serial 
class SerialThread(QThread):
    def __init__(self, parent):  # Initialise with serial port details
        QThread.__init__(self)

        self.parent = parent
        self.ser = self.parent.ser_port
        self.txq = Queue.Queue()
        self.running = True
 
    def ser_out(self, s):   
        self.txq.put(s)                     # ..using a queue to sync with reader thread
         
    def ser_in(self, s):                    # Write incoming serial data to screen
        self.display(s)

    def bytes_str(self, d):
            return d if type(d) is str else "".join([chr(b) for b in d])

    def display(self, s):
        def textdump(data):
        # Return a string with high-bit chars replaced by hex values
            return "".join(["[%02X]" % ord(b) if b>'\x7e' else b for b in data])
        self.parent.terminal.write(textdump(str(s)))

    def run(self):
        if self.ser is not None:
            self.parent.terminal.write(f"Opening {self.ser.port} at {self.ser.baudrate} baud")
            self.parent.terminal.write('\x0d')
            try:
                self.ser.open()
                self.ser.flushInput()
            except:
                self.ser = None
        if not self.ser:
            self.parent.terminal_frame.write("Can't open port")
            self.running = False
        while self.running:
            s = self.ser.read(self.ser.in_waiting or 1)
            if s:                                       # Get data from serial port
                self.ser_in(self.bytes_str(s))               # ..and convert to string
            if not self.txq.empty():
                txd = str(self.txq.get())               # If Tx data in queue, write to serial port
                self.ser.write(txd.encode('latin-1'))
        if self.ser:                                    # Close serial port when thread finished
            self.ser.close()
            self.ser = None

class SerialControl(QObject):
    sig_keyseq_pressed = Signal(str)
    sig_CPU_comout     = Signal(str)
    sig_CPU_comin      = Signal(str)
    sig_port_change    = Signal(str)
    sig_button_pressed = Signal(int)
    sig_terminal_open  = Signal(bool)
    sig_firmware_update  = Signal(str)

    def __init__(self, cpu, monitor_frame, terminal_frame, usb_frame, statusbar, config, sig_update, config_file_path):
        QObject.__init__(self)

        self.cpu       = cpu
        self.monitor   = monitor_frame
        self.terminal   = terminal_frame
        self.statusbar = statusbar
        self.config    = config
        self.ser_port  = None
        self.sig_update = sig_update
        self.fd_thread = None
        self.fwth = None
        self.monitor_frame = monitor_frame
        self.usb_frame = usb_frame
        self.config_file_path = config_file_path

        # Connect signal
        self.sig_keyseq_pressed.connect(self.on_key_pressed)
        self.sig_CPU_comout.connect(self.on_comout)
        self.sig_CPU_comin.connect(self.on_comin)
        self.sig_port_change.connect(self.on_port_change)
        self.sig_button_pressed.connect(self.on_button_dispatch)
        self.sig_terminal_open.connect(self.on_terminal_open)
        self.sig_firmware_update.connect(self.on_firmware_update)

        self.monitor_frame.sig_keyseq_pressed = self.sig_keyseq_pressed
        self.monitor_frame.sig_button_pressed = self.sig_button_pressed
        self.cpu.sig_CPU_comout = self.sig_CPU_comout
        self.cpu.sig_CPU_comin = self.sig_CPU_comin
        self.usb_frame.usb_combo.sig_port_change = self.sig_port_change
        self.usb_frame.sig_button_pressed = self.sig_button_pressed
        self.usb_frame.sig_firmware_update = self.sig_firmware_update

        self.terminal.sig_terminal_open = self.sig_terminal_open
        
        self.init_serial()

    def init_serial(self, do_refresh=True):
        is_thread = InitSerialThread(self)
        is_thread.update_combo = self.usb_frame.usb_combo.set_ports
        is_thread.do_refresh = do_refresh
        is_thread.start()

    def init_OK(self):
        self.statusbar.sig_temp_message.emit("Serial port Initialized")

    #
    # Signal Handling
    #
    @Slot(str)
    def on_key_pressed(self, key):
        if self.cpu.rx is None and len(key) == 1:
            self.cpu.rx = key
            self.monitor_frame.serial_in.setText(key)

    @Slot(str)
    def on_comin(self, char):
        """Char is handled by CPU, we free the slot"""
        self.monitor_frame.serial_in.setText(" ")

    @Slot(str)
    def on_comout(self, char):
        """Append the char to the console"""
        try:
            self.monitor_frame.append_serial_out(char)
        except ValueError:            
            self.monitor_frame.append_serial_out("?")


    @Slot(str)
    def on_port_change(self, port):
        self.config.set("serial", "port", port)
        if self.ser_port:
            self.ser_port.port = port
        with open(self.config_file_path, 'w') as configfile:
            self.config.write(configfile)
        self.init_serial(False)

    @Slot(int)
    def on_button_dispatch(self, btn_nbr):
        if btn_nbr == 0:
            self.to_digirule()
        elif btn_nbr == 1:
            self.from_digirule()
        elif btn_nbr == 2:
            self.init_serial()
        elif btn_nbr == 3:
            self.on_clear_button()

    @Slot(bool)
    def on_terminal_open(self, is_open):
        if is_open:
            # Terminal window is open : create the terminal serial thread
            self.statusbar.sig_temp_message.emit("open terminal thread")
            self.terminal.serth = SerialThread(self)   # Start serial thread
            self.terminal.serth.start()
        else:
            # Terminal window is closed : quit the terminal serial thread
            if self.terminal.serth:
                self.terminal.serth.running = False
                sleep(0.5)
                self.terminal.serth = None

    def on_clear_button(self):
        self.monitor_frame.clear()  # Clear the serial in/out content
        self.cpu.rx = None
        self.cpu.tx = None

    def to_digirule(self):
        if self.ser_port is None:
            self.statusbar.sig_temp_message.emit("Error : No serial port configured")
        else:
            dump = ram2hex(self.cpu.ram)
            self.statusbar.sig_temp_message.emit("Dumpimg memory on port " + self.ser_port.port)
            try:
                self.ser_port.open()
            except serial.serialutil.SerialException as ex:
                self.statusbar.sig_temp_message.emit(ex.strerror)
            else:
                for line in dump.splitlines():
                    self.ser_port.write(line.encode("utf-8"))
                    sleep(0.1)
                sleep(2)
                self.ser_port.close()
                self.statusbar.sig_temp_message.emit("Memory sent")

    def from_digirule(self):
        """Launch receive sequence in background"""
        if self.ser_port:
            self.statusbar.sig_temp_message.emit("Waiting to receive Digirule on " + self.ser_port.port)
            self.fd_thread = FromDigiruleThread(self)
            self.fd_thread.start()
        else:
            self.init_serial()
    
    @Slot(str)
    def on_firmware_update(self, filepath):
        if self.ser_port:
            self.proc = QProcess(self)
            self.proc.readyReadStandardOutput.connect(self.stdoutReady)
            self.proc.readyReadStandardError.connect(self.stderrReady)

            if sys.platform == "win32":
                udr2 = f"cli\\udr2-win32.exe"
                command = f'{udr2} --program {self.ser_port.port} < {filepath}'
                self.usb_frame.out.write("Firmware update started, please wait ")
                # displays running dots on windows to pretend it is not stalled
                self.bullshitTimer = QTimer()
                self.bullshitTimer.timeout.connect(self.stdoutBullshit)
                self.bullshitTimer.start(1000)
                self.proc.setProcessChannelMode(QProcess.MergedChannels)
                self.proc.start('cmd.exe', ['/c' , command])
            else:
                udr2 = f"cli/udr2-{sys.platform}"
                command = f'{udr2} --program {self.ser_port.port} < "{filepath}"'
                self.bullshitTimer = None
                self.proc.start('bash', ['-c' , command])
            # print(command)
            
    
    def stdoutBullshit(self):
        self.usb_frame.out.write(".")

    def stdoutReady(self):
        if self.bullshitTimer:
            self.usb_frame.out.write("\n")
            self.bullshitTimer.stop()

        text = str(self.proc.readAllStandardOutput())
        self.usb_frame.out.write(eval(text).decode('iso8859-1'))

    def stderrReady(self):
        text = str(self.proc.readAllStandardError())
        self.usb_frame.out.write(eval(text).decode('iso8859-1'))