// PrimeSerial 
// Olivier Lecluse 
// Platform : Digirule2B

%define status 252 
%define dataLED 255 

%define ZFlag 0 
%define CFlag 1 
// we use bit 3 of status to store the prime state 
%define PFlag 3 

initsp	
speed	0 

// Variables initialisations 
copylr	0 status 
copylr	5 nb 

// start the search with 5 
:search_loop 
  call	prime_test 
  bcrsc	PFlag status 
  jump	nb_is_prime 
:increment_nb 
  incr	nb 
// if null, we reached 256 
  bcrsc	ZFlag status 
  jump	the_end 
// increment nb by 2 
  incr	nb 
  jump	search_loop 
:nb_is_prime 
  copyrr	nb dataLED 
// searching next prime 
  jump	increment_nb 
:the_end 
  halt	
  jump 0

// primality test 
// input : nb 
// ouput : PFlag on status 
:prime_test 
  cbr	CFlag status 
  copyrr	nb dv 
  shiftrr	dv 
// making sure dv is odd 
  sbr	0 dv 
:loop_div 
  copyrr	nb r0 
  div	r0 dv 
// r0 is the quotient, acc the remainder 
// CFlag is set if the remainder is 0 
  bcrsc	CFlag status 
  jump	not_prime 
// we stop when dv is 3 
  decr	dv 
  decr	dv 
  copyra	dv 
  subla	1 
  bcrss	ZFlag status 
  jump	loop_div 
// Number is prime 
  sbr	PFlag status 
  return	
:not_prime 
  cbr	PFlag status 
  return	



// General Registers 
%data dv 0 
%data ten 10 
%data r0 0 
%data nb 0 