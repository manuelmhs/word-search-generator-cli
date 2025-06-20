# Word search input data generator
[Main documentation](../README.md)

**Asks the user to enter the dimension/size and words required** to generate a word search.\
Then saves this information to a desired output file using a specific syntax.

## Usage

When compiled and run (see main documentation), the program first asks for a valid dimension value. Then, it asks for a sequence of word-direction pairs until a STOP word is written.\
Finally the user can write a desired output file name to write this information.

From a terminal on the root folder, an example of use would be:
```bash
make
./WsInput.out
5
hola
0
STOP
output.txt
```

## About

- **Input parsing**: ensures all required information is valid and properly formatted, looking out for buffer overflows and other input related problems.
- **Data structures**: uses a dynamic array with geometric expansion that makes each new word insertion cost amortized. A singly linked list with reference to both ends would provide a cleaner interface.
- **Error handling**: besides a correct input parsing, error handling could be improved, e.g. when writing to file is needed.