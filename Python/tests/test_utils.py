import pytest #we use pytest to run our test cases
from pathlib import Path #used to get the absolute path, to search for files
from os import remove #remove files (e.g. mockups)

from Python.src.utils import (OpenFile, CloseFile, FileJumpToLine,
                              BinarySearch, SaveFile) #functions tested in this file

currentDir = Path(__file__).resolve().parent.as_posix()
"""Absolute path of the parent directory of this file."""

#we use pytest.fixture decorator to prepare the necessary files, mockups, classes, etc.
#for a test to use, and then cleanup, free resources, files, etc.
#we also use monkeypatch to change the behaviour of certain functions, without having to
#reset this changes again when the test ends 

#a fixture will wrap a test function if passed as an argument to it
#all the code before a yield will execute before the test (preparation), and the code after the yield will execute
#when the test ends (cleanup)
@pytest.fixture
def fixtureOpenFile(monkeypatch): #we pass monkeypatch as an argument, to use it in the fixture
    #we define a generator function (yield keyword), used to mockup the user input
    #we then save it in gen (important to save state between calls)
    #and use next(gen) to produce each yielded value one at a time
    def _openfileinput():
        yield f"{currentDir}/files"
        yield f"{currentDir}"
        yield f"{currentDir}/files/file"
        yield f"{currentDir}/files/file2"

    gen = _openfileinput()

    #then, we use monkeypatch to change the behaviour of the input function, to mockup a user input
    #when the test ends, monkeypatch will take care of resetting the input function properly
    #although we could do this manually, monkeypatch ensures there's no problems between tests
    monkeypatch.setattr("builtins.input", lambda _: next(gen))

def test_OpenFile(fixtureOpenFile): #we pass the fixture as an argument, so pytest executes it properly
    #OpenFile will ask for user input using the input() function, but it's patched and will return the input we prepared
    with (OpenFile(f"{currentDir}/files/file1", "r") as f):
        content1 = f.read()

    with (OpenFile("", "r") as f):
        content2 = f.read()

    #a pytest test will success if all asserts evaluate to True
    assert content1 == ""
    assert content2 == "Hello World"

@pytest.fixture
def fixtureCloseFile():
    #we can also use the fixture return value, in this case it's a file
    return OpenFile(f"{currentDir}/files/file1", "r")

def test_CloseFile(fixtureCloseFile):
    #we try to close the file returned by fixtureCloseFile
    ret1 = CloseFile(None)
    ret2 = CloseFile(fixtureCloseFile)
    ret3 = CloseFile(fixtureCloseFile)

    assert not ret1
    assert ret2
    assert ret3

@pytest.fixture
def fixtureFileJumpToLine():
    #in this case, we open a file, yield it (which serves as a return value) and then close it
    #pytest will run the fixture, yield the file, and when the test ends, continue execution to close the file
    f = OpenFile(f"{currentDir}/files/file3", "r")
    yield f
    CloseFile(f)

def test_FileJumpToLine(fixtureFileJumpToLine):
    f = fixtureFileJumpToLine
    str1 = FileJumpToLine(f, "HELLO")
    str2 = FileJumpToLine(f, "lorem ipsum")
    str3 = FileJumpToLine(f, "")
    str4 = FileJumpToLine(f, "")

    assert str1 == "HELLO"
    assert str2 == "lorem ipsum"
    assert str3 == "abcd"
    assert str4 == ""

@pytest.fixture
def fixtureBinarySearch():
    return ([1,2,3,4,5], [], ["a","b","c"])

def test_BinarySearch(fixtureBinarySearch):
    l1, l2, l3 = fixtureBinarySearch

    assert BinarySearch(l1, 1)
    assert not BinarySearch(l1, 6)
    assert not BinarySearch(l2, 5)
    assert BinarySearch(l3, "c")
    assert not BinarySearch(l3, "ab")

@pytest.fixture
def fixtureSaveFile(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")

    return ("HELLO\nWORLD", f"{currentDir}/files/savefile1", f"{currentDir}")

def test_SaveFile(fixtureSaveFile):
    str, path1, path2 = fixtureSaveFile
    flag1 = SaveFile(str, path1)
    flag2 = SaveFile("", path2)

    with OpenFile(path1, "r") as f:
        content = f.read()
    remove(path1) #we remove any created files in tests

    assert content == str and flag1
    assert not flag2