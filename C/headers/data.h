#ifndef DATA_H
#define DATA_H

#include "includes.h"
#include "macros.h"

/*
  Dynamic array with fixed resize factor used to store all the information the user inputs.
  By using a resize factor we intend to provide a O(1) amortized cost in insertion.

  A more practical choice would be, e.g. using a linked list that stores each word and direction,
  with a reference to the last element to make insertions faster
  (this would solve occasional reallocation when the user inserts a new word).
*/
typedef struct Data
{
  /* Words saved by our struct, following the format:
  word1 n1\nword2 n2\nword3 n3\n...\nwordX nX
  where wordX is the word saved and nX is the direction of it */
  char* words;
  unsigned int bytesAllocated; //Control of the bytes allocated in words
  unsigned int bytesInUse; //Control of the bytes currently occupied by words
  int dimension; //Dimension of the word search
} Data;

//Struct creation, memory allocation.
Data* dataCreate();

//Struct destruction, free resources.
void dataDelete(Data* datos);

//Access to the dimension stored.
int dataGetDim(Data* datos);
//Access to the words stored.
char* dataGetWords(Data* datos);

/*
  Inserts a new word to the Data struct, reallocating if necessary.
  It updates the bytesInUse and occasionally the bytesAllocated (if realloc was done).
*/
void dataAppendWord(Data* datos, char* word, char* dir);

//Sets the dimension.
void dataSetDim(Data* datos, int dim);

//Searches if a word is already stored in the struct. Returns 1 in that case, 0 otherwise.
int dataSearchWord(char cadena[], Data* datos);

//Searches if there's at least one word stored.
int isDataEmpty(Data* datos);

#endif