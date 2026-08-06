"""
Handles collision detection for the player.
"""
from typing import Tuple
from ursina import raycast, Vec3
from .player import Player

class PlayerCollision:
    """
    Detects obstacles ahead of the player using raycasting.
    Operates independently of movement application logic.
    """
    
    def __init__(self, player: Player) -> None:
        """
        Initializes the collision system.
        
        Args:
            player (Player): The player entity to use as the raycast origin.
        """
        self.player = player
        
    def can_move(self, direction: Tuple[float, float, float], distance: float) -> bool:
        """
        Checks if the player can move in the given direction for the given distance.
        
        Args:
            direction (Tuple[float, float, float]): The normalized direction vector.
            distance (float): The distance the player intends to move.
            
        Returns:
            bool: True if the path is clear, False if an obstacle is detected.
        """
        x, y, z = direction
        if x == 0.0 and y == 0.0 and z == 0.0:
            return True
            
        # Raycast from player center (offset Y slightly to avoid ground collision)
        origin = self.player.position + Vec3(0, 0.5, 0)
        dir_vec = Vec3(x, y, z).normalized()
        
        hit_info = raycast(
            origin=origin,
            direction=dir_vec,
            distance=distance + 0.6,  # Player half-width (0.5) + small buffer
            ignore=(self.player,)
        )
        
        return not hit_info.hit
