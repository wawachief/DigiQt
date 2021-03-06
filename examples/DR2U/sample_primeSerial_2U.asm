// PrimeSerial 
// Olivier Lecluse 
// Brent Hauser 
// Platform : Digirule2U 

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
copylr	init_str init_strPtr 

// Displays init_str 
:disp_initstr 
  copyia	init_strPtr 
  btstsc	ZFlag status 
  jump	search_loop 
  comout	
  incr	init_strPtr 
  jump	disp_initstr 

// start the search with 5 
:search_loop 
  call	prime_test 
  btstsc	PFlag status 
  jump	nb_is_prime 
:increment_nb 
  incr	nb 
// if null, we reached 256 
  btstsc	ZFlag status 
  jump	the_end 
// increment nb by 2 
  incr	nb 
  jump	search_loop 
:nb_is_prime 
  copyrr	nb dataLED 
// output result to serial 
  call	int_comout 
// Outputs a space separator 
  copyla	' ' 
  comout	
// searching next prime 
  jump	increment_nb 
:the_end 
// We reached 255 
  copyla	0x0d 
  comout	
  copyla	0x0a 
  comout	
  halt	
  jump 0

// primality test 
// input : nb 
// ouput : PFlag on status 
:prime_test 
  bclr	CFlag status 
  copyrr	nb dv 
  shiftrr	dv 
// making sure dv is odd 
  bset	0 dv 
:loop_div 
  copyrr	nb r0 
  div	r0 dv 
// r0 is the quotient, acc the remainder 
// CFlag is set if the remainder is 0 
  btstsc	CFlag status 
  jump	not_prime 
// we stop when dv is 3 
  decr	dv 
  decr	dv 
  copyra	dv 
  xorla	1 
  btstss	ZFlag status 
  jump	loop_div 
// Number is prime 
  bset	PFlag status 
  return	
:not_prime 
  bclr	PFlag status 
  return	


// converting binary to decimal 
// input : nb 
// outputs decimal representation of nb on serial 
:int_comout 
  copyrr	nb r0 
// Initialize the stack pointer 
  copylr	stack stackPtr 
:get_digits 
  div	r0 ten 
  copyai	stackPtr 
  incr	stackPtr 
  copyra	r0 
  btstss	ZFlag status 
  jump	get_digits 
// Outputs the content of the stack over USB 
:stack_out 
  decr	stackPtr 
  copyia	stackPtr 
  orla	'0' 
  comout	
// test if we reached the head of the stack 
  copyra	stackPtr 
  xorla	stack 
  btstss	ZFlag status 
  jump	stack_out 
  return	

// General Registers 
%data dv 0 
%data ten 10 
%data r0 0 
%data nb 0 
%data init_str "Prime list : 2 3 " 0 
%data init_strPtr 0 
// Stack initialized with NULL caracters 
%data stack 0 0 0 
%data stackPtr 0 

