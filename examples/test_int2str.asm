%define 	ZFlag 0
%define 	statusReg 252

copylr	153 r0

//
// converting binary to decimal
//
  // Initialize the stack pointer to the second element
copylr	stack+1 stackPtr	
  

// Optimized version
:get_digits                 
    div    	r0 ten
    addla	'0'
    incr	stackPtr
    copyai	stackPtr
    copyra	r0
    bcrss	ZFlag statusReg
    jump	get_digits  
:serial_out
    halt
    

// The END
// Result is in stack+1
// 

//
// Implementing stack
//

// pushes accumulator into the stack
:push
    copyai	stackPtr
    incr	stackPtr
    return
// pops a number out of the stack into the acc
:pop
    decr	stackPtr
    copyia	stackPtr
    return

// stack variables
%data 	r0 0
%data 	ten 10
%data 	stackPtr 0
// Stack initialized with NULL caracters
%data 	stack 0 0 0 0
