%define _sr 252 
%define _ar 254 
%define _dr 255 
%define _sar 2 
%define _c 1 

%define byte2 254 
%define byte1 255 

sbr	_sar,_sr 
copylr	0, byte2 
copylr	0, byte1 

:loop 
  sbr	_c,_sr 

  copyra	byte0 
  subla	1 
  copyar	byte0 

  copyra	byte1 
  subla	0 
  copyar	byte1 

  copyra	byte2 
  subla	0 
  copyar	byte2 

  jump	loop 


%org 0xF0 
%data byte0 0 


