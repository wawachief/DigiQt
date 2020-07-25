// PrimeSerial 
// Olivier Lecluse 
// Brent Hauser 
// Platform : Digirule2U 

%define _sr 252 
%define _dr 255 

%define _z 0 
%define _c 1 
// we use bit 3 of _sr to store the prime state 
%define _p 3 

initsp	
speed	0 

sbr	_sar _sr 
copylr	2 _ar 
// Variables initialisations 
copylr	0 _dr 
copylr	5 nb 

// Displays init_str 

// start the search with 5 
:search_loop 
  call	prime_test 
  bcrsc	_p _sr 
  jump	nb_is_prime 
:increment_nb 
  incr	nb 
// if null, we reached 256 
  bcrsc	_z _sr 
  jump	the_end 
// increment nb by 2 
  incr	nb 
  jump	search_loop 
:nb_is_prime 
  copyrr	nb _dr 
// output result to serial 
  call	int_out 
// Outputs a space separator 
// searching next prime 
  jump	increment_nb 
:the_end 
  jump	the_end
  jump 0 

// primality test 
// input : nb 
// ouput : _p on _sr 
:prime_test 
  cbr	_c _sr 
  copyrr	nb dv 
  shiftrr	dv 
// making sure dv is odd 
  sbr	0 dv 
:loop_div 
  copyrr	nb r0 
  div	r0 dv 
// r0 is the quotient, acc the remainder 
// _c is set if the remainder is 0 
  bcrsc	_c _sr 
  jump	not_prime 
// we stop when dv is 3 
  decr	dv 
  decr	dv 
  copyra	dv 
  xorla	1 
  bcrss	_z _sr 
  jump	loop_div 
// Number is prime 
  sbr	_p _sr 
  return	
:not_prime 
  cbr	_p _sr 
  return	


// converting binary to decimal 
// input : nb 
// outputs decimal representation of nb on serial 
:int_out 
  copyrr	nb _dr 
  incr	_ar 
  return	

// General Registers 
%data dv 0 
%data ten 10 
%data r0 0 
%data nb 0 
