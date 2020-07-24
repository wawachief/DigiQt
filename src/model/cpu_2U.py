# Author: Olivier Lécluse
# License GPL-3

#
# Digirule CPU Core
#

from PySide2.QtCore import Signal, Slot, QObject
from random import randint
from src.model.cpu import Core

class Cpu(Core):
    def __init__(self, sig_cpu_stopped = None, sig_cpu_speed = None):
        super().__init__()
        self.sig_cpu_stopped = sig_cpu_stopped
        self.sig_cpu_speed = sig_cpu_speed

        # CPU configuration
        self.dr_model     = "2U"
        self.stack_size   = 64
        # attributes initialization
        self.stack  = [0] * self.stack_size    # CPU Stack
        self.serial_enable = True # enable Serial capability

        self.make_lookup_table()

    #
    # Instructions Implementation
    # Nothing to override since Core is 2U based
    