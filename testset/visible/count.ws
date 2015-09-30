WWWTN#put a one on the stack
NWWWTWWWWTTN#set a label point.
WNW# duplicate the top of the stack
TNWT# output the current value
WWWTWTWN# put ten on the stack
TNWW# output the value on the top of the stack as a char (newline)
WWWTN# put 1 on the stack
TWWW# addition - increments the current value
WNW# duplicates the current value on the stack
WWWTWTTN# put 11 onto the stack
TWWT# subtraction
NTWWTWWWTWTN# if top of stack is 0 jump to end.
NWNWTWWWWTTN# jump back to the start
NWWWTWWWTWTN# set the end label
WNN# discard the iterator
NNN# terminate
