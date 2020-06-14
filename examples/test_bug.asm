// PrimeSerial
// Olivier Lecluse
// Brent Hauser
// Platform : Digirule2U

%define	status	252
%define	dataLED	255

%define	ZFlag	0

// Displays init_str
:disp_initstr
  copyra	init_str
  bcrsc	ZFlag status
  jump	search_loop
  comout
// Increments argument of copyra instruction
  incr	disp_initstr+1
  jump	disp_initstr

:search_loop
    halt
%data	init_str "Hello, World" 0
%data	init_strPtr 0