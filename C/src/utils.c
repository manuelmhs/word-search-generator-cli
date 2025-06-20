#include "../headers/utils.h"

void StrToLower(char* str)
{
  for(size_t i = 0; i < strlen(str); i++)
    str[i] = tolower(str[i]);
}

int DeleteNewLine(char* str)
{
  int r = 0;
  char* newLinePtr = strchr(str, '\n'); //NULL if \n is not in str, ptr to \n otherwise
  if (newLinePtr)
  {
    *newLinePtr = '\0';
    r = 1;
  }

  return r;
}

void CleanStdin()
{
  int c;
  while ((c = getchar()) != '\n' && c != EOF); //searches for \n or EOF in stdin
  /* we search for both because, if there's input left in stdin there will be a \n, 
  but we also search for EOF in case there's an error */
}

int IsAlphabetic(char* str)
{
  int i = 0, flag = 1, len = strlen(str);
  while (i < len && flag)
  {
    flag = (isalpha(str[i]) != 0);
    i++;
  }

  return flag;
}

int IsNumeric(char* str)
{
  int i = 0, flag = 1, len = strlen(str);
  while (i < len && flag)
  {
    flag = (isdigit(str[i]) != 0);
    i++;
  }

  return flag;
}