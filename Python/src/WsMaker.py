from random import shuffle, choice #random functionality to insert words or pick letters
from copy import deepcopy #deepcopy list to allow backtracking without overwriting
from typing import IO #type hinting
from Python.src.constants import ALPHABET #letters to fill the whitespaces of the word search
from Python.src.data import WsData, Word, Direction, DIR, ws
from Python.src.utils import (WrongWSDataFormat, FileException, OpenFile, CloseFile,
                   FileJumpToLine, BinarySearch, SaveFile)

def InitializeWSList(wsData: WsData) -> None:
    """
    Initializes the wsDP variable of a WsData object.
    
    Firstly appends a dimension x dimension list of empty str (""),
    then appends as many None's as words in the words list.
    """
    dim = wsData.dimension
    wordsNum = len(wsData.words)

    empty = [[""] * dim for i in range(dim)]
    #e.g. if dim == 3, empty = [["","",""], ["","",""], ["","",""]]

    wsData.wsDP.append(empty)
    for i in range(0, wordsNum):
        wsData.wsDP.append(None)

def WordsPositions(wsData: WsData) -> None:
    """Fills all the possible positions where to insert each word into the word search, taking into account
    the ws dimension and each word's direction. The positions are then shuffled to provide randomness.
    
    Modifies the WsData.words.positions and WsData.words.positionsIndex and doesn't return anything."""
    
    dim = wsData.dimension
    for word in wsData.words:
        posibilitiesCounter = 0
        
        wDir: DIR = word.dir.value
        wLen = len(word.string)-1

        #we loop through each index in dim*dim and see if it's possible to start writing the word in there
        for x in range(dim):
            for y in range(dim):
                #we verify that the last char's position is inside the boundaries (>= 0 and < dim) in x and y coordinates
                if (x + (wDir.x * wLen) < dim and x + (wDir.x * wLen) >= 0 and
                y + (wDir.y * wLen) < dim and y + (wDir.y * wLen) >= 0):
                    word.positions.append((x, y))
                    posibilitiesCounter += 1

        #we shuffle all the positions of the current word, so the indexes are easier to calculate after
        shuffle(word.positions)
        #positionsIndex = (0, j) because 0 is the first index to try in the algorithm
        word.positionsIndex = (0, posibilitiesCounter-1)

def InsertWord(wordStr: str, wordDir: Direction, position: tuple[int, int], ws: ws) -> tuple[bool, ws]:
    """Tries to insert a word in the desired direction and position in the word search.
    
    Doesn't modify the word search, returns a tuple (bool flag, newWs) indicating if the word could be inserted and
    the resultant word search."""
    
    newWs = deepcopy(ws) #deepcopy so each insertion doesn't modify the previous ws, in case of backtrack

    i = 0
    flag = False #becomes True if word couldn't be inserted
    #because of the way we store our ws, x and y coordinates are inverted
    startY, startX = position
    incrementY, incrementX = wordDir.value
    while (i < len(wordStr) and not flag):
        #for each char of word, we calculate the x,y position of it depending on the start position and direction
        x = startX + i * incrementX
        y = startY + i * incrementY

        #we write the char (if necessary) and go on to the next one
        if (newWs[x][y] == "" or newWs[x][y] == wordStr[i]):
            if (newWs[x][y] == ""):
                newWs[x][y] = wordStr[i]
            i += 1
        else:
            flag = True

    return (not flag, newWs) #return (True, newWs) if word was correctly inserted

def WsInsertWords(wsData: WsData) -> None:
    """Tries to insert all words into an empty word search. Uses the vars 'words' and 'wsDP' from a WsData object.
    
    Modifies the wsDP var in WsData struct. The last element of wsDP will be the ws with all words inserted (if possible),
    otherwise it will be None. Doesn't return anything.
    """
    #this is a backtracking with dynamic programming (dp) algorithm
    #it tries to insert each of the words (WsData.words) in order (this is pre-shuffled) and uses
    #an auxiliar structure (WsData.wsDP) to save the state of the ws each time a word is inserted
    #when a new word can't be inserted, it goes back to a previous word and changes it's position (using Word.positions) to try again 
    #the algorithm ends if all words are inserted, or all possibilities are exhausted

    i = 0
    solution = False
    final = False
    while (not final and not solution):
        wordI = wsData.words[i]
        #Word.positionsIndex is an auxiliar tuple that tells us which position to try, and how many positions are in total
        currentPosIdx = wordI.positionsIndex[0]
        posAvailable = wordI.positionsIndex[1]
        #in this case, we have no more possibilities in the current word, so we go back (if possible) to try other combinations
        if (currentPosIdx > posAvailable):
            if (i > 0):
                wordI.positionsIndex = (0, posAvailable) #we will try again with the first position of the current word in the future
                i -= 1 #go back to previous word
            else:
                final = True #there's no words "behind", so there's no possible solution

            continue

        #otherwise, we try to insert our i-th word in the position Word.positions[currentPosIdx], in the i-th ws in WsData.wsDP
        #this doesn't modify the i-th wsDP ws, it returns a new one with a bool flag
        insertedFlag, newWS = InsertWord(wordI.string, wordI.dir, wordI.positions[currentPosIdx], wsData.wsDP[i])

        if insertedFlag:
            wsData.wsDP[i+1] = newWS #we save the ws with the i-th word inserted in the (i+1)-th ws
            wordI.positionsIndex = (currentPosIdx+1, posAvailable) #important to know this positions been tried in case of backtrack

            if (i >= len(wsData.words)-1):
                solution = True
            else:
                i += 1
        else:
            #if word couldn't be inserted, we try with the next position in the current word
            wordI.positionsIndex = (currentPosIdx+1, posAvailable)

def FillChars(ws: ws, alphabet: str) -> None:
    """Fills all whitespaces in a word search with random chars from alphabet argument.
    
    Modifies the original ws struct and doesn't return anything."""

    #we use enumerate to "zip" the ws with the corresponding index of each element
    for i, line in enumerate(ws):
        for j, c in enumerate(line):
            if not c:
                ws[i][j] = choice(alphabet) #so here we can access each index properly

def RetWSData(wsDataFile: IO) -> WsData:
    """Returns a WsData struct containing dimension and words info from a wsData file.
    
    If an error occurs or the file is wrongly formatted, raises an exception."""
    
    wsData = WsData()

    #we handle empty lines and extra whitespaces (at the sides of the line)
    #but other format errors may result in WrongWSDataFormat exception

    #we read the next non-empty line to the DIMENSION line searching for an int
    str = FileJumpToLine(wsDataFile, "DIMENSION")
    if (str == "DIMENSION"):
        str = FileJumpToLine(wsDataFile)
        try:
            if not str:
                raise WrongWSDataFormat("DIMENSION line not followed by dimension number")
            
            wsData.dimension = int(str)
        except:
            raise WrongWSDataFormat("Dimension isn't numerical")
    else:
        raise WrongWSDataFormat("DIMENSION line wasn't found")

    #now we search for the words below the WORDS line, and expect at least 1 word
    #each word line must be exactly: "word" "direction", with word a alphabetic string and direction an int between 0-5
    str = FileJumpToLine(wsDataFile, "WORDS")
    if (str == "WORDS"):
        for line in wsDataFile:
            str = line.strip(" \n")
            if not str:
                continue #skip empty lines

            lineSplit = str.split(" ")
            if len(lineSplit) != 2:
                raise WrongWSDataFormat("Words contain a wrong formatted (word, dir) pair")
            
            wordStr = lineSplit[0]
            directionStr = lineSplit[1]
            
            if (not wordStr.isalpha() or not directionStr.isnumeric()):
                raise WrongWSDataFormat("Words contain a wrong formatted word or dir (non alpha word or non numeric dir)")

            dirInt = int(directionStr)
            if dirInt < 0 or dirInt > 5:
                raise WrongWSDataFormat("Words contain a wrong direction (must be dir [0..5])")

            word = Word(wordStr, Direction[dirInt]) #create a Word struct with str and Direction (Enum)
            wsData.words.append(word) #append word to the WsData struct

            print(f"Added: {word.string}, {word.dir} ({word.dir.value})")
    else:
        raise WrongWSDataFormat("WORDS line wasn't found")

    if not wsData.words:
        raise WrongWSDataFormat("There wasn't any words in file")

    return wsData

def WordsValidation(lexiconFile: IO, wsData: WsData) -> None:
    """Validates each word in a WsData struct with a lexicon file, replacing missing words with random ones. ASSUMES LEXICON IS SORTED.
    
    Modifies the original struct and doesn't return anything."""

    #we read all at once each word in the lexicon and put them into a list (which is in fact a dynamic array)
    #we do so to be able to use binary search for optimization, to search for each of our words in the lexicon (which must be alphabetically sorted)
    lexiconWords = [line.rstrip('\n') for line in lexiconFile]
    for word in wsData.words:
        if not BinarySearch(lexiconWords, word.string):
            replace = choice(lexiconWords)
            print(f"Replacing {word.string} with {replace}.")

            word.string = replace

def LoadFilesData() -> WsData:
    """Asks the user for the paths of the lexicon and word search data files. Retrieves the dimension, words of the ws, uses the
    lexicon to validate each word and closes all the opened files.
    
    Returns a WsData struct with dimension and words properly initialized if possible. Otherwise, returns None."""

    #try to open the lexicon and wsData files, asking for user input
    lexiconFile = wsDataFile = None
    try:
        lexiconPath = input("Enter the path of the file containing the available words: ")
        lexiconFile = OpenFile(lexiconPath, "r")

        wsDataPath = input("Enter the path of the file containing the information to make the Word Search (the C output): ")
        wsDataFile = OpenFile(wsDataPath, "r")
    #if it's not possible to do so, we close any open file and return None
    except FileException as e:
        print(f"Error opening the chosen files:\nError: {type(e).__name__}\nAdditional info : {e}")
        CloseFile(lexiconFile)
        CloseFile(wsDataFile)
        return None
    except Exception as e:
        print(f"Unexpected error opening the chosen files:\nError: {type(e).__name__}\nAdditional info : {e}")
        CloseFile(lexiconFile)
        CloseFile(wsDataFile)
        return None

    #try to read the wsData file, loading dimension and words into a WsData struct
    try:
        wsData = RetWSData(wsDataFile)
    #there can be errors reading the file or if the file is incorrectly formatted
    except WrongWSDataFormat as e:
        print(f"Error, the WS data file format is incorrect:\nError: {type(e).__name__}\nAdditional info: {e}")
        CloseFile(lexiconFile)
        return None
    except Exception as e:
        print(f"Unexpected error reading the WS data file:\nError: {type(e).__name__}\nAdditional info: {e}")
        CloseFile(lexiconFile)
        return None
    finally:
        CloseFile(wsDataFile)

    #validate the words with our lexicon file and then close it
    WordsValidation(lexiconFile, wsData)
    CloseFile(lexiconFile)

    return wsData

def WsToText(ws: ws) -> str:
    """Formats a ws (2d char list) to plain text and returns it. Doesn't modify the original ws."""

    wsTemp = [line + ["\n"] for line in ws] #appends a newline to each line (element) of the ws (in a copy)
    wsFlattened = [c for line in wsTemp for c in line] #flattens 
    wsFlattened.pop() #removes last newline
    
    return "".join(wsFlattened) #joins all the chars into a string

def ShowWSText(ws: str) -> None:
    """Prints word search to console."""

    print("--------------------------")
    print(ws)
    print("--------------------------")

def SaveWS(ws: ws) -> None:
    """Shows a word search in console, then asks the user to save it to a file."""

    wsText = WsToText(ws)
    ShowWSText(wsText)

    answer = input("Enter the file path to save the Word Search (N to cancel): ")
    if (answer == "N" or answer == "n"):
        print("Goodbye.")
    else:
        SaveFile(wsText, answer)

def WsMaker() -> bool:
    """Runs the word search maker program.
    
    It first loads all the necessary data from the lexicon and input file (user input required).
    Then it tries to generate the word search, outputs to the console and asks to save to a text file.

    Returns True if the word search was properly generated, False otherwise."""

    #asks for user input to load lexicon and ws data files, validates and processes the input, generating a WsData object
    wsData : WsData = LoadFilesData()

    if not wsData or not wsData.words:
        print("Couldn't retrieve correct information from files. End.")
        return False

    #generates the positions and positionsIndex for each Word in wsData
    WordsPositions(wsData)

    #creates the wsDP structure for the backtracking algorithm
    InitializeWSList(wsData)

    #tries to insert each word in the word search, verifies if it was possible and fills whitespaces before saving the file
    WsInsertWords(wsData)
    wsFinal = wsData.wsDP[-1] #gets the last element of the wsDP struct, if it's None then there's no solution
    if wsFinal:
        FillChars(wsFinal, ALPHABET)
        SaveWS(wsFinal)
        return True
    else:
        print("There's no solution.")
        return False