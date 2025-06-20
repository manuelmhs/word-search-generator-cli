# Word search generator program
[Main documentation](../README.md)

The python program first asks for lexicon and input data files. The lexicon is then used to validate the given words, and randomly replace the missing ones.\
Then, the main algorithm attempts to write all the words in the limited space given at random starting positions, using dynamic programming and backtracking. If it's possible to do so, it fills the remaining blanks with random characters.\
Finally, if the word search was properly generated, asks the user for a file path to save the result.

## Usage

To simply run the Python program, from a terminal on the root folder use: ```python3 -m Python.run```.\
Then just enter the information prompted on console.

From a terminal on the root folder, an example of use would be:
```bash
python3 -m Python.run
Resources/lexicon.txt
Resources/wsData1.txt
Resources/output1.txt
```

## About

- **Testing**: see [testing section below](#testing).

- **Algorithms**: we use a simple iterative backtracking algorithm to insert each of the necessary words in the word search.\
If we can't insert a given word, the algorithm returns to a previous state and tries an available different option. Finally, we find a valid layout for all the words if possible, otherwise, all possibilities are tried before terminating.\
Randomness is handled by shuffling the word's possible starting positions before the algorithm starts.

- **Data structures**: a word search is represented by a 2d char array in Python, whereas we use an array of word searchs to implement backtracking in our algorithm. This structure acts like a form of dynamic programming saving intermediate states.\
An important improvement would be to replace this dp structure for a cache that only saves the changes made in each insertion. This is particularly impactful if we work with a bigger dimension (size) word search.
We also use Python's dataclasses and typing utilities to improve code readability, modularization and abstraction.

- **Error handling**: we handle incorrect user input, errors in I/O files and incorrect file formats using Python's try-except-else-finally feature as well as raising our own personalized exceptions. This provides a safe and robust code structure to handle exceptions, avoid crashes and manage custom behaviours.

## Testing

The **tests** folder contains different test cases using the **pytest** framework for automatization, as well as fixtures, asserts, monkeypatching, mockups, etc.\
You can run all test cases using ```pytest -vv Python``` from a terminal on the root folder. These tests involve unit, functional and integration testing.

- The use of **pytest** allows test automatization. This is useful to run tests automatically in each code-execute cycle and avoid unexpected errors.
- **Assertion** testing allows to know if each function or module tested behaves as we intend to, as a sort of specification for our code.
- **Fixtures** and **monkeypatching** allows us to prepare a specific environment for each test safely. Altogether with **mockups** we can set a specific random seed, predefine user input or work with certain file's data.