// Olivier Lecluse 
// Logic Trainer for Digirule 2B - 2U 

// Guess which logic gate is applied to A and B 
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

initsp	
// Init scores 
copylr	0 score 
copylr	0 score+1 

:start 
  bset	_sar, _sr 
  randa	
  copyar	gate 
  div	gate, six 
  copyar	gate // Random number beetween 0 and 5 
// Careful, carry may be set by DIV !! 
  bclr	_c, _sr 
  addla	lookupLogic 
  copyar	lookupPtr 
// lookupPtr contains the address of the random logic function 
  copyir	lookupPtr, lookupPtr 
// Button configuration for the answer 
  copylr	0b10000000, buttonsGate 
  copyrr	gate, r0 
:s_loop 
  btstsc	_z, _sr 
  jump	mainloop 
  shiftrr	buttonsGate 
  decr	r0 
  jump	s_loop 
:mainloop 
  copyra	_br 
  copyar	_dr 
// Acc contains buttons - Indirect call to random gate 
  calli	lookupPtr 
  call	test_answer 
  btstsc	_z, _sr // _z set -> no answer yet 
  jump	mainloop 
  jump	start 

:test_answer 
// search for an answer 
// Ignore Gate inputs 
  copyra	_br 
  andla	0b11111100 // _z -> no answer yet 
  btstsc	_z, _sr 
  return	
  nop	
// An answer button is pressed 
// Check the answer 
  xorra	buttonsGate 
  btstsc	_z, _sr 
  jump	you_win 
:you_lose 
  incr	score // # games 
  copylr	0, _dr 
  jump	wait 
:you_win 
  incr	score // # games 
  incr	score+1 // # wins 
  copylr	255, _dr 
  jump	wait 
:wait 
  bclr	_c, _sr 
  copyrr	score, buttonsTmp 
  shiftrl	buttonsTmp 
  shiftrl	buttonsTmp 
  shiftrl	buttonsTmp 
  shiftrl	buttonsTmp 
  copyra	buttonsTmp 
  orra	score+1 
  copyar	_ar 
  copylr	255, r0 
  speed	8 
:w_loop 
// Add some delay by doing n times the same operation 
  decrjz	r0 
  jump	w_loop 
  speed	0 
  bclr	_z, _sr // _z clear -> new game 
  return	

// check the answer 

// Logic operations Results 
:logic_0 
  copylr	0, _ar 
  return	
:logic_1 
  copylr	1, _ar 
  return	

// Logic operations 
:and 
  andla	0b00000011 
  xorla	0b00000011 
  btstss	_z, _sr 
  jump	logic_0 
  jump	logic_1 

:or 
  andla	0b00000011 
  btstss	_z, _sr 
  jump	logic_1 
  jump	logic_0 

:xor 
  andla	0b00000011 
  btstsc	_z, _sr 
  jump	logic_0 
  xorla	0b00000011 
  btstsc	_z, _sr 
  jump	logic_0 
  jump	logic_1 

:nor 
  andla	0b00000011 
  btstss	_z, _sr 
  jump	logic_0 
  jump	logic_1 

:nand 
  andla	0b00000011 
  xorla	0b00000011 
  btstss	_z, _sr 
  jump	logic_1 
  jump	logic_0 

:xnor 
  andla	0b00000011 
  btstsc	_z, _sr 
  jump	logic_1 
  xorla	0b00000011 
  btstsc	_z, _sr 
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