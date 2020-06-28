%define status 252 
%define adrled 254 
%define dataled 255 
%define Zero 0 
%define Carry 1 
%define Adroff 2 

sbr	Adroff status 
// Initialize value to be the number to convert 
copyrr	number value 
copyrr	number+1 value+1 
// Initialize the stack pointer 
copylr	stack stackPtr 

:divide 
// Initialize the remainder to 0 
  copylr	0 mod10 
  copylr	0 mod10+1 
  cbr	Carry status 

  copylr	16 idx 
:divloop 
// Rotate quotient and remainder 
  copyrr	value dataled 
  copyrr	value+1 adrled 
  shiftrl	value 
  shiftrl	value+1 
  shiftrl	mod10 
  shiftrl	mod10+1 

// Acc, tmp = dividend - divisor 
  sbr	Carry status 
  copyra	mod10 
  subla	10 // BUG : CARRY should go to 0 ?? 
  copyar	tmp 
  copyra	mod10+1 
  subla	0 
  bcrss	Carry status 
  jump	ignore_result // branch if dividend < divisor 
  copyrr	tmp mod10 
  copyar	mod10+1 
:ignore_result 
  decrjz	idx 
  jump	divloop 
  shiftrl	value // shift in the last bit of the quotient 
  shiftrl	value+1 

  copyra	mod10 
  cbr	Carry status 
// push the remainder into the stack 
  copyai	stackPtr 
  incr	stackPtr 

// if value != 0, then continue dividing 
  copyra	value 
  orra	value+1 
  bcrss	Zero status 
  jump	divide // branch if value is not zero 

  call	stack_out 
  halt	
  jump	0 

:stack_out 
// pops out the stack into serial 
  decr	stackPtr 
  copyia	stackPtr 
  addla	'0' 
  comout	
// test if we reached the head of the stack 
  copyra	stackPtr 
  subla	stack 
  bcrss	Zero status 
  jump	stack_out 
  return	

%org 232 
%data value 0 0 // 2 bytes 
%data mod10 0 0 // 2 bytes 
%data number 0xc1 0x06 // 1729 little indian 
%data tmp 0 // temp register 
%data idx 0 
%data stack 0 0 0 0 0 0 
%data stackPtr 0 



