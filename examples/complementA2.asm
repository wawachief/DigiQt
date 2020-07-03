// Complement a 2 
// Olivier Lecluse 
// Utiliser les boutons pour choisir un nombre 
// Le complément a2 s’affiche en temps réel 


initsp	
sbr	_sar _sr // Autorise l’écriture sur les LED d’adresses 

:mainLoop 
  copyra	_br 
  bcrss	_z _sr 
  jump	wait4release 
  jump	mainLoop 

:wait4release 
  copyrr	_br btntmp 
  bcrsc	_z _sr 
  jump	release 
  copyra	input 
  xorra	btntmp 
  copyar	_dr 
// display 2-complement of input 
  cbr	_c _sr 
  copyla	0 
  subra	_dr 
  copyar	_ar 
  jump	wait4release 
:release 
// button is released 
  copyrr	_dr input 
  jump	mainLoop 


%data input 0 
%data btntmp 0 