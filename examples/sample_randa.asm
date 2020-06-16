%define status_reg 252 
%define data_reg 255 
%define zero 0 
%define arleds 2 

:start 
  speed	0 
  initsp	
  sbr	arleds status_reg 

:loop 
  randa	
  copyar	data_reg 
  call	comdec 
  copyla	13 
  comout	
  copyla	10 
  comout	
  jump	loop 

  ; convert number in accumulator to decimal ASCII and transmit 

:comdec 
  copylr	stack sp 
  copyar	n 

:cd_1 
  div	n ten 
  copyai	sp 
  incr	sp 

  copyra	n 
  bcrss	zero status_reg 
  jump	cd_1 

:cd_2 
  decr	sp 
  copyia	sp 
  addla	'0' 
  comout	

  copyra	sp 
  subla	stack 
  bcrss	zero status_reg 
  jump	cd_2 

  return	


%data n 0 
%data sp 0 
%data stack 0 0 0 
%data ten 10 