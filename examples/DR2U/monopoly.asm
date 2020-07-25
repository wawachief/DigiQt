// tarot contracter 


initsp	
speed	0 
bset	_sar _sr 
:start 
  randa	
  copyar	random 
  div	random six 
  bclr	_c _sr 
  addla	1 
  copylr	0 _ar 
  copyar	colorPtr1+1 
:colorPtr1 
  bset	0 _ar // first param is [colorPtr1+1] 

  randa	
  copyar	random 
  div	random six 
  bclr	_c _sr 
  addla	1 
  copylr	0 _dr 
  copyar	colorPtr2+1 
:colorPtr2 
  bset	0 _dr // first param is [colorPtr2+1] 

  randa	
  copyar	random 
  div	random six 
  bclr	_c _sr // remainder of 0 arms the carry bit and impact addition ! 
  addla	1 
  copyar	random 
  andla	4 
  btstsc	_z _sr 
  jump	de3 
// de 456 
  btstsc	1 random 
  jump	voiture 
  bset	0 _ar 
  jump	wait 

:voiture 
  bset	7 _ar 
  jump	wait 

:de3 
// random vaut 1, 2 ou 3, affichage a la fin de _dr 
  bclr	_c _sr 
  copyra	random 
  andla	1 
  addla	35 
  copyar	de3_1 // bclr = 35 bset = 36 
  shiftrr	random 
  bclr	_c _sr 
  copyra	random 
  andla	1 
  addla	35 
  copyar	de3_2 
:de3_1 
  bset	0 _dr // bset or bclr 

:de3_2 
  bset	7 _dr 

:wait 
// Wait for choice release to begin 
  copyra	_br 
  btstsc	_z _sr 
  jump	wait 

  jump	start 

%data random 0 
%data six 6 