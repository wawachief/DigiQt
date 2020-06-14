# DigiQt

[![Alt text](https://img.youtube.com/vi/mRx_jkY8RU8/0.jpg)](https://www.youtube.com/watch?v=mRx_jkY8RU8)

Simulator of digirule 2 (https://bradsprojects.com/digirule2/) written in Python.

# Instruction set

DigiQt offers the *Digirule 2A, 2B & 2U* enhanced instruction set. See https://github.com/wawachief/DGR2B for more informations.

# Assembler Quick guide

## Assembler special commands

- **%define** : defines constants. Usage : `%define NAME VALUE`
```
// Constants
%define statusRegister  252
%define dataLEDRegister 255
%define hideAddressBit  2
```
- **%data** : inserts one or many bytes in the code. Usage : `%data NAME byte1 byte2 ... byten`
```
// Variables declarations
%data index 0
%data lineadr 0

// Drawing
%data POV 126 129 165 129 165 153 129 126
```

## Labels
Labels begin with `:`.
```
:loop
	copyir lineadr dataLEDRegister
	incr lineadr
	decrjz index
	jump loop
```
## Comments

Comments begin with `//`

## Numbers 

Numbers are 8 bits long and can be in decimal (`127` for example) or in binary , beginning with `0b` (`0b11110101` for example).

# Attribution
Icons from: https://www.flaticon.com/

Authors: 
- *Freepik:* https://www.flaticon.com/authors/freepik
- *Roundicons:* https://www.flaticon.com/authors/roundicons
- *Pixel perfect:* https://www.flaticon.com/authors/pixel-perfect
- *Srip:* https://www.flaticon.com/authors/srip
- *Surang:* https://www.flaticon.com/free-icon/usb-cable_2890886
- *Good Ware:* https://www.flaticon.com/authors/good-ware
# Licence
GNU General Public License v3.0


![LECLUSE DevCorp.](assets/LDC-dark.png)
