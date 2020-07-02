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

initsp
:start 
  speed	0 
  sbr	_sar, _sr 

// initialize game 

  randa	
// copyla 0xAA // This is cheating 
  copyar	nb2guess 
  copyrr	nb2guess, _dr // prints number to guess on dataLEDs 
  copylr	0, nbplayer // user guess 
  call	init_timer // time limit 

:guess_nb 
// Wait for user input 
  comrdy	
  bcrss	_z, _sr 
  jump	read_nb 
  call	tick_timer 
  bcrsc	_c, _sr 
  jump	you_loose 
  jump	guess_nb 
:read_nb 
// a character is available 
  comin	
  comout	// echo on console 
  copyar	char 
  xorla	13 
  bcrsc	_z, _sr 
// End of input on Enter key 
  jump	input_end 
  copyra	char 
// to upper case 
  cbr	_c, _sr // XX Set Carry for "normal" substraction
  subla	'a' 
  bcrss	_c, _sr // XX
  subla	32 // ord('a') - ord('A') = 32
  addla	96 // XX C is set 'a' is 97 
// letter is uppercase 
// test if digit or letter 
  cbr	_c, _sr // XX
  subla	'A' 
  bcrss	_c _sr // XX
  subla	7 // A -> '0' + 10
  addla	64 // XX C is set 'A' is 65 
  subla	47 // XX C is set. '0' is 48.
  
  // user input (0-15) is in accumulator 
  mul	nbplayer, BASE 
  addra	nbplayer 
  copyar	nbplayer 
  jump	guess_nb 
:input_end 
  copylr	0, _sr 
  copyra	nb2guess 
  xorra	nbplayer 
  bcrsc	_z, _sr 
  jump	you_win 
  jump	you_loose 

:you_win 
  copylr	0xff, _dr 
  copylr	win_str, strPtr 
  call	print_message 
  call	wait_for_space 
  jump	start 
:you_loose 
  copylr	0 _dr 
  copylr	lose_str, strPtr 
  call	print_message 
  call	wait_for_space 
  jump	start 

// Displays message string 
:print_message 
  copyia	strPtr 
  bcrsc	_z, _sr 
  return	
  nop	
  comout	
  incr	strPtr 
  jump	print_message 

:wait_for_space 
  copylr	space_str, strPtr 
  call	print_message 
  comin	
  xorla	' ' 
  bcrss	_z, _sr 
  jump	wait_for_space 
  return	

:init_timer 
// Initialize timer 
  copylr	0, counter 
  copyrr	COUNT_SPEED, cs 
  copylr	0xFF, cs+1 
  copylr	0, _ar 
  cbr	_c, _sr 
  return	
:tick_timer 
// Non blocking timer 
  decrjz	cs+1 
  return	
  nop	
  copylr	0xFF, cs+1 
  decrjz	cs 
  return	
  nop	
  copyrr	COUNT_SPEED, cs 
// displays a progress bar on ADDR leds 
  cbr	_c, _sr 
  shiftrl	counter 
  incr	counter 
  copyrr	counter, _ar 
// The Carry is Set in case of TimeOut 
  return	

// Variables declaration 

%data cs 0 0 
%data counter 0 
%data nb2guess 0 
%data char 0 
%data nbplayer 0 
%data strPtr 0 
%data win_str 13 10 "You win," 0 
%data lose_str 13 10 "You lose," 0 
%data space_str " hit SPACE to restart" 13 10 

%org 248 
%data COUNT_SPEED 20 
%data BASE 16 
