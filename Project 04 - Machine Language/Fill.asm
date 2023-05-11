// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.


(LOOP) //starting the infinite loop until the keyboard tell us stop
@SCREEN //screen 
D=A // pointer 
@i 
M=D

@KBD //keyboard 
D=M 
@FILLWHITE
D;JEQ // if no key is pressed,then fill pixel in white
@FILLBLACK
0;JEQ // if a key is pressed, then fill pixel in black

 
(FILLBLACK) // Fill the pixel in black color
@CHANGE
M=-1
@SETPIXEL
0;JMP

(FILLWHITE) // Fill the pixel in white color
@CHANGE
M=0
@SETPIXEL 
0;JMP


(SETPIXEL) //changing the CHANGE of the pixel according to the keyboard input
@i
D=M
@KBD
D=D-A
@LOOP
D;JEQ

@CHANGE
D=M
@i
A=M
M=D
@i
M=M+1
@SETPIXEL
0;JMP