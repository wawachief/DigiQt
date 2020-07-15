%define _sr 252 
%define _sar 2 
%define _c 1 
%define byte2 254 
%define byte1 255 

bset	_sar,_sr 
copylr	0, byte1 
copylr	0, byte2 
:loop 

  copyra	byte0 
  addla	1 
  copyar	byte0 

  copyra	byte1 
  addla	0 
  copyar	byte1 

  copyra	byte2 
  addla	0 
  copyar	byte2 

  jump	loop 


%org 0xF0 
%data byte0 0 
