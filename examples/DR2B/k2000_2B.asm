speed    40 

:start 
  tbr    7 255 
  decrjz    start+1 
  jump    start 

  tbr    0 255 
:start1 
  tbr    248 255 
  incrjz    start1+1 
  jump    start1 

// get things in order for the second round !
  copylr    248 start1+1 
  copylr    7 start+1 

jump    start 