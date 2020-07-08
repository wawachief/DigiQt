// tarot contracter 


initsp	
speed 0
sbr	_sar _sr 
:start 
  randa	
  copyar	random 
  div	random quatre 
  copylr	0 _ar
  copyar colorPtr1+1
:colorPtr1 
  sbr 0 _ar // first param is [colorPtr1+1]

  randa	
  copyar	random 
  div	random trois 
  copylr	0 _dr
  copyar colorPtr2+1
:colorPtr2
  sbr 0 _dr // first param is [colorPtr1+1]

:wait
// Wait for choice release to begin 
  copyra	_br 
  bcrsc	_z _sr 
  jump	wait 

  jump	start 

%data random 0 
%data quatre 4 
%data trois 3 