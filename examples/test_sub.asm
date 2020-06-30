%define status 252 
%define Carry 1 
copylr 0 status
sbr 2 status
sbr Carry status
copyra val
subla 10

copyar 255
copyrr status 254 

:loop
  jump loop
  
%data val 0
