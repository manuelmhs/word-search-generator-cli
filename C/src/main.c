#include "../headers/includes.h"
#include "../headers/utils.h"
#include "../headers/data.h"
#include "../headers/macros.h"
#include "../headers/input_parsing.h"

/*
  Asks the user to enter all the necessary information for the word search.
  Waits for the keyword ENDSTR to finish the input.
*/
void InputData(Data* dat)
{
  printf("Enter the size for the word search:\n");

  int dim = GetDim();
  dataSetDim(dat, dim);

  printf("Enter the words followed by the direction for the word search, "
  "one at a time (enter %s to finish):\n", ENDSTR);

  int stopFlag = 0;
  while (!stopFlag)
  {
    printf("Word: ");
    char* word = GetWord();

    if (strcmp(word, ENDSTR) == 0)
    {
      stopFlag = 1;
      free(word);
    }
    else
    {
      StrToLower(word);
      
      printf("Direction (0-5): ");
      char* dir = GetDir();

      //we don't allow duplicates in the words
      int repeatWord = dataSearchWord(word, dat);

      if (repeatWord)
        printf("Word already registered!\n");
      else
        dataAppendWord(dat, word, dir);
      
      free(word); free(dir);
    }
  }
}

/*
  Returns 0 if writing is successful
  Returns 1 if there's a problem closing the file
  Returns 2 if the data entered by the user doesn't contain any words
*/
int DataToFile(Data* dat)
{
  if (isDataEmpty(dat)) return 2;
  
  char strFile[50];
  printf("Enter file directory to save: ");
  scanf("%49s", strFile); //we should use a safer input

  FILE* fd = fopen(strFile, "w");
  while (fd == NULL)
  {
    printf("Couldn't open file. Retry: ");
    scanf("%49s", strFile);
    fd = fopen(strFile, "w");
  }

  int ret;
  
  char strFormat[50];
  snprintf(strFormat, 50, FILEFORMAT, dataGetDim(dat));

  //we should check if writing is successful also
  fputs(strFormat, fd);
  fputs(dataGetWords(dat), fd);

  int closeVal = fclose(fd);

  if (closeVal == EOF) ret = 1;
  else ret = 0;
  
  return ret;
}

/*
  The program waits for user input in InputData (dimension, words, directions) and then tries to
  write the information in a file.
*/
int main()
{
  Data* dat = dataCreate();
  InputData(dat);

  int saveFlag = DataToFile(dat);

  switch (saveFlag)
  {
    case 0: printf("File was correctly saved.\n"); break;
    case 1: printf("File couldn't be saved correctly (error in file creation or save).\n"); break;
    case 2: printf("File not created. There's no words to save.\n"); break;
  }

  dataDelete(dat);
  return 0;
}
