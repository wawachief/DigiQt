// tarot contracter 


initsp	
speed	0 
bset	_sar _sr 
:start 
  randa	
  copyar	random 
  div	random quatre 
  copylr	0 _ar 
  copyar	colorPtr1+1 
:colorPtr1 
  bset	0 _ar // first param is [colorPtr1+1] 

  randa	
  copyar	random 
  div	random trois 
  copylr	0 _dr 
  copyar	colorPtr2+1 
:colorPtr2 
  bset	0 _dr // first param is [colorPtr2+1] 

  randa	
  copyar	random 
  div	random cinq 
  bclr	_c _sr // remainder of 0 arms the carry bit and impact addition !
  addla	3 
  copyar	colorPtr3+1 
:colorPtr3 
  bset	0 _dr // first param is [colorPtr3+1] 

:wait 
// Wait for choice release to begin 
  copyra	_br 
  btstsc	_z _sr 
  jump	wait 

  jump	start 

%data random 0 
%data quatre 4 
%data cinq 5 
%data trois 3 