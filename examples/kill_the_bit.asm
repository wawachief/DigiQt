// This game starts with a single bit (LED) lit and continually shifts left.
// The aim of the game is to press any of the data input buttons, when the
// corresponding LED is lit to turn it off. Once all LED's are off - you have won
// the game. If you press the button when the LED is off - the LED will turn on
// and you will have more LED's to now 'kill'.

// Constants
%define statusRegister      252
%define buttonRegister      253
%define addressLEDRegister  254
%define dataLEDRegister     255

// Setup (this code runs once)
speed 32
copylr 1 dataLEDRegister

// Main loop (this code runs repeatedly until power is removed) 
:Loop
shiftrl dataLEDRegister
copyra buttonRegister
xorra dataLEDRegister
copyar dataLEDRegister
jump loop
