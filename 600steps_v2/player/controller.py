"""
Defines the PlayerController to handle player logic and lifecycle.
"""
from typing import Tuple
from .player import Player
from .input import PlayerInput
from .movement import PlayerMovement

class PlayerController:
    """
    Manages the Player entity.
    Coordinates input processing and movement logic per frame.
    """
    
    def __init__(self, speed: float) -> None:
        """
        Initialize the controller and its subsystems.
        
        Args:
            speed (float): Base speed injected into the Player.
        """
        self.player: Player = Player(speed=speed)
        self.input_system: PlayerInput = PlayerInput()
        self.movement_system: PlayerMovement = PlayerMovement(self.player)

    def update(self, delta_time: float) -> None:
        """
        Update the player logic once per frame.
        
        Args:
            delta_time (float): The time elapsed since the last frame.
        """
        # Step 1: Read user input (pure data)
        move_vector = self.input_system.get_move_vector()
        
        # Step 2: Pass data to movement system for state modification
        self.movement_system.move(move_vector, delta_time)

    def get_player_position(self) -> Tuple[float, float, float]:
        """
        Convenience method to retrieve the player's current position.
        
        Returns:
            Tuple[float, float, float]: The (x, y, z) coordinates.
        """
        return self.player.position
