// Olivier Lecluse 
// Designed for Digirule 2U 
// Ceasar crypting

%define status_reg 252 
%define button_reg 253 
%define addrLED_reg 254 
%define dataLED_reg 255 
%define ZFlag 0 
%define CFlag 1 

initsp	
speed	0 

:read_char 
// Wait for user input 
  comrdy	
  bcrsc	ZFlag status_reg 
  jump	read_char 

// a character is available 

  comin	

// to upper case 
  cbr	CFlag status_reg 
  subla	'a' 
  bcrss	CFlag status_reg 
  subla	32 // ord('a') - ord('A') 
  addla	'a' 
// dont crypt non alpha characters 
  cbr	CFlag status_reg 
  subla	'A' 
  bcrsc	CFlag status_reg 
  jump	print 

// crypt the char 
  call	crypt 
:print 
  addla	'A' 
  comout	
  jump	read_char 

:crypt 
  addra	offset 
  copylr	26 c_26 
  copyar	r0 
  div	r0 c_26 
  // acc contains r0 mod 26
  return	
:the_end 

%data r0 0 
%data c_26 0 
%data char 0 
%org 248 
%data offset 1 