// PrimeSerial
// Olivier Lecluse
// Platform : Digirule2U

%define	status	252
%define	dataLED	255
%define	pi	248

%define	ZFlag	0
%define	CFlag	1
// we use bit 3 of status to store the prime state
%define	PFlag	3

initsp
speed	0

// Displays 002 and 003
copylr	2 nb
call	disp_nb
copylr	3 nb
call	disp_nb			

// star the search with 5 
copylr 	5 nb
:primeloop
    call	prime_test
    bcrsc	PFlag status_reg
    jump	isprime
:pl1
    cbr	ZFlag status_reg
    incr	nb 
    bcrsc	ZFlag status_reg
    jump	the_end			 // End on game : nb > 255
    incr	nb
    jump	primeloop
:isprime
    copyrr	nb dataLED_reg
    // output result to serial
    call	disp_nb
    // searching next prime 
    incr	pi
    jump	pl1
:the_end
    halt

// primality test
// input : nb
// ouput : PFlag on status
:prime_test
    copyrr	nb dv
:loopdiv
    decr	dv
    decr	dv
    copyrr	nb r0 			
    div	r0 dv
    // r0 is the quotient, acc the remainder
    // CFlag is set if the remainder is 0
    bcrsc	CFlag status_reg
    jump	not_prime
    copyra	dv
    subla	3
    bcrss	ZFlag status_reg
    jump	loopdiv
// Number is prime
    sbr	PFlag status_reg
    return
:not_prime
    cbr	PFlag status_reg
    return

// outputs nb on the serial port


//
// converting binary to decimal
//
:int2str
    copyrr	nb r0
    copylr	stack stackPtr	
    :get_digits                 
        div	r0 ten
        addla	'0'
        copyai	stackPtr
        incr	stackPtr
        copyra	r0
        bcrss	ZFlag statusReg
        jump	get_digits
// Outputs the content of the stack over USB
:disp_nb
    copylr	3 r0
    :loop_out
        decr	stackPtr
        copyia	stackPtr
        bcrss	ZFlag status
        comout
        nop
        decrjz	r0
        jump loop_out
    return

// General Registers
%data 	r0 0
%data	nb 0
%data 	dv 0
%data 	t0 0

%data 	ten 10
%data 	stackPtr 0
// Stack initialized with NULL caracters
%data 	stack 0 0 0
