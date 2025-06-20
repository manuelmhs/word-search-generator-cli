#all imports used to improve readability
from enum import Enum, EnumMeta
from dataclasses import dataclass, field
from typing import NamedTuple, TypeAlias

class EnumByIndexMeta(EnumMeta):
    """Enum metaclass to support item access by (integer) index in our Enums."""
    #we create a new metaclass that inherits from EnumMeta (the default metaclass for Enum type)
    #then we use this metaclass to create any Enum class that we want to support access by index
    #every python class is an object, and this classes are created using a metaclass (a class for classes)

    #we override the 'new' method in the metaclass, to change the behaviour when a new Enum is created
    def __new__(cls, name, bases, dict):
        #we first use the new method of EnumMeta, so obj is the new Enum recently created as default by Python
        obj = super().__new__(cls, name, bases, dict)

        #we then give our Enum a class variable _dirlist set to tuple(obj),
        #which returns the tuple of all the Enum values in the order declared in the Enum
        cls._dirlist = tuple(obj)
        return obj
    
    #now we override the 'getitem' class method of our Enum by defining it in our metaclass
    def __getitem__(cls, key):
        #we look for a valid integer in our _dirlist
        if (isinstance(key, int) and key >= 0 and key < len(cls._dirlist)):
            return cls._dirlist[key]
        #or use the default getitem method of Enum
        else:
            return super().__getitem__(key)

class DIR(NamedTuple):
    """
    Represents the direction a word is written in the word search.

    Supports access by field name, e.g. dir.x, dir.y.
    """
    x: int
    y: int

class Direction(Enum, metaclass=EnumByIndexMeta):
    """
    Enum that contains all the possible directions for the words to be written.
    
    Supports access by index, e.g. Direction.RIGHT == Direction[0].
    """
    RIGHT: DIR = DIR(1, 0)
    LEFT: DIR = DIR(-1, 0)
    DOWN: DIR = DIR(0, 1)
    UP: DIR = DIR(0, -1)
    RIGHTDOWN: DIR = DIR(1, 1)
    RIGHTUP: DIR = DIR(1, -1)
    LEFTDOWN: DIR = DIR(-1, 1)
    LEFTUP: DIR = DIR(-1, -1)

#we use dataclasses bacause they provide certain utilities (e.g. init method and fields)
#and also to make the intention of our code more clear
@dataclass
class Word:
    """Dataclass that contains all the data and auxiliary structures associated to a word for our word search."""
    #dataclasses use field to set default values if they are not provided when creating the class
    #important: if a variable type is mutable, then we must use default_factory (e.g. list), otherwise, the same list instance would be shared
    #across all the instances

    string: str = field(default=None)
    """String of the word."""
    dir: Direction = field(default=None)
    """Direction (Enum) in which the word must be written in the word search."""
    positions: list[tuple[int, int]] = field(default_factory=list)
    """Possible (x,y) indexes (coordinates) to start writing the word in an empty word search.
    
    Must contain exactly all (x,y) coordinates, which are the starting positions of the word, without going out of
    boundaries, taking in consideration the word's length, word's direction and ws dimension."""
    positionsIndex: tuple[int, int] = field(default=None)
    """Auxiliary data for the backtracking algorithm.
    
    It's a tuple (i, j) where i is the current position index (used in the algorithm) and j is the maximum index available in the positions list."""

ws: TypeAlias = list[list[str]]
"""We represent a word search like a list of list of str, this is, a 2d array of chars."""

@dataclass
class WsData:
    """Dataclass that contains all the data necessary to generate our word search."""
    
    dimension: int = field(default=None)
    """Dimension of the word search (generates a square of dimension x dimension)."""
    words: list[Word] = field(default_factory=list)
    """List of all the words and their data to put in the word search."""
    wsDP: list[ws] = field(default_factory=list)
    """Auxiliary struct for the algorithm (we use a list of ws structs, using a new one as we fill in a new word)."""