import serial
import serial.tools.list_ports as list_ports
from PySide2.QtCore import QObject, QThread
from time import sleep

class InitSerialThread(QThread):
    """Initialize the serial port in background"""
    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.parent = parent

        # Serial port configuration
        self.port      = parent.config.get("serial","port")
        self.baudrate  = int(parent.config.get("serial","baudrate"))
        self.timeout   = float(parent.config.get("serial","TIMEOUT"))

    def run(self):
        list_available_ports =  [p.device for p in list_ports.comports()]
        if self.port in list_available_ports:
            self.parent.ser_port = serial.Serial(timeout=self.timeout)
            self.parent.ser_port.baudrate = self.baudrate
            self.parent.ser_port.port = self.port
            self.parent.init_OK()
        else:
            self.parent.ser_port = None

class SerialControl(QObject):
    def __init__(self, cpu, monitor_frame, statusbar, config):
        QObject.__init__(self)

        self.cpu       = cpu
        self.monitor   = monitor_frame
        self.statusbar = statusbar
        self.config    = config
        self.ser_port  = None
        self.init_serial()
        
    def init_serial(self):
        is_thread = InitSerialThread(self)
        is_thread.start()

    def init_OK(self):
        self.statusbar.sig_temp_message.emit("Serial port Initialized")

    def to_digirule(self):
        if self.ser_port is None:
            self.statusbar.sig_temp_message.emit("Error : No serial port configured")
        else:
            dump = self.ram2hex(self.cpu.ram)
            self.statusbar.sig_temp_message.emit("Dumpimg memory on port " + self.ser_port.port)
            try:
                self.ser_port.open()
            except serial.serialutil.SerialException as ex:
                self.statusbar.sig_temp_message.emit(ex)
            else:
                for line in dump.splitlines():
                    self.ser_port.write(line.encode("utf-8"))
                    sleep(0.1)
                sleep(2)
                self.ser_port.close()
                self.statusbar.sig_temp_message.emit("Memory sent")

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