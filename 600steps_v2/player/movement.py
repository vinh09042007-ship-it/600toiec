"""
Handles movement calculation and application for the Player entity.
"""
from typing import Tuple
from .player import Player

class PlayerMovement:
    """
    Calculates velocity and updates the position of the Player entity 
    based on the provided input vector.
    Operates entirely decoupled from input hardware reading or world physics.
    """
    
    def __init__(self, player: Player) -> None:
        """
        Initializes the movement system.
        
        Args:
            player (Player): The player entity to modify.
        """
        self.player = player

    def move(self, move_vector: Tuple[float, float, float], delta_time: float) -> None:
        """
        Applies the movement vector to the player's position.
        
        Args:
            move_vector (Tuple[float, float, float]): The normalized direction vector (x, y, z).
            delta_time (float): The time elapsed since the last frame.
        """
        x, y, z = move_vector
        
        # Determine if the player is currently moving
        is_moving = (x != 0.0 or y != 0.0 or z != 0.0)
        self.player.is_moving = is_moving
        
        if is_moving:
            # Calculate displacement based on speed and delta_time
            displacement_x = x * self.player.speed * delta_time
            displacement_y = y * self.player.speed * delta_time
            displacement_z = z * self.player.speed * delta_time
            
            # Retrieve current position
            current_x, current_y, current_z = self.player.position
            
            # Apply displacement to get the new position
            new_x = current_x + displacement_x
            new_y = current_y + displacement_y
            new_z = current_z + displacement_z
            self.player.position = (new_x, new_y, new_z)
            
            # Update the forward direction facing vector
            self.player.set_forward(x, y, z)
            
            # Update logical state
            self.player.state = "RUNNING"
        else:
            self.player.state = "IDLE"
