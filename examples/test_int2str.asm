%define 	ZFlag 0
%define 	statusReg 252

copylr	51 r0

//
// converting binary to decimal
//

copylr	stack+1 stackPtr	    // Initialize the stack pointer to the second element
	    
:get_digits                 // When we pop a 0, this is the end !
    div	r0 ten		        // input : r0 is dividend, ten is divisor. Output : r0 is the quotient, acc is the remainder
    bcrsc	ZFlag statusReg	// Quotient is null, we stop pushing to the stack band make the string
    jump	to_str
    addla	'0'
    call	push		    // Push digit into the stack. '0' is not NULL !
    jump 	get_digits  
:to_str
    addla	'0'
    call	push		    // pushes the last digit into the stack
    // All the digits should be in the stack, 
    // now we stack them out into str
    copylr	str strPtr	    // Initialize the str pointer
    :loop			
        call 	pop
        bcrsc	ZFlag statusReg	// we pop a 0, the 
        halt	                // String is complete
        nop
        copyai 	strptr
        incr	strptr
        jump	loop
        
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
%data 	strPtr 0
%data 	stack 0 0 0 0		    // Stack initialized with NULL caracters
%data 	str "0  "

