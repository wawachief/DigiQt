sbr	_sar,_sr 

// test subla function

// test1 : C=0 20+10=30 C=0 
copylr	1, _ar 

cbr	_c,_sr 
copyla	20 
addla	10 

xorla	30 // 20+10 = 30
bcrss	_z, _sr 
jump	error1 

bcrsc	_c, _sr // C = 0 
jump	error2 


// test2 : C=1 20+10=31 C=0 
copylr	2, _ar 

sbr	_c,_sr 
copyla	20 
addla	10 

xorla	30 // 20+10 = 31 
bcrss	_z, _sr 
jump	error1 

bcrsc	_c, _sr // C = 0 
jump	error2 

// test3 : C=0 250+10=4 C=1
copylr	4, _ar 

cbr	_c,_sr 
copyla	250 
addla	10

xorla	4 // 250+10=4 
bcrss	_z, _sr 
jump	error1 

bcrss	_c, _sr // C = 1
jump	error2 


// test4 : C=1 250+10=5 C=1
copylr	8, _ar 

sbr	_c,_sr 
copyla	250 
addla	10

xorla	4 // 250+10=5
bcrss	_z, _sr 
jump	error1 

bcrss	_c, _sr // C = 1
jump	error2 


// Test subra function

copylr	20, a
copylr	10, b

// test5 : C=0 20+10=30 C=0 
copylr	16, _ar 

cbr	_c,_sr 
copyra	a 
addra	b 

xorla	30 // 20+10=30
bcrss	_z, _sr 
jump	error1 

bcrsc	_c, _sr // C = 0 
jump	error2 

// test6 : C=1 20+10=31 C=0 
copylr	32, _ar 

sbr	_c,_sr 
copyra	a 
addra	b 

xorla	30 // 20+10=31
bcrss	_z, _sr 
jump	error1 

bcrsc	_c, _sr // C = 0 
jump	error2 

copylr	250, a
copylr	10, b

// test7 : C=0 250+10=4 C=1
copylr	64, _ar 

cbr	_c,_sr 
copyra	a 
addra	b 

xorla	4 // 250+10=4
bcrss	_z, _sr 
jump	error1 

bcrss	_c, _sr // C = 1
jump	error2 


// test8 : C=1 250+10=5 C=1
copylr	128, _ar 

sbr	_c,_sr 
copyra	a 
addra	b 

xorla	4 // 250+10=5
bcrss	_z, _sr 
jump	error1 

bcrss	_c, _sr // C = 1
jump	error2 

:OK 
  copylr	255, _dr 
  jump	end 

:error1 // error on result 
  copylr	170, _dr 
  jump	end 

:error2 // error on carry 
  copylr	85, _dr 
  jump	end 

:end 
  jump	end 

%data a 0
%data b 0