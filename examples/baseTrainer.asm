%define statusReg 252 
%define buttonReg 253 
%define addrLEDReg 254 
%define dataLEDReg 255 
%define ZFlag 0 
%define CFlag 1 
%define AFlag 2 

// Constants 
%define COUNT_SPEED 20

:start
  initsp	
  speed	0 
  sbr	AFlag statusReg 


randa	
copyar	nb2guess 

// to_hex trainner 
:to_hex 
  copyrr	nb2guess dataLEDReg 	// number to guess
  copylr	0 input_nb		// user guess
  copylr	base 0x10			// 16 base
  call	begin_timer 		// time limit
:guess_hex 
  comrdy	
  bcrss	ZFlag statusReg 
  jump	read_hex 
  call	time_count 
  jump	guess_hex 
:read_hex 
// a character is available 
  comin	
  copyar	input_char
  subla	13
  bcrsc	ZFlag statusReg
  // End of input on Enter key
  jump	hexinput_end
  copyra	input_char
// to upper case
  cbr	CFlag statusReg
  subla	'a'
  bcrss	CFlag statusReg
  subla	32 // ord('a') - ord('A')
  addla	'a'
// letter is uppercase
// test if digit or letter
  cbr	CFlag statusReg
  subla	'A'
  bcrss	CFlag statusReg
  subla	7 // A -> '0' + 10
  addla	'A'
  subla 	'0'			// user input (0-15) is in accumulator
  mul	input_nb base
  addra	input_nb
  copyar	input_nb
  jump	guess_hex 
:hexinput_end
  call 	int_comout
  copyla 	' '
  comout
  copyla 	nb2guess
  call 	int_comout
  cbr	ZFlag statusReg
  copyra	nb2guess
  subra	input_nb
  bcrss	ZFlag statusReg
  jump	you_win
  jump	you_loose

:you_win
  copylr	0xff dataLEDReg
  call begin_timer
  jump start
:you_loose
  copylr 	0 dataLEDReg
  call begin_timer
  jump start


:begin_timer 
// Initialize timer
  copylr	0 counter 
  copylr	COUNT_SPEED cs 
  copylr	0xFF cs+1 
  copylr	0 addrLEDReg 
  return	
:time_count 
// Non blocking timer
  decrjz	cs+1 
  return	
  nop	
  copylr	0xFF cs+1 
  decrjz	cs 
  return	
  nop	
  copylr	COUNT_SPEED cs 
:progress_bar 
// displays a progress bar on ADDR leds 
  cbr	CFlag statusReg
  shiftrl	counter 
  bcrsc	CFlag statusReg 
  jump	you_loose 		// Time out
  incr	counter 
  copyrr	counter addrLEDReg 
  return

// DEBUG 
// outputs decimal representation of ACC on serial 
:int_comout 
  copyar	r0 
// Initialize the stack pointer 
  copylr	stack stackPtr 
:get_digits 
  div	r0 ten 
  copyai	stackPtr 
  incr	stackPtr 
  copyra	r0 
  bcrss	ZFlag statusReg 
  jump	get_digits 
// Outputs the content of the stack over USB 
:stack_out 
  decr	stackPtr 
  copyia	stackPtr 
  addla	'0' 
  comout	
// test if we reached the head of the stack 
  copyra	stackPtr 
  subla	stack 
  bcrss	ZFlag statusReg 
  jump	stack_out 
  return	


%data cs 0 0 
%data counter 0 
%data nb2guess 0 
%data input_char 0
%data input_nb 0

%data ten 10 
%data base 0
%data r0 0 
%data stack 0 0 0 
%data stackPtr 0 



