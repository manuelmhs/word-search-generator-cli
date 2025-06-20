import pytest
from pathlib import Path
from os import remove
from random import seed #we use seed to properly test functions with random functionality
from copy import deepcopy

from Python.src.WsMaker import (
    InitializeWSList, WordsPositions, InsertWord, WsInsertWords,
    FillChars, RetWSData, WordsValidation, LoadFilesData,
    WsToText, ShowWSText, SaveWS, WsMaker) #all tested functions in this file

#functions needed to run the tests
from Python.src.utils import (OpenFile, CloseFile, WrongWSDataFormat)
from Python.src.data import Direction, Word, WsData
from Python.src.constants import ALPHABET

currentDir = Path(__file__).resolve().parent.as_posix()
"""Absolute path of the parent directory of this file."""

@pytest.fixture
def fixtureInsertWord():
    #region
    ws = [["","","","",""],
          ["","","","",""],
          ["","","","",""],
          ["","","","",""],
          ["","","","",""]]
    insert1 = ("bye", Direction.RIGHT, (1,0))
    outcome1 = [["","b","y","e",""],
                ["","","","",""],
                ["","","","",""],
                ["","","","",""],
                ["","","","",""]]
    insert2 = ("enemy", Direction.DOWN, (3, 0))
    outcome2 = [["","b","y","e",""],
                ["","","","n",""],
                ["","","","e",""],
                ["","","","m",""],
                ["","","","y",""]]
    insert3 = ("bare", Direction.RIGHTDOWN, (1,0))
    outcome3 = [["","b","y","e",""],
                ["","","a","n",""],
                ["","","","e",""],
                ["","","","m",""],
                ["","","","y",""]]
    insert4 = ("year", Direction.LEFT, (3,4))
    outcome4 = [["","b","y","e",""],
                ["","","","n",""],
                ["","","","e",""],
                ["","","","m",""],
                ["r","a","e","y",""]]
    insert5 = ("sea", Direction.UP, (2,2))
    outcome5 = [["","b","y","e",""],
                ["","","e","n",""],
                ["","","s","e",""],
                ["","","","m",""],
                ["r","a","e","y",""]]
    #endregion

    return (ws, (insert1, insert2, insert3, insert4, insert5),
            ((True, outcome1), (True, outcome2), (False, outcome3), (True, outcome4), (False, outcome5)))

def test_InsertWord(fixtureInsertWord):
    #we try to insert all the words in order, starting from an empty ws, and assert the results are correct
    ws, inserts, desiredOutcomes = fixtureInsertWord
    outcomes = [ws]
    for idx, insert in enumerate(inserts):
        initialWS = deepcopy(outcomes[idx])

        #the starred expression (*insert) separates the tuple: e.g. ("bye", Direction.RIGHT, (1,0)) in the three corresponding arguments
        flag, outcome = InsertWord(*insert, outcomes[idx])
        if flag:
            outcomes.append(outcome)
        else:
            outcomes.append(initialWS)

        assert flag == desiredOutcomes[idx][0] #we test the bool flag
        assert outcome == desiredOutcomes[idx][1] #the resultant ws
        assert initialWS == outcomes[idx] #and that the function doesn't modify the original one

@pytest.fixture
def fixtureWordsPositions(monkeypatch):
    #region
    #important: we patch the shuffle function imported in the WsMaker module, NOT directly from the random module
    #because this code will be executed when python already imported shuffle in WsMaker, changing later the random.shuffle
    #behaviour will not affect the already imported one in WsMaker
    #another solution would be, in the WsMaker module, use import random, and use random.shuffle, so it really changes it's
    #behaviour
    #this is because (i presume) WsMaker.shuffle or random.shuffle just point to the memory address of the actual code to execute
    #(like callbacks), and changing e.g. the random.shuffle behaviour just makes it point to another memory address with another code
    #but doesn't change the code already pointed to by WsMaker.shuffle
    #endregion
    monkeypatch.setattr("Python.src.WsMaker.shuffle", lambda x: x) #we ensure shuffle doesn't make any changes
    data = WsData(5, [Word("hello", Direction.RIGHT), Word("abcd", Direction.RIGHTUP), Word("goodbye", Direction.DOWN)])
    desiredPos = [[(0,0), (0, 1), (0, 2), (0, 3), (0,4)], [(0,3),(0,4),(1,3),(1,4)], []]
    desiredPosIdx = [(0, 4), (0, 3), (0, -1)]

    return (data, desiredPos, desiredPosIdx)

def test_WordsPositions(fixtureWordsPositions):
    data, desiredPos, desiredPosIdx = fixtureWordsPositions
    WordsPositions(data)

    for i, word in enumerate(data.words):
        assert word.positions == desiredPos[i]
        assert word.positionsIndex == desiredPosIdx[i]

@pytest.fixture
def fixtureInitializeWSList():
    #only the ws dimension and the number of Word is relevant
    data1 = WsData(1, [Word()])
    data2 = WsData(2, [Word(), Word(), Word()])
    return (data1, data2)

def test_InitializeWSList(fixtureInitializeWSList):
    data1, data2 = fixtureInitializeWSList
    InitializeWSList(data1)
    InitializeWSList(data2)

    desiredOutput1 = [[[""]], None]
    desiredOutput2 = [[["", ""], ["", ""]], None, None, None]

    assert data1.wsDP == desiredOutput1
    assert data2.wsDP == desiredOutput2

@pytest.fixture
def fixtureWsInsertWords(monkeypatch):
    monkeypatch.setattr("Python.src.WsMaker.shuffle", lambda x: x)

    data1 = WsData(5, [Word("hello", Direction.RIGHT), Word("ready", Direction.DOWN), Word("have", Direction.RIGHTDOWN)])
    WordsPositions(data1)
    InitializeWSList(data1)
    desiredOutput1 = [
        ["","r","","",""],
        ["h","e","l","l","o"],
        ["","a","","",""],
        ["","d","v","",""],
        ["","y","","e",""]
    ]

    data2 = WsData(4, [Word("have", Direction.RIGHTDOWN), Word("care", Direction.LEFT)])
    WordsPositions(data2)
    InitializeWSList(data2)
    desiredOutput2 = None

    return (data1, data2, desiredOutput1, desiredOutput2)

def test_WsInsertWords(fixtureWsInsertWords):
    data1, data2, desiredOutput1, desiredOutput2 = fixtureWsInsertWords

    WsInsertWords(data1)
    final1 = data1.wsDP[-1]

    WsInsertWords(data2)
    final2 = data2.wsDP[-1]

    assert final1 == desiredOutput1
    assert final2 == desiredOutput2

@pytest.fixture
def fixtureFillChars():
    seed(0) #we use seed so we are able to know which chars to expect
    ws = [["a","",""],["","e",""],["g","","i"]]
    alphabet = ALPHABET
    desiredOutput = [["a","n","z"], ["o","e","b"], ["g","i","i"]]

    return (ws, alphabet, desiredOutput)

def test_FillChars(fixtureFillChars):
    ws, alphabet, desiredOutput = fixtureFillChars
    FillChars(ws, alphabet)
    
    assert ws == desiredOutput

@pytest.fixture
def fixtureWsToText():
    return [["a","b","c"],["d","e","f"],["g","h","i"]]

def test_WsToText(fixtureWsToText):
    str = WsToText(fixtureWsToText)
    assert str == "abc\ndef\nghi"

@pytest.fixture
def fixtureShowWSText(monkeypatch):
    ws = [["a","b","c"],["d","e","f"],["g","h","i"]]
    mock = OpenFile(f"{currentDir}/mock", "w+")
    #we change the print function, instead writing to the mock file, so we can easily read it's content
    monkeypatch.setattr("builtins.print", lambda str: mock.write(f"{str}\n"))
    yield (ws, mock)

    CloseFile(mock)
    remove(f"{currentDir}/mock")

def test_ShowWSText(fixtureShowWSText):
    ws, mock = fixtureShowWSText
    ShowWSText(WsToText(ws))
    mock.seek(0)
    output = mock.read()
    assert "--------------------------\nabc\ndef\nghi\n--------------------------\n" == output

@pytest.fixture
def fixtureSaveWS(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: f"{currentDir}/mock")
    yield [["a","b","c"],["d","e","f"],["g","h","i"]]

    remove(f"{currentDir}/mock")

def test_SaveWS(fixtureSaveWS):
    SaveWS(fixtureSaveWS)

    desiredOutput = "abc\ndef\nghi"
    with open(f"{currentDir}/mock", "r") as f:
        output = f.read()

    assert desiredOutput == output

@pytest.fixture
def fixtureRetWSData():
    file1 = OpenFile(f"{currentDir}/files/wsTest1.txt", "r")
    file2 = OpenFile(f"{currentDir}/files/wsTest3.txt", "r")
    file3 = OpenFile(f"{currentDir}/files/wsTest4.txt", "r")
    file4 = OpenFile(f"{currentDir}/files/wsTest5.txt", "r")
    desiredOutput = WsData(5, [Word("casa", Direction[2]), Word("arbol", Direction[1]),
                           Word("jorge", Direction[4]), Word("hola", Direction[5])])
    yield [file1, file2, file3, file4, desiredOutput]

    CloseFile(file1)
    CloseFile(file2)
    CloseFile(file3)
    CloseFile(file4)

def test_RetWSData(fixtureRetWSData):
    file1 = fixtureRetWSData.pop(0)
    file2 = fixtureRetWSData.pop(0)
    file3 = fixtureRetWSData.pop(0)
    file4 = fixtureRetWSData.pop(0)
    desiredOutput = fixtureRetWSData.pop(0)

    data1: WsData = RetWSData(file1)
    assert data1 == desiredOutput
    
    error = None

    try:
        RetWSData(file2)
    except Exception as e:
        error = e
    assert type(error) == WrongWSDataFormat and str(error) == "Dimension isn't numerical"
    
    try:
        RetWSData(file3)
    except Exception as e:
        error = e
    assert type(error) == WrongWSDataFormat and str(error) == "There wasn't any words in file"

    try:
        RetWSData(file4)
    except Exception as e:
        error = e
    assert type(error) == WrongWSDataFormat and str(error) == "Words contain a wrong formatted word or dir (non alpha word or non numeric dir)"

@pytest.fixture
def fixtureWordsValidation():
    seed(0) #to know which words will be chosen from the lexicon file as replace for the missing ones
    file = OpenFile(f"{currentDir}/files/lexicon.txt", "r")
    data = WsData(5, [Word("abc", Direction[0]), Word("hola", Direction[0]), Word("abcd", Direction[0])])
    yield (file, data)

    CloseFile(file)

def test_WordsValidation(fixtureWordsValidation):
    file, data = fixtureWordsValidation
    WordsValidation(file, data)

    assert data.words[0].string == "laconio" and data.words[0].dir == Direction[0]
    assert data.words[1].string == "hola" and data.words[1].dir == Direction[0]
    assert data.words[2].string == "melguizo" and data.words[2].dir == Direction[0]

@pytest.fixture
def fixtureLoadFilesData(monkeypatch):
    def _loadfilesdatainput():
        yield f"notfound.txt"
        yield f"notfound.txt"
        yield f"notfound.txt"
        yield f"notfound.txt"
        yield f"notfound.txt"
        yield f"notfound.txt"

        yield f"{currentDir}/files/lexicon.txt"
        yield f"{currentDir}/files/wsTest4.txt"

        yield f"{currentDir}/files/lexicon.txt"
        yield f"{currentDir}/files/wsTest2.txt"
    
    gen = _loadfilesdatainput()

    monkeypatch.setattr("builtins.input", lambda _: next(gen))

    seed(0)

    desiredOutput = WsData(6,
                          [Word("maria", Direction.LEFT), Word("cohete", Direction.DOWN), Word("tela", Direction.RIGHT),
                           Word("laconio", Direction.UP), Word("monitor", Direction.RIGHT)])
    
    return desiredOutput

def test_LoadFilesData(fixtureLoadFilesData):
    data1 = LoadFilesData()
    data2 = LoadFilesData()
    data3 = LoadFilesData()
    desiredOutput = fixtureLoadFilesData

    assert not data1
    assert not data2
    assert data3 == desiredOutput

@pytest.fixture
def fixtureWsMaker(monkeypatch):
    seed(0)

    def _wsmakerinput():
        yield f"{currentDir}/files/lexicon.txt"
        yield f"{currentDir}/files/wsTest1.txt"
        yield f"{currentDir}/files/wsTestOutput1.txt"

        yield f"{currentDir}/files/lexicon.txt"
        yield f"{currentDir}/files/wsTest2.txt"

    gen = _wsmakerinput()

    monkeypatch.setattr("builtins.input", lambda _: next(gen))

def test_WsMaker(fixtureWsMaker):
    flag1 = WsMaker()
    flag2 = WsMaker()

    with open(f"{currentDir}/files/wsTestOutput1.txt", "r") as f:
        testOutput = f.read()
    remove(f"{currentDir}/files/wsTestOutput1.txt")
    
    with open(f"{currentDir}/files/output1.txt", "r") as f:
        desiredOutput = f.read()

    assert flag1 and desiredOutput == testOutput
    assert not flag2