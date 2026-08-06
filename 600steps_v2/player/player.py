"""
Defines the Player entity and its data structure.
"""
from typing import Tuple
from ursina import Entity, color

class Player(Entity):
    """
    The main player entity.
    Acts as a data container for the player's physical and logical state,
    and inherits from Ursina's Entity to represent the 3D model.
    """
    
    def __init__(self, speed: float) -> None:
        """
        Initialize the player with essential attributes and visual representation.
        
        Args:
            speed (float): The base movement speed of the player.
        """
        super().__init__(
            model="cube",
            color=color.azure,
            scale=(1, 2, 1),
            collider="box",
            position=(0, 1, 0)
        )
        self.speed: float = speed
        
        # Logical states
        self.state: str = "IDLE"
        self.is_moving: bool = False



    def get_forward(self) -> Tuple[float, float, float]:
        """
        Retrieve the current forward direction vector.
        
        Returns:
            Tuple[float, float, float]: The (x, y, z) direction vector.
        """
        return (self.forward.x, self.forward.y, self.forward.z)

    def set_forward(self, x: float, y: float, z: float) -> None:
        """
        Update the player's forward direction vector.
        Rotates the model to face the moving direction.
        
        Args:
            x (float): X direction component.
            y (float): Y direction component.
            z (float): Z direction component.
        """
        # In Ursina, look_at points the entity towards a target coordinate
        if x != 0.0 or y != 0.0 or z != 0.0:
            target_pos = self.position + (x, y, z)
            self.look_at(target_pos)
