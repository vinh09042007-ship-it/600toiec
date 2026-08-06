"""
Handles user input for the player entity.
"""
from typing import Tuple
from ursina import held_keys

class PlayerInput:
    """
    Reads and processes raw input from the user (keyboard/mouse).
    Provides processed data (like movement vectors or interaction flags) 
    for the PlayerController to query.
    Does not modify any game state directly.
    """
    
    def get_move_vector(self) -> Tuple[float, float, float]:
        """
        Calculates the movement direction based on WASD keys.
        
        Returns:
            Tuple[float, float, float]: The normalized (x, y, z) movement vector.
        """
        # Get raw input axes
        x: float = float(held_keys.get('d', 0) - held_keys.get('a', 0))
        z: float = float(held_keys.get('w', 0) - held_keys.get('s', 0))
        y: float = 0.0
        
        # Normalize the vector to prevent faster diagonal movement
        if x != 0.0 or z != 0.0:
            length = (x**2 + z**2) ** 0.5
            x /= length
            z /= length
            
        return (x, y, z)

    def is_interact_pressed(self) -> bool:
        """
        Checks if the interaction key (E) is currently pressed.
        
        Returns:
            bool: True if 'e' is pressed, False otherwise.
        """
        return bool(held_keys.get('e', 0))
