# CLI Word Search Generator

This project consists of a CLI program that **generates a random word search** using input data previously asked to the user. It's divided in two different components that run separately coded in C and Python.

- **C/**: *asks the user for all the necessary information* to generate a word search, then outputs it to a desired file using a specific format.\
[C documentation](C/README.md)

- **Python/**: asks for the data file previously generated and a lexicon file (used to validate words) and *generates the word search* (if possible). There's also provided a tests folder to run with pytest.\
[Python documentation](Python/README.md)

- **Resources/**: contains some example lexicon and data files to use as input for the Python generator.\
[Resources documentation](Resources/README.md)

## Description

This program uses a **DP and backtracking algorithm** to generate a word search with the information provided by the user. This information is the size of the word search and a list of words to be included in it with a certain direction.\
The program attemps to generate a word search that contains all of the words in the desired directions, exhausting all possible combinations. If it's not possible to place all words within the space given the algorithm finishes properly.

## Requirements
- Linux (Ubuntu x86-64)
- gcc, make (GNU Compiler Collection)
- Python3 (3.12 or higher)

## Usage

Tested in Ubuntu using bash. Just ensure requirements are installed.

Clone the [repository](https://github.com/mmhs114/word-search-generator-cli.git) and enter the directory.\
Within the root folder using bash:
- ```make``` or ```make all``` compiles all C sources files and generates the output file.
- ```make run``` compiles (if necessary) and runs: pytest test cases, C output file and python program.
- ```make run TEST=false``` to not run test cases. 
- ```./WsInput.out``` to run the C program (if already compiled).
- ```pytest -vv Python``` to run all test cases.
- ```python3 -m Python.run``` to run the Python program.
