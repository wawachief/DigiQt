%define 	ZFlag 0
%define 	statusReg 252

copylr	153 r0

//
// converting binary to decimal
//
  // Initialize the stack pointer to the second element
copylr	stack+1 stackPtr	
  
// When we pop a 0, this is the end !
:get_digits                 
    // input : r0 is dividend, ten is divisor. Output : r0 is the quotient, acc is the remainder
    div	r0 ten		        
    bcrsc	ZFlag statusReg
    // Quotient is null, we stop pushing to the stack and quit
    jump	the_end
    addla	'0'
    // Push digit into the stack. '0' is not NULL !
    call	push		    
    jump 	get_digits  
:the_end
    addla	'0'
    call	push		    // pushes the last digit into the stack
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
