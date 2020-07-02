// Olivier Lecluse 
// Designed for Digirule 2U 
// Ceasar crypting 

initsp	
speed	0 

:read_char 
// Wait for user input 
  comrdy	
  bcrsc	_z, _sr 
  jump	read_char 

// a character is available 

  comin	

// to upper case 
  cbr	_c, _sr 
  subla	'a' 
  bcrss	_c, _sr 
  subla	32 // ord('a') - ord('A') 
  addla	96 
// dont crypt non alpha characters 
  cbr	_c, _sr 
  subla	'A' 
  bcrsc	_c, _sr 
  jump	print 

// crypt the char 
  call	crypt 
:print 
  cbr	_c, _sr 
  addla	'A' 
  comout	
  jump	read_char 

:crypt 
  cbr	_c, _sr 
  addra	offset 
  copylr	26, c_26 
  copyar	r0 
  div	r0, c_26 
// acc contains r0 mod 26 
  return	
:the_end 

%data r0 0 
%data c_26 0 
%data char 0 
%org 248 
%data offset 25 