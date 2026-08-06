"""
Handles collision detection against world boundaries and obstacles.
"""
from typing import List
from ursina import Entity
import utils.constants as const

class WorldCollision:
    """
    Validates if a given position is within world bounds and outside obstacles.
    Designed to be reusable for any entity, not just the player.
    """
    
    def __init__(self, obstacles: List[Entity]) -> None:
        """
        Initializes the collision system with the world's static obstacles.
        
        Args:
            obstacles (List[Entity]): Entities that act as solid walls.
        """
        self.obstacles = obstacles
        self.radius = const.PLAYER_RADIUS
        self.border = const.WORLD_BORDER

    def is_position_valid(self, new_x: float, new_z: float) -> bool:
        """
        Checks if the desired X, Z position is valid (no collision).
        
        Args:
            new_x (float): The desired X coordinate.
            new_z (float): The desired Z coordinate.
            
        Returns:
            bool: True if the position is free, False if blocked.
        """
        # 1. Check world boundaries
        if not (-self.border <= new_x <= self.border):
            return False
        if not (-self.border <= new_z <= self.border):
            return False
            
        # 2. Check obstacles (AABB mathematical intersection)
        for obs in self.obstacles:
            obs_x, _, obs_z = obs.position
            obs_sx, _, obs_sz = obs.scale
            
            # Calculate obstacle bounds
            min_x = obs_x - (obs_sx / 2.0) - self.radius
            max_x = obs_x + (obs_sx / 2.0) + self.radius
            min_z = obs_z - (obs_sz / 2.0) - self.radius
            max_z = obs_z + (obs_sz / 2.0) + self.radius
            
            # Check if the point (new_x, new_z) falls inside the obstacle's expanded bounding box
            if min_x < new_x < max_x and min_z < new_z < max_z:
                return False
                
        return True
