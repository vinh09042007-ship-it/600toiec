"""
Handles movement calculation and application for the Player entity.
"""
from typing import Tuple, TYPE_CHECKING
from .player import Player

if TYPE_CHECKING:
    from .collision import PlayerCollision

class PlayerMovement:
    """
    Calculates velocity and updates the position of the Player entity 
    based on the provided input vector.
    Operates entirely decoupled from input hardware reading or world physics.
    """
    
    def __init__(self, player: Player, collision_system: 'PlayerCollision') -> None:
        """
        Initializes the movement system.
        
        Args:
            player (Player): The player entity to modify.
            collision_system (PlayerCollision): The collision system to check path clearance.
        """
        self.player = player
        self.collision_system = collision_system

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
            # Update the forward direction facing vector FIRST
            # This ensures the player always faces the input direction even if blocked
            self.player.set_forward(x, y, z)
            
            # Determine how far the player wants to move
            distance = self.player.speed * delta_time
            
            # Ask the CollisionSystem if the path is clear
            if self.collision_system.can_move((x, y, z), distance):
                # Calculate displacement based on speed and delta_time
                displacement_x = x * distance
                displacement_y = y * distance
                displacement_z = z * distance
                
                # Retrieve current position
                current_x, current_y, current_z = self.player.position
                
                # Apply displacement to get the new position
                new_x = current_x + displacement_x
                new_y = current_y + displacement_y
                new_z = current_z + displacement_z
                self.player.position = (new_x, new_y, new_z)
                
                # Update logical state
                self.player.state = "RUNNING"
            else:
                # Path is blocked
                self.player.state = "IDLE"
        else:
            self.player.state = "IDLE"
