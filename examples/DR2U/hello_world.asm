// hello world sample program 

%define cr 13 
%define lf 10

:start 
  copylr	hello loop+1 // point to beginning of string 

:loop 
  copyra 0
  incr	loop+1 // point to next character 

  xorla	0 
  btstsc	_z _sr // if not NUL 
  jump	start // if NUL (end of string) 

  comout	// output character 
  jump	loop 


%org 0x20 

%data hello " _  _     _ _      __      __       _    _   _ " cr lf "| || |___| | |___  \ \    / /__ _ _| |__| | | |" cr lf "| __ / -_) | / _ \  \ \/\/ / _ \  _| / _` | |_|"  cr lf "|_||_\___|_|_\___/   \_/\_/\___/_| |_\__,_| (_)" cr lf 0 