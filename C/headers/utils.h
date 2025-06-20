#ifndef UTILS_H
#define UTILS_H

#include "includes.h"

/* Converts str to lowercase */
void StrToLower(char* str);

/* Empties stdin, consuming character until a \n or EOF is read.
If stdin is already empty, it blocks waiting an input*/
void CleanStdin();

/* Delete the '\n' from a string if it exists, returns 1 in that case.
Otherwise it returns 0 */
int DeleteNewLine(char* str);

/* Returns 1 if str contains only letters (a-z, A-Z). Returns 0 otherwise */
int IsAlphabetic(char* str);

/* Returns 1 if str contains only digits (0-9). Returns 0 otherwise */
int IsNumeric(char* str);

#endif