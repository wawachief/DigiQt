// PrimeSerial
// Olivier Lecluse
// Platform : Digirule2U

%define	status	252
%define	dataLED	255

%define	ZFlag	0
%define	CFlag	1
// we use bit 3 of status to store the prime state
%define	PFlag	3

initsp
speed	0

// Displays 2 and 3
copylr	2 nb
call	int2str
copylr	3 nb
call	int2str

// start the search with 5 
copylr 	5 nb
:search_loop
    call	prime_test
    bcrsc	PFlag status
    jump	nb_is_prime
    :increment_nb
        incr	nb 
// if null, we reached 256
        bcrsc	ZFlag status
        jump	the_end
// increment nb by 2
        incr	nb
        jump	search_loop
    :nb_is_prime
        copyrr	nb dataLED
// output result to serial
        call	int2str
// searching next prime
        jump	increment_nb
    :the_end
// We reached 255
        copyla	'\n'
        comout
        halt

// primality test
// input : nb
// ouput : PFlag on status
:prime_test
    copyrr	nb dv
:loop_div
    decr	dv
    decr	dv
    copyrr	nb r0 			
    div	r0 dv
    // r0 is the quotient, acc the remainder
    // CFlag is set if the remainder is 0
    bcrsc	CFlag status
    jump	not_prime
// we stop when dv is 3
    copyra	dv
    subla	3
    bcrss	ZFlag status
    jump	loop_div
// Number is prime
    sbr	PFlag status
    return
:not_prime
    cbr	PFlag status
    return


// converting binary to decimal
// input : nb
// output : ascii decimal representation in the stack
:int2str
    copyrr	nb r0
    copylr	stack stackPtr
    :get_digits                 
        div	r0 ten
        addla	'0'
        copyai	stackPtr
        incr	stackPtr
        copyra	r0
        bcrss	ZFlag status
        jump	get_digits
// Outputs the content of the stack over USB
:disp_nb
    copylr	3 r0
    copylr	stack+3 stackPtr
    :loop_out
        decr	stackPtr
        copyia	stackPtr
        bcrss	ZFlag status
        comout
        nop
        decrjz	r0
        jump loop_out
// Outouts a space separator
    copyla	' '
    comout
    return

// General Registers
%data 	dv 0
%data 	ten 10
%data 	r0 0
%data	nb 0
// Stack initialized with NULL caracters
%data 	stack 0 0 0 255
%data 	stackPtr 0
