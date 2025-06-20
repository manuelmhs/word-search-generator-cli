#include "../headers/data.h"

Data* dataCreate()
{
  Data* d = malloc(sizeof(Data));
  d->dimension = -1;
  //we first allocate INITSIZE chars
  d->bytesAllocated = sizeof(char) * INITSIZE;
  d->words = malloc(d->bytesAllocated);
  //we start with only a \0, to make it easier to insert the first element
  d->bytesInUse = sizeof(char);
  *(d->words) = '\0';

  return d;
}

void dataDelete(Data* d)
{
  free(d->words);
  free(d);
}

int dataGetDim(Data* d) { return d->dimension; }

char* dataGetWords(Data* d) { return d->words; }

void dataAppendWord(Data* d, char* word, char* dir)
{
  //if we currently have: "hello 0\n", and want to save: "world", "1"
  //then the result is: "hello 0\nworld 1\n"
  //so we add to bytesInUse: length of word + length of dir + " " + "\n" (the 2 extra bytes)
  d->bytesInUse += (strlen(word) + strlen(dir) + 2)*sizeof(char);

  //we expand the bytesAllocated only if (and while) it's lower than bytesInUse
  int needRealloc = 0;
  while (d->bytesAllocated < d->bytesInUse)
  {
    d->bytesAllocated *= RESIZEFACTOR;
    needRealloc = 1;
  }
  if (needRealloc) d->words = realloc(d->words, d->bytesAllocated); //we only realloc one time
  
  strcat(d->words, word);
  strcat(d->words, " ");
  strcat(d->words, dir);
  strcat(d->words, "\n");
}

void dataSetDim(Data* d, int dim) { d->dimension = dim; }

int dataSearchWord(char searchStr[], Data* d)
{
  /*
    The important thing is that we do not search if searchStr is a substring of d->words,
    because it would detect that "ola" is already stored if "hola" is in the struct.
    We basically divide each stored word and the compare if it's the exact same as searchStr.
    This would obviously be easier if we used a linked list instead of just a char* to store.
  */

  /*
    We read through the words until we reach a ' ', used as a delimiter of the words.
    We copy the word using two indexes and use strcmp to see if it's equal to searchStr.
    If not, we skip the following chars until we reach a '\n', so the next word comes next, and we repeat the process.
  */
 
  char* words = d->words;
  
  int skipFlag = 0; //skip the next chars until a '\n' is read
  int okFlag = 0; //word already found
  long unsigned int i = 0; //current index in words
  int initIdx = 0; int finishIdx = 0; //indexes to mark where the words start and finish
  while (i < strlen(words) && !okFlag)
  {
    if (!skipFlag)
    {
      if (words[i] == ' ')
      {
        finishIdx = i;
        char word[finishIdx-initIdx+1];
        memcpy(word, &(words[initIdx]), finishIdx-initIdx);
        word[finishIdx-initIdx] = '\0';

        if (strcmp(word, searchStr) == 0)
        {
          okFlag = 1;
          continue;
        }
        skipFlag = 1;
      }
    }
    else
    {
      if (words[i] == '\n')
      {
        skipFlag = 0;
        initIdx = i+1;
      }
    }

    i++;
  }

  return okFlag;
}

int isDataEmpty(Data* d) { return (d->bytesInUse == sizeof(char));  } //if there's only 1 char then it's the \0