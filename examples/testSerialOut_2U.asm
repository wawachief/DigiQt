%define statusReg 252
%define ZFlag     0

copylr 0 count
:loop
    copyra count
    comout 
    incr count
    btstss ZFlag statusReg
    jump loop 
    halt
%data count 0