// test I/O 

%define PIN0 0 
%define PIN1 1 
%define OUTPUT 0 
%define INPUT 1 
%define LOW 0 
%define HIGH 1 

speed	32 

pindir	PIN0 OUTPUT 
pindir	PIN1 INPUT 

:start 
  pinin	PIN1 
  bcrsc	_z _sr 
  jump	btn_pressed 

  pinout	PIN0 LOW 
  jump	start 
:btn_pressed 
  pinout	PIN0 HIGH 
  jump	start 
