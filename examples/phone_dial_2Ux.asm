// test I/O 

%define PIN0 0 
%define PIN1 1 
%define OUTPUT 0 
%define INPUT 1 
%define LOW 0 
%define HIGH 1 

%define _r 3 // rising edge detection 
%define _m 4 // mode : 0 = idle, 1 = dial 

initsp	
copylr	0b00000100 _sr

// set IO pin direction 
pindir	PIN0 INPUT  // state. LOW = dial is activated
pindir	PIN1 INPUT  // impulsions

//mainloop
:loop
   btstss _m _sr
   jump process_idle
   jump process_dial

:process_idle
  pinin PIN0
  btstss _z _sr // ZF set = dial is activated
  jump loop
  // enter dial mode
  copylr 0 number
  copylr 0b10000000 _ar
  bset _m _sr
  bclr _r _sr // initialize the rising edge detection
  jump loop

:process_dial
  // detect impulsion
  pinin PIN1
  btstss _z _sr // ZF set = no impulsion
  jump process_impuls
  
  bclr _r _sr
  bclr 0 _ar
  pinin PIN0
  btstsc _z _sr // ZF clear = back to idle mode
  jump loop
  // exit dial mode
  copylr 0b00000000 _ar
  bclr _m _sr
  copyrr number _dr // we display the number
  jump loop

:process_impuls
  btstsc _r _sr // _r clear => we have a rising edge
  jump loop // _r set ==> nothing new
  
  // we have a rising edge
  bset _r _sr 
  bset 0 _ar // turn on A0
  incr number // increment impulsion counter
  jump loop
  
%data number 0