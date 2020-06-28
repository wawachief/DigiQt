%define status 252 
%define Carry 1 

sbr	Carry status 
copyra	mod10 
subla	10 
copyar	result 
copyra	mod10+1 
subla	0 
copyar	result+1 

%org 240
%data mod10 0b1001 0 
%data result 0 0 


