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


%define PIN0 0 
%define PIN1 1 
%define OUTPUT 0 
%define INPUT 1 
%define LOW 0 
%define HIGH 1 

%define _r 3 // rising edge detection 
%define _m 4 // mode : 0 = idle, 1 = dial 

initsp	
copylr	0b00000100 _sr 

// set IO pin direction 
pindir	PIN0 INPUT // state. LOW = dial is activated 
pindir	PIN1 INPUT // impulsions 

:start 
  speed	0 
  bset	_sar, _sr 

// initialize game 

  randa	
  //copyla	0xAA // This is cheating 
  copyar	nb2guess 
  copyrr	nb2guess, _dr // prints number to guess on dataLEDs 
  copylr	0, nbplayer // user guess 
  call	init_timer // time limit 

:loop 

// Countdown timer 
  call	tick_timer 
  btstsc	_c, _sr 
  jump	you_loose 
// test input dial 
  btstss	_m _sr 
  jump	process_idle 
  jump	process_dial 

:process_idle 
  pinin	PIN0 
  btstss	_z _sr // ZF set = dial is activated 
  jump	loop 
// enter dial mode 
  copylr	0 number 
  bset	_m _sr 
  bclr	_r _sr // initialize the rising edge detection 
  jump	loop 

:process_dial 
// detect impulsion 
  pinin	PIN1 
  btstss	_z _sr // ZF set = no impulsion 
  jump	process_impuls 

  bclr	_r _sr 
  pinin	PIN0 
  btstsc	_z _sr // ZF clear = back to idle mode 
  jump	loop 
// exit dial mode 
  bclr	_m _sr 
// 10 is 0 so we take mod 10 
  div	number BASE 
// user input (0-15) is in accumulator 
  mul	nbplayer, BASE 
  addra	nbplayer 
  copyar	nbplayer 
  jump	input_end 

:process_impuls 
  btstsc	_r _sr // _r clear => we have a rising edge 
  jump	loop // _r set ==> nothing new 

// we have a rising edge 
  bset	_r _sr 
  incr	number // increment impulsion counter 
  jump	loop 

:input_end 
  //copyrr	nbplayer _ar 
  copyra	nb2guess 
  xorra	nbplayer 
  btstsc	_z, _sr 
  jump	you_win 
  jump	loop 

:you_win 
  copylr	0xff, _dr 
  call	wait_for_btn 
  jump	start 
:you_loose 
  copylr	0 _dr 
  call	wait_for_btn 
  jump	start 


:wait_for_btn 
  copyra	_br 
  btstsc	_z, _sr // ZF clear ==> btn pressed 
  jump	wait_for_btn 
  return	

:init_timer 
// Initialize timer 
  copylr	0, counter 
  copyrr	COUNT_SPEED, cs 
  copylr	0xFF, cs+1 
  copylr	0, _ar 
  bclr	_c, _sr 
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
  bclr	_c, _sr 
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
%data number 0 

%org 248 
%data COUNT_SPEED 40 
%data BASE 10 
