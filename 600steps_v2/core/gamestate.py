"""
Game state enumerations.
"""
from enum import Enum, auto

class GameState(Enum):
    """Represents the various states the game can be in."""
    MENU = auto()
    INTRO = auto()
    PLAYING = auto()
    PAUSED = auto()
    QUIZ = auto()
    RESULT = auto()
    EXIT = auto()
