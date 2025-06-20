from bisect import bisect_left #For binary search in the lexicon file (must be sorted)
from typing import Any, IO #Type hinting

class WrongWSDataFormat(Exception):
    """Personalized exception used when the word search data file format is incorrect in any ways"""
    pass

class FileException(Exception):
    """Personalized exception used when there's a problem opening a file."""
    pass

def OpenFile(path: str, mode: str, Encoding: str=None, Newline: str=None, retry: int=5) -> IO:
    """
    Tries to open the file with the given path and mode.
    If it can't, it asks for another path up to a given amount of retries.

    Returns the opened file or raises FileException.
    """
    fileFlag = False
    file = None
    while fileFlag == False and retry > 0:
        retry -= 1
        try:
            file = open(path, mode, encoding=Encoding, newline=Newline)
        except Exception as e:
            print(f"Error opening file:\n{type(e).__name__}\n{e}")
            path = input("Couldn't open file. Retry: ")
        else:
            fileFlag = True

    if not file:
        raise FileException("Max. retries reached. Couldn't open file")

    return file

def CloseFile(file: IO) -> int:
    """Closes the given file and returns True, or returns False is an exception occurs."""
    try:
        file.close()
        return True
    except Exception as e:
        print(f"Error closing file:\n{type(e).__name__} : {e}")
        return False

def FileJumpToLine(file: IO, str: str="") -> str:
    """
    If a string is given, seeks for the first occurrence of it in the file (which lines are stripped for " \\n").
    If there's no str given, it seeks for the first non-empty line (whitespaces don't count).

    Returns the last line read (and the file pointing to the next line), or the last line of the file.
    """
    cleanLine = ""
    for line in file:
        cleanLine = line.strip(" \n")
        if not str and cleanLine:
            break
        elif str and cleanLine == str:
            break
    
    return cleanLine

def BinarySearch(list: list[Any], item: Any) -> bool:
    """
    Given a sorted list, returns True if item is found in list or False otherwise.
    
    Unexpected behaviour if list isn't sorted.
    """
    idx = bisect_left(list, item)
    return (idx < len(list) and list[idx] == item)

def SaveFile(data: str, path: str=""):
    """
    Saves data str to file given by path (or asks for path if empty).

    Returns True if saved correctly or False if couldn't open/write file.
    """
    if (not path):
        path = input("Enter the file path: ")

    try:
        file = OpenFile(path, "w")
    except Exception as e:
        print(f"Error opening file:\n{type(e).__name__} : {e}")
        return False

    try:
        file.write(data)
        CloseFile(file)
    except Exception as e:
        print(f"Error writing data to file:\n{type(e).__name__} : {e}")
        return False
    else:
        print("File saved correctly.")
        return True