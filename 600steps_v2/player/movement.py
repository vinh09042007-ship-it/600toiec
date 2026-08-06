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

    def calculate_desired_position(self, move_vector: Tuple[float, float, float], delta_time: float) -> Tuple[float, float, float]:
        """
        Calculates the new position based on input. Does NOT modify the player's position.
        
        Args:
            move_vector (Tuple[float, float, float]): The normalized direction vector (x, y, z).
            delta_time (float): The time elapsed since the last frame.
            
        Returns:
            Tuple[float, float, float]: The desired new (x, y, z) position.
        """
        x, y, z = move_vector
        
        # Determine if the player is currently moving
        is_moving = (x != 0.0 or y != 0.0 or z != 0.0)
        self.player.is_moving = is_moving
        
        if is_moving:
            # Update the forward direction facing vector FIRST
            # This ensures the player always faces the input direction even if blocked
            self.player.set_forward(x, y, z)
            
            # Determine how far the player wants to move
            distance = self.player.speed * delta_time
            
            # Calculate displacement
            displacement_x = x * distance
            displacement_y = y * distance
            displacement_z = z * distance
            
            # Retrieve current position
            current_x, current_y, current_z = self.player.position
            
            # Return desired position
            return (current_x + displacement_x, current_y + displacement_y, current_z + displacement_z)
            
        # If not moving, desired position is current position
        return self.player.position
