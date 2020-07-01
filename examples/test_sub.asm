%define _sr 252 
%define _ar 254 
%define _dr 255 
%define _sar 2 
%define _c 1 

sbr	_sar,_sr 

sbr	_c,_sr 
copyla	20 
subla	10 
copyar	_dr 
copyrr	_sr,_ar 
:loop 
  jump	loop 
