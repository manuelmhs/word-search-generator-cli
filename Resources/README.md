# Resource files
[Main documentation](../README.md)

This folder contains **sample lexicon and data files** to run the Python Word Search generator.\
Note that the sample files are in Spanish. If you wish to generate a word search with english (or other languages) words you need to provide a different lexicon file.

## Lexicon file
Plain text file, **alphabetically sorted**, with exactly one word per line. The sorting is useful to implement *binary search* and the program doesn't handle unsorted lexicon files as-is.

## Data file
Contains the necessary information to generate a word search: *dimension*, to generate a (dimension x dimension) size word search, and *words* with a given *direction*.

A syntax example would be:
```
DIMENSION
x
WORDS
word1 dir1
word2 dir2
...
wordN dirN
```
where **x** is a positive int, **wordK** is a string and **dirK** is a [0-5] number.\
The program supports minor syntax changes such as extra newlines or whitespaces.