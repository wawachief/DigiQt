import serial
import serial.tools.list_ports as list_ports
from PySide2.QtCore import QObject, QThread, Signal, Slot
from time import sleep

NO_SERIAL = "No serial available"
SELECT_SERIAL = "Select..."


class InitSerialThread(QThread):
    """Initialize the serial port in background"""
    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.parent = parent

        # Serial port configuration
        self.port      = parent.config.get("serial","port")
        self.baudrate  = int(parent.config.get("serial","baudrate"))
        self.timeout   = float(parent.config.get("serial","TIMEOUT"))
        self.update_combo = None # pushed by controler
        self.do_refresh = False  # we hit refresh button

    def run(self):
        list_available_ports =  [p.device for p in list_ports.comports()]
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
                    newram = self.parent.hex2ram(hexdump)
                except ValueError:
                    self.parent.statusbar.sig_temp_message.emit("Checksum error")
                else:
                    # Ram is received and no checksum error
                    # writing newram in RAM
                    self.parent.statusbar.sig_temp_message.emit("Memory received")
                    for i,r in enumerate(newram):
                        self.parent.cpu.ram[i] = r
                    self.parent.sig_update.emit("from digirule complete")
            else:
                self.parent.statusbar.sig_temp_message.emit("Abort receive")
            self.parent.ser_port.close()

class SerialControl(QObject):
    sig_keyseq_pressed       = Signal(str)
    sig_CPU_comout           = Signal(str)
    sig_CPU_comin            = Signal(str)
    sig_port_change          = Signal(str)
    sig_clearconsole_pressed = Signal()

    def __init__(self, cpu, monitor_frame, statusbar, config, sig_update, config_file_path):
        QObject.__init__(self)

        self.cpu       = cpu
        self.monitor   = monitor_frame
        self.statusbar = statusbar
        self.config    = config
        self.ser_port  = None
        self.sig_update = sig_update
        self.fd_thread = None
        self.monitor_frame = monitor_frame
        self.config_file_path = config_file_path

        # Connect buttons to controler's methods
        self.monitor_frame.to_dr_btn.to_digirule = self.to_digirule
        self.monitor_frame.from_dr_btn.from_digirule = self.from_digirule
        self.monitor_frame.refresh_btn.on_refresh = self.init_serial

        
        # Connect signal
        self.sig_keyseq_pressed.connect(self.on_key_pressed)
        self.sig_CPU_comout.connect(self.on_comout)
        self.sig_CPU_comin.connect(self.on_comin)
        self.sig_port_change.connect(self.on_port_change)
        self.sig_clearconsole_pressed.connect(self.on_clear_button)

        self.monitor_frame.sig_keyseq_pressed = self.sig_keyseq_pressed
        self.monitor_frame.sig_clearconsole_pressed = self.sig_clearconsole_pressed
        self.cpu.sig_CPU_comout = self.sig_CPU_comout
        self.cpu.sig_CPU_comin = self.sig_CPU_comin
        self.monitor_frame.usb_combo.sig_port_change = self.sig_port_change
        
        self.keydict = {"Return": "\n", "Enter": chr(13), "Backspace":chr(8), "Esc":chr(27), "Del":chr(127)}

        self.init_serial()

    def init_serial(self, do_refresh = True):
        is_thread = InitSerialThread(self)
        is_thread.update_combo = self.monitor_frame.usb_combo.set_ports
        is_thread.do_refresh = do_refresh
        is_thread.start()

    def init_OK(self):
        self.statusbar.sig_temp_message.emit("Serial port Initialized")

    #
    # Signal Handling
    #
    @Slot(str)
    def on_key_pressed(self, key):
        if self.cpu.rx is None:
            if key in self.keydict:
                self.cpu.rx = self.keydict[key]
            elif len(key) == 1:
                self.cpu.rx = key
                self.monitor_frame.serial_in.setText(key)
            else:
                self.statusbar.sig_temp_message.emit(f"Unknown key: {key}")

    @Slot(str)
    def on_comin(self, char):
        """Char is handled by CPU, we free the slot"""
        self.monitor_frame.serial_in.setText(" ")

    @Slot(str)
    def on_comout(self, char):
        """Append the char to the console"""
        self.monitor_frame.append_serial_out(char)

    @Slot(str)
    def on_port_change(self, port):
        self.config.set("serial", "port", port)
        if self.ser_port:
            self.ser_port.port = port
        with open(self.config_file_path, 'w') as configfile:
            self.config.write(configfile)
        self.init_serial(False)
    @Slot()
    def on_clear_button(self):
        self.monitor_frame.serial_out.setPlainText("")  # Clear the serial out content
        self.monitor_frame.serial_in.setText(" ")       # Clear the serial input content
        self.cpu.rx = None
        self.cpu.tx = None

    def to_digirule(self):
        if self.ser_port is None:
            self.statusbar.sig_temp_message.emit("Error : No serial port configured")
        else:
            dump = self.ram2hex(self.cpu.ram)
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

    def ram2hex(self, ram):
        """converts the content of the ram into hex format"""
        def tohex(i):
            """converts an integer into hexadecimal on 2 caracters
            ex : tohex(8) -> '08' ; tohex(12) -> '0C'
            """
            return hex(i)[2:].rjust(2,'0').upper()

        hexdump = ""
        for line in range(16):
            nbcol = 12 if line == 15 else 16
            # Line header : nbcol (2 bytes) + address (2 bytes)
            newline = ':' + tohex(nbcol) + '00' + tohex(line * 16) + '00'
            control = nbcol + line * 16
            for col in range(nbcol):
                r = ram[line*16+col]
                control += r
                newline += tohex(r)
            newline += tohex((256-control)%256)
            hexdump += newline + '\n'
        hexdump += ":00000001FF"
        return hexdump

    def hex2ram(self, hexdump):
        """converts a dump from a digirule into ram content
        Line format  :BBAAAATTHHHHHH.....HHHHCC
        - BB est le nombre d'octets de données dans la ligne (en hexadécimal)
        - AAAA est l'adresse absolue (ou relative) du début de la ligne
        - TT est le champ spécifiant le type
        - HH...HHHH est le champ des données
        - CC est l'octet de checksum.
        """
        newram = [0]*256
        for line in hexdump.splitlines()[:-1]:
            BB = line[1:3]
            AAAA = line[3:7]
            DATA = line[9:-2]
            CC = line[-2:]

            B = int(f"0x{BB}",16)
            A = int(f"0x{AAAA}",16)
            C = int(f"0x{CC}",16)

            cs = B+A
            for i in range(B):
                HH = DATA[2*i:2*(i+1)]
                d = int(f"0x{HH}",16)
                if not (0 <= A+i < 256):
                    raise ValueError('Checksum Error')
                newram[A+i] = d
                cs += d
            if (cs+C)%256 != 0:
                raise ValueError('Checksum Error')
        return newram