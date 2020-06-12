// PrimeSerial
// Olivier Lecluse
// Platform : Digirule2U

%define 	status_reg  		252
%define 	dataLED_reg	255
%define 	pi		248

%define 	ZFlag	0
%define 	CFlag	1
%define 	PFlag	3		// we use bit 3 of status_reg to store the prime state

initsp
speed 	0

copylr	2 nb
call	disp_nb
copylr	3 nb
call 	disp_nb			// Displays 002 and 003

// compute all primes beginnig with 5 
copylr 	2 pi 			// 2 and 3 are primes and not computed
copylr 	5 nb 			// start the prime search with 5
:primeloop
    call 	prime_test
    bcrsc 	PFlag status_reg
    jump 	isprime
:pl1
    cbr 	ZFlag status_reg
    incr 	nb 
    bcrsc 	ZFlag status_reg
    jump 	the_end			 // End on game : nb > 255
    incr 	nb
    jump 	primeloop
:isprime
    copyrr 	nb dataLED_reg
    // output result to serial
    call disp_nb
    // searching next prime 
    incr pi
    jump pl1
:the_end
    halt

// Test if nb is prime
:prime_test
    copyrr 	nb dv
:loopdiv
    decr 	dv
    decr 	dv
    copyrr 	nb r0 			// arg1 is modified by div, 
    div 	r0 dv   			// arg1 is the quotient, acc the remainder
    bcrsc 	CFlag status_reg 
    jump 	not_prime
    copyra 	dv
    subla 	3
    bcrss 	ZFlag status_reg
    jump 	loopdiv
// Number is prime
    sbr 	PFlag status_reg
    return
:not_prime
    cbr 	PFlag status_reg
    return    

// outputs nb (3 digits)  on the serial port
:disp_nb				
    call 	int2str
    copyra 	ascii_str
    comout
    copyra 	ascii_str+1
    comout
    copyra 	ascii_str+2
    comout
    copyla 	' '			// add a space separator
    comout
    return

// Transforms an integer to an ASCII representation
// Input:
//    nb: int
//    ascii_str: Address of the first byte of the string
:int2str
    copyrr 	nb t0
    copylr 	10 r0
    div 	t0 r0
    addla 	'0'
    copyar 	ascii_str+2
    
    div 	t0 r0
    addla 	'0' 
    copyar 	ascii_str+1
    
    copyra 	t0
    addla 	'0'
    copyar 	ascii_str
    return


// General Registers
%data 	r0 0
%data	nb 0
%data 	dv 0
%data 	t0 0
%data 	ascii_str "000"
