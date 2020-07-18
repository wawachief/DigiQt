// test I/O 

%define PIN0 0 
%define PIN1 1 
%define OUTPUT 0 
%define INPUT 1 
%define LOW 0 
%define HIGH 1 

speed	0 

pindir	PIN0 OUTPUT 
pindir	PIN1 OUTPUT 

:start 
  pinout	PIN0 HIGH 
  pinout	PIN0 LOW 
  jump	start 