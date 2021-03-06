bset	_sar,_sr 

// test subla function

// test1 : C=0 0-1 C=1
copylr	1, _ar 

bclr	_c,_sr 
copyla	0 
subla	1 

xorla	0xff
btstss	_z, _sr 
jump	error1 

btstss	_c, _sr // C = 1
jump	error2 


// test2 : C=1 0-1 C=1
copylr	2, _ar 

bset	_c,_sr 
copyla	0
subla	1

xorla	0xfe
btstss	_z, _sr 
jump	error1 

btstss	_c, _sr // C = 1
jump	error2 


// test3 : C=0 FF-1 C=0
copylr	4, _ar 

bclr	_c,_sr 
copyla	1
subla	1 

xorla	0x0
btstss	_z, _sr 
jump	error1 

btstsc	_c, _sr // C = 0
jump	error2 


// test4 : C=1 1-1 C=1
copylr	8, _ar 

bset	_c,_sr 
copyla	1
subla	1

xorla	0xff
btstss	_z, _sr 
jump	error1 

btstss	_c, _sr // C = 1
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