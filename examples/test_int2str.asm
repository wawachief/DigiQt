%define 	ZFlag 0
%define 	statusReg 252

copylr	53 r0

//
// converting binary to decimal
//
// Initialize the stack pointer to the second element
copylr	stack stackPtr	
  
:get_digits                 
    div        r0 ten
    addla    '0'
    copyai    stackPtr
    incr    stackPtr
    copyra    r0
    bcrss    ZFlag statusReg
    jump    get_digits  
:the_end
    halt
    
// The END
// Result is in stack+4
// 


// stack variables
%data 	r0 0
%data 	ten 10
%data 	stackPtr 0
// Stack initialized with NULL caracters
%data 	stack 0 0 0 255
