// Complement a 2 
// Olivier Lecluse 
// Utiliser les boutons pour choisir un nombre 
// Le complément a2 s’affiche en temps réel 


initsp	
speed	0 
sbr	_sar _sr // Autorise l’écriture sur les LED d’adresses 

:debut 
  cbr _c _sr
  copyla	0 
  subra	_dr // Acc = 0 – dataLEDRegister 
  copyar	_ar 
  copyrr	_dr lastData 
  copyra	_br 
// Réalise un XOR entre les boutons et dataLED 
// afin de prendre en compte une éventuelle saisie 
  xorra	_dr 
  copyar	_dr 
  subra	lastData 
// Si aucun bouton n’a été préssé, on revient au début 
  bcrss	_z _sr 
  call	wait 
  jump	debut 

// Boucle d’attente de 10*255 tours sur la vraie DGR 
:wait 
  copylr	18 loopTouche 
:waitloop 
// copylr 7 loopTouche1 // use this for digimulator 
  copylr	255 loopTouche1 // use this for digirule 
:waitloop1 
  decrjz	loopTouche1 
  jump	waitloop1 
  decrjz	loopTouche 
  jump	waitloop 
  return	

%data lastData 0 
%data loopTouche 0 
%data loopTouche1 0 

