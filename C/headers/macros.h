#ifndef MACROS_H
#define MACROS_H

#define ENDSTR "STOP" //Keyword to stop writing words
#define DIMLEN 4 //Max length of dimension
#define WORDLEN 30 //Max length of each word
#define DIRLEN 1 //Max length of each direction
#define DIRMIN 0 //Min value of each direction
#define DIRMAX 5 //Max value of each direction
#define EXTRACHARS 2 //Using fgets we will also receive the \n and \0 in the buffer
#define FILEFORMAT "DIMENSION\n%d\nWORDS\n" //Format used at the start of the output file
#define INITSIZE 10 //Initial size of the dynamic array
#define RESIZEFACTOR 2 //Resize factor for each realloc

#endif