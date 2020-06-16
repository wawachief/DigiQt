// Binary Conversion Trainer 
// Olivier Lecluse 
// Designed for Digirule 2U 

// 
// connect a terminal to the DR 
// Run the program 
// the DR displkays a number on row data row 
// Convert it to hexadecimal 
// and press Return 
// speed is at address 248 
// base is at address 249 

%define statusReg 252 
%define buttonReg 253 
%define addrLEDReg 254 
%define dataLEDReg 255 
%define ZFlag 0 
%define CFlag 1 
%define AFlag 2 

:start 
  initsp	
  speed	0 
  sbr	AFlag statusReg 

// initialize game 

  randa	
// copyla 0xAA // This is cheating 
  copyar	nb2guess 
  copyrr	nb2guess dataLEDReg // prints number to guess on dataLEDs 
  copylr	0 nbplayer // user guess 
  call	init_timer // time limit 

:guess_nb 
// Wait for user input 
  comrdy	
  bcrss	ZFlag statusReg 
  jump	read_nb 
  call	tick_timer 
  bcrsc	CFlag statusReg 
  jump	you_loose 
  jump	guess_nb 
:read_nb 
// a character is available 
  comin	
  comout	// echo on console 
  copyar	char 
  subla	13 
  bcrsc	ZFlag statusReg 
// End of input on Enter key 
  jump	input_end 
  copyra	char 
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
  subla	'0' // user input (0-15) is in accumulator 
  mul	nbplayer BASE 
  addra	nbplayer 
  copyar	nbplayer 
  jump	guess_nb 
:input_end 
  cbr	ZFlag statusReg 
  copyra	nb2guess 
  subra	nbplayer 
  bcrsc	ZFlag statusReg 
  jump	you_win 
  jump	you_loose 

:you_win 
  copylr	0xff dataLEDReg 
  copylr	win_str strPtr 
  call	print_message 
  call	wait_for_space 
  jump	start 
:you_loose 
  copylr	0 dataLEDReg 
  copylr	lose_str strPtr 
  call	print_message 
  call	wait_for_space 
  jump	start 

// Displays message string 
:print_message 
  copyia	strPtr 
  bcrsc	ZFlag statusReg 
  return	
  nop	
  comout	
  incr	strPtr 
  jump	print_message 

:wait_for_space 
  copylr	space_str strPtr 
  call	print_message 
  comin	
  subla	' ' 
  bcrss	ZFlag statusReg 
  jump	wait_for_space 
  return	

:init_timer 
// Initialize timer 
  copylr	0 counter 
  copyrr	COUNT_SPEED cs 
  copylr	0xFF cs+1 
  copylr	0 addrLEDReg 
  cbr	CFlag statusReg 
  return	
:tick_timer 
// Non blocking timer 
  decrjz	cs+1 
  return	
  nop	
  copylr	0xFF cs+1 
  decrjz	cs 
  return	
  nop	
  copyrr	COUNT_SPEED cs 
// displays a progress bar on ADDR leds 
  cbr	CFlag statusReg 
  shiftrl	counter 
  incr	counter 
  copyrr	counter addrLEDReg 
// The Carry is Set in case of TimeOut 
  return	

// Variables declaration 

%data cs 0 0 
%data counter 0 
%data nb2guess 0 
%data char 0 
%data nbplayer 0 
%data strPtr 0 
%data win_str 13 10 "You win!" 0 
%data lose_str 13 10 "You lose!" 0 
%data space_str " press SPACE to restart" 13 10 

%org 248
%data COUNT_SPEED 20 
%data BASE 16 