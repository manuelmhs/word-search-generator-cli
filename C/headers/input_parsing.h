#ifndef INPUT_PARSING_H
#define INPUT_PARSING_H

#include "includes.h"
#include "macros.h"
#include "utils.h"

/*
    Functions that allow safe input parsing for the information used in Data struct.
    We could use more general functions with arguments if we need to reuse them for other purposes. 
*/

/*
    Uses dynamic memory, must free returned string.
    Allows input that's at most WORDLEN chars, and only letters (a-z/A-Z). Doesn't allow empty input.
    Asks the user again until the input is correct.
    Output is the string with '\0' and without '\n'.
*/
char* GetWord();

/*
    Uses dynamic memory, must free returned string.
    Allows input that's at most DIRLEN chars, and only numbers between (DIRMIN, DIRMAX). Doesn't allow empty input.
    Asks the user again until the input is correct.
    Output is the string with '\0' and without '\n'.
*/
char* GetDir();

/*
    Allows input that's at most DIMLEN chars, and only numbers (0-9). Doesn't allow empty input.
    Asks the user again until the input is correct.
    Output is a positive int.
*/
int GetDim();

#endif