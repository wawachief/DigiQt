// OperationTrainer - Olivier Lecluse 07 / 2020 
// CC BY-NC-SA 

// Start the program. Choose your operation : 
// - D0 = Addition trainning 
// - D1 = Substraction trainning 
// Add (or substract) the numbers displayed on AR and DR 
// Press buttons to input the answer 
// While the button is pressed, you can see the current input on DR 
// As soon the answer is OK, you will see a flashing animation 
// switching between input numbers ans the answer 
// Press a button to play again. 

// demo tour : https://youtu.be/U_D4bkQjlSA 

initsp	
sbr	_sar _sr // Autorise l’écriture sur les LED d’adresses 

// Operation Choice 
// D0 = Addidion 
// D3 = 2-complement
// D7 = Substration 

:begin 
  copylr	0b10001001 _dr 
  copylr	1 _ar 

  copylr	0 input 
  randa	
  andla	0b01111111 
  bcrsc	_z _sr 
  orla	1 // n1 can't be 0
  copyar	n1 
  randa	
  andla	0b01111111 
  copyar	n2 

// Choose which game we play
:choice 
  copylr	0xff waitCounter 
:choiceLoop 
  decrjz	waitCounter 
  jump	choiceLoop 

  shiftrl	_ar 
  bcrsc	7 _br 
  jump	subChoice 
  bcrsc	3 _br 
  jump	2cmpChoice 
  bcrsc	0 _br 
  jump	addChoice 
  jump	choice 

// We modify the operation instruction in the program for the game chosen
:addChoice 
  copylr	9 ml1+5 // addra opcode = 18 (9 on 2A) 
  jump	wait4begin 
:2cmpChoice 
  copylr	0 n1 
:subChoice 
  copylr	11 ml1+5 // subra copcode = 20 (11 on 2A) 

:wait4begin 
// Wait for choice release to begin 
  copyra	_br 
  bcrss	_z _sr 
  jump	wait4begin 

:mainloop 
  cbr	_c _sr 
  copyrr	n1 _ar 
  bcrss	_z _sr // if n1=0 (2 complement game) 
  jump	ml1 
  copyrr	input _ar // display input on AR
:ml1 
  copyrr	n2 _dr 
  copyra	n1 
  addra	n2 // [ml1+5] 
  xorra	input 
  bcrss	_z _sr 
  jump	wait4press 
  jump	win 

:win 
  copylr	255 _ar 
  copyrr	input _dr 
  call	wait 
  copyrr	n1 _ar 
  copyrr	n2 _dr 
  call	wait 
  jump	win 

// waits a long time using a 16 bits counter
:wait 
  copylr	0x8 waitCounter // change this to change the delay
  copylr	0xff waitCounter+1 
:waitLoop 
// Press button to start again 
  copyra	_br 
  bcrss	_z _sr 
  jump	restart 

// 16 bits counter 
  cbr	_c _sr 

  copyra	waitCounter+1 
  subla	1 
  copyar	waitCounter+1 

  copyra	waitCounter 
  subla	0 
  copyar	waitCounter 

  bcrss	_z _sr 
  jump	waitLoop 
  return	

:restart 
// wait for button release to restart 
  copyra	_br 
  bcrss	_z _sr 
  jump	restart 
  jump	begin 

// Button Handling 
:wait4press 
  copyra	_br 
  bcrss	_z _sr 
  jump	wait4release 
  jump	wait4press 
:wait4release 
  copyrr	_br btntmp 
  bcrsc	_z _sr 
  jump	release 
  copyra	input 
  xorra	btntmp 
  copyar	_dr 
  jump	wait4release 
:release 
// button is released 
  copyrr	_dr input 
  jump	mainLoop 


%data input 0 
%data btntmp 0 
%data n1 0 
%data n2 0 
%data waitCounter 0 0 