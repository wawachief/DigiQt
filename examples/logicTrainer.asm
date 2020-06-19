// Guess which logic gate the rule chose 
// by experimenting around truth tables 
// 
// D0 : Input A / D1 : input B 
// Answer with buttons D7 -> D2 : 
// 
// D7 : AND -> 0 
// D6 : OR -> 1 
// D5 : XOR -> 2 
// D4 : NOR -> 3 
// D3 : NAND -> 4 
// D2 : XNOR -> 5 

%define sts_reg 252 
%define btn_reg 253 
%define add_reg 254 
%define dta_reg 255 
%define carry_f 1 
%define zero_f 0 
%define hide_a 2 

:start 
  sbr	hide_a sts_reg 
  randa	
  copyar	gate 
  div	gate six 
  copyar	gate // Random number beetween 0 and 5 
  addla	lookupLogic
  copyar	lookupPtr
  copyir	lookupPtr lookupPtr 
  // lookupPtr contains the address of the random logic function 
  
:mainloop 
  copyra	btn_reg 
  copyar	dta_reg 
  // Acc contains buttons - Indirect call to random gate
  calli	lookupPtr
  jump	mainloop 

:test_answer
  // search for an answer
  copyla	0
  bcrsc	7 r0
:ta_loop
  
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

%data lookupLogic and or xor nor nand xnor 
%data lookupPtr 0
%data buttons 0 0 0 0 0 0 0 0 
%data buttonsPtr 0 
%data buttonsTmp 0 
%data gate 0 
%data six 6 
%data r0 0 
