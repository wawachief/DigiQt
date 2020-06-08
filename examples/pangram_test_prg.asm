%define status_reg 252
%define zero_bit   0
%define carry_bit  1

SBR 7 R0
SHIFTRL R0
SHIFTRR R1
INCR R0
COPYRA R0
XORLA 0xFF
ANDLA 0xF0
SUBLA 0x10
ORLA 0x02
CALL some_proc
ADDRA R1
XORRA R1
SUBRA R1
ORRA R1
INCRJZ R0
BCRSC zero_bit status_reg
DECRJZ R1
CBR zero_bit status_reg
COPYAR R1
COPYRR R1 R0
ADDRPC R0
HALT

:some_proc
    COPYLR 0x01 R1
    BCRSS zero_bit status_reg
    RETLA 0xF
    RETURN

%data R0 0
%data R1 0 0xFF 0xFF 0xFF 0xFF 0xFF
HALT