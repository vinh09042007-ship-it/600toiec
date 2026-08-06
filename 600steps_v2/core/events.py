"""
Defines all global events for the game using an Enum.
"""
from enum import Enum, auto

class Events(Enum):
    """Enumeration of all possible game events."""
    APP_START = auto()
    APP_EXIT = auto()
    
    PLAYER_MOVE = auto()
    PLAYER_STOP = auto()
    PLAYER_INTERACT = auto()
    
    NPC_INTERACT = auto()
    
    QUEST_ACCEPTED = auto()
    QUEST_COMPLETED = auto()
    BUILDING_UNLOCKED = auto()
    
    QUIZ_OPEN = auto()
    QUIZ_START = auto()
    QUIZ_FINISH = auto()
    
    SAVE_GAME = auto()
    LOAD_GAME = auto()
    
    GAME_STATE_CHANGED = auto()
