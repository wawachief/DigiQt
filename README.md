# DigiQt

Simulator of digirule 2 (https://bradsprojects.com/digirule2/) written in Python.

# Installation 

## Windows platform

You can get the MSI installer here : https://drive.google.com/drive/folders/1dwLxvtCJGBuTdACno-ls_LYQgG-knT0l

Just install the program. Launch **Main.exe**.

## Linux platform

A standalone AppImage can be found here : https://drive.google.com/drive/folders/1dwLxvtCJGBuTdACno-ls_LYQgG-knT0l

Just download the .AppImage file, make it executable and clic on it.

## Osx

I don't have a valid developper certificate, so my build won't launch for security reasons. You have to proceed manually and launch the program from source. Here is the procedure :
1. download and install python (3.6 minimum - 3.8.5 is the latest version when I write this guide and works fine) : https://www.python.org/downloads/mac-osx/
1. open a terminal window and install the following packages via your favorite Python package manager (*pip* or *conda*)
	- pyside2 
	- serial
	- serial-tool
	
`sudo pip3 install pyside2 serial serial-tool`shoud do it.
3. Go into the DigiQt source directory and launch the program : `python3 main.py`

# Instruction set

DigiQt offers the *Digirule 2A, 2B & 2U* instruction set. Choose in the button the model corresponding to the hardware you want to simulate.

# Assembler Quick guide

## Assembler special directives

- **%define** : defines constants. Usage : `%define NAME VALUE`
```
// Constants
%define myNumber  42
```

Some symbols corresponding to Digirule registers are already defined :
	- `_sr` : Status Register (252)
	- `_br` : Button Register (253)
	- `_ar` : Address Register (254)
	- `_dr` : Data Register (255)
	- `_z` : Zero FLag (0)
	- `_c` : Carry FLag (1)
	- `_sar` : Show Address Register FLag (2)

- **%data** : Inserts one or many bytes in the code. Usage : `%data NAME byte1 byte2 ... byten`
```
// Variables declarations
%data index 0
%data lineadr 0

// Drawing
%data POV 126 129 165 129 165 153 129 126
```

- **%org** : Allows you to choose the value of program counter where the following code will take place. This can be useful if you want your variables to take place at a specific location.

Example : 
```
// some stuff
// ...

%org 248
%data myVariable 0xFF
%data otherVariable 0x01
```
The `myVariable` variable will be at location 248, `otherVariable` will be at location 249.

## Labels
Labels begin with `:`.
```
:loop
	copyir lineadr _dr
	incr lineadr
	decrjz index
	jump loop
```
## Comments

Comments begin with `//`

## Ofsets
You can put ofsets just after a symbol (variable name or label). It will allow you to deal easily with multi-bytes variables.

Example : you want to access second byte of the `bigNumber` variable
```
// copies 0xC1 into acccumulator
copyra bigNumber 
// copies 0x06 into acccumulator
copyra bigNumber+1 

%data bigNumber 0xC1 0x06
```

Ofsets are not additions !

## Numbers 

Numbers are 8 bits long and can be in decimal (`127` for example), in hexadecimal beginning with **0x**(`0xC1`) or in binary beginning with **0b** (`0b11110101`).

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
