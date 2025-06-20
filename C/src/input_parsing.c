#include "../headers/input_parsing.h"

char* GetWord()
{
  char* word = malloc(sizeof(char) * (WORDLEN + EXTRACHARS)); //EXTRACHARS count \0 and \n
  fgets(word, WORDLEN + EXTRACHARS, stdin);
  int newL = DeleteNewLine(word);
  int isAlpha = IsAlphabetic(word);

  int retry = 0;
  if (strlen(word) <= 0)
  {
    printf("Empty input. Retry: ");
    retry = 1;
  }
  else if (!newL)
  {
    printf("Input too long. Retry: ");
    //we must clean stdin because we know there's chars left (not in other cases because it blocks)
    CleanStdin();
    retry = 1;
  }
  else if (!isAlpha)
  {
    printf("Words can only contain letters (a-z). Retry: ");
    retry = 1;
  }
  
  if (retry)
  {
    free(word);
    return GetWord();
  }
  
  return word;
}

char* GetDir()
{
  char* dirStr = malloc(sizeof(char) * (DIRLEN + EXTRACHARS));
  fgets(dirStr, DIRLEN + EXTRACHARS, stdin);
  int newL = DeleteNewLine(dirStr);
  int isNum = IsNumeric(dirStr);

  int retry = 0;
  if (strlen(dirStr) <= 0)
  {
    printf("Empty input. Retry: ");
    retry = 1;
  }
  else if (!newL)
  {
    printf("Input too long. Retry: ");
    CleanStdin();
    retry = 1;
  }
  else if (!isNum)
  {
    printf("Direction must be an int. Retry: ");
    retry = 1;
  }
  else if (newL && isNum)
  {
    int dir = atoi(dirStr);
    if (dir < DIRMIN || dir > DIRMAX)
    {
      printf("Direction must be a number between (%d-%d). Retry: ", DIRMIN, DIRMAX);
      retry = 1;
    }
  }
  
  if (retry)
  {
    free(dirStr);
    return GetDir();
  }

  return dirStr;
}

int GetDim()
{
  char dimStr[DIMLEN + EXTRACHARS];
  fgets(dimStr, DIMLEN + EXTRACHARS, stdin);
  int newL = DeleteNewLine(dimStr);
  int isNum = IsNumeric(dimStr);

  int dim = -1, retry = 0;
  if (strlen(dimStr) <= 0)
  {
    printf("Empty input. Retry: ");
    retry = 1;
  }
  else if (!newL)
  {
    printf("Input too long. Retry: ");
    CleanStdin();
    retry = 1;
  }
  else if (!isNum)
  {
    printf("Dimension must be a positive int. Retry: ");
    retry = 1;
  }
  else if (newL && isNum)
    dim = atoi(dimStr);

  if (!retry && dim <= 0)
  {
    printf("Dimension must be greater than zero. Retry: ");
    retry = 1;
  }
  
  if (retry) return GetDim();

  return dim;
}