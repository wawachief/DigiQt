// Olivier Lecluse 
// Logic Trainer for Digirule 2B - 2U 

// Guess which logic gate the rule chose 
// by experimenting around truth tables 
// 
// D0 : Input A / D1 : input B 
// Answer with buttons D7 -> D2 : 
// D7 : AND -> 0 
// D6 : OR -> 1 
// D5 : XOR -> 2 
// D4 : NAND -> 3 
// D3 : NOR -> 4 
// D2 : XNOR -> 5 

%define sts_reg 252 
%define btn_reg 253 
%define add_reg 254 
%define dta_reg 255 
%define carry_f 1 
%define zero_f 0 
%define hide_a 2 

// Init scores 
copylr	0 score 
copylr	0 score+1 

:start 
  sbr	hide_a sts_reg 
  randa	
  copyar	gate 
  div	gate six 
  copyar	gate // Random number beetween 0 and 5 
  // Careful, carry may be set by DIV !!
  cbr 	carry_f sts_reg
  addla	lookupLogic 
  copyar	lookupPtr 
// lookupPtr contains the address of the random logic function 
  copyir	lookupPtr lookupPtr 
// Button configuration for the answer 
  copylr	0b10000000 buttonsGate 
  copyrr	gate r0 
:s_loop 
  bcrsc	zero_f sts_reg 
  jump	mainloop 
  shiftrr	buttonsGate 
  decr	r0 
  jump	s_loop 
:mainloop 
  copyra	btn_reg 
  copyar	dta_reg 
// Acc contains buttons - Indirect call to random gate 
  calli	lookupPtr 
  call	test_answer 
  bcrsc	zero_f sts_reg // zero_f set -> no answer yet 
  jump	mainloop 
  jump	start 

:test_answer 
// search for an answer 
// Ignore Gate inputs 
  copyra	btn_reg 
  andla	0b11111100 // zero_f -> no answer yet 
  bcrsc	zero_f sts_reg 
  return	
  nop	
// An answer button is pressed 
// Check the answer 
  subra	buttonsGate 
  bcrsc	zero_f sts_reg 
  jump	you_win 
:you_lose 
  incr	score // # games 
  copylr	0 dta_reg 
  jump	wait 
:you_win 
  incr	score // # games 
  incr	score+1 // # wins 
  copylr	255 dta_reg 
  jump	wait 
:wait 
  cbr	carry_f sts_reg 
  copyrr	score buttonsTmp 
  shiftrl	buttonsTmp 
  shiftrl	buttonsTmp 
  shiftrl	buttonsTmp 
  shiftrl	buttonsTmp 
  copyra	buttonsTmp 
  orra	score+1 
  copyar	add_reg 
  copylr	255 r0 
  speed	8 
:w_loop 
// Add some delay by doing n times the same operation 
  decrjz	r0 
  jump	w_loop 
  speed	0 
  cbr	zero_f sts_reg // zero_f clear -> new game 
  return	

// check the answer 

// Logic operations Results 
:logic_0 
  copylr	0 add_reg 
  return	
:logic_1 
  copylr	1 add_reg 
  return	

// Logic operations 
:and 
  andla	0b00000011 
  subla	0b00000011 
  bcrss	zero_f sts_reg 
  jump	logic_0 
  jump	logic_1 

:or 
  andla	0b00000011 
  bcrss	zero_f sts_reg 
  jump	logic_1 
  jump	logic_0 

:xor 
  andla	0b00000011 
  bcrsc	zero_f sts_reg 
  jump	logic_0 
  subla	0b00000011 
  bcrsc	zero_f sts_reg 
  jump	logic_0 
  jump	logic_1 

:nor 
  andla	0b00000011 
  bcrss	zero_f sts_reg 
  jump	logic_0 
  jump	logic_1 

:nand 
  andla	0b00000011 
  subla	0b00000011 
  bcrss	zero_f sts_reg 
  jump	logic_1 
  jump	logic_0 

:xnor 
  andla	0b00000011 
  bcrsc	zero_f sts_reg 
  jump	logic_1 
  subla	0b00000011 
  bcrsc	zero_f sts_reg 
  jump	logic_1 
  jump	logic_0 

%data lookupLogic and or xor nand nor xnor 
%data lookupPtr 0 
%data buttonsTmp 0 
%data buttonsGate 0 
%data gate 0 
%data six 6 
%data score 0 0 // # of games - # of wins 
%data r0 0 
