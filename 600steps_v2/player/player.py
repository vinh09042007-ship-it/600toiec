"""
Defines the Player entity and its data structure.
"""
import os
import math
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
            color=color.clear, # Completely invisible collider
            scale=(1, 2, 1),
            collider="box",
            position=(0, 1, 0)
        )
        self.speed: float = speed
        
        # 4. Create intermediate pivot to counteract the Player root's (1, 2, 1) scale 
        # and adjust the model's feet to the bottom of the bounding box.
        self.model_pivot = Entity(
            parent=self,
            scale=(1, 0.5, 1), # Counteract parent's Y scale of 2
            position=(0, -0.5, 0) # Base of the box (local y=-0.5 corresponds to world y=0)
        )
        
        # 5. Load the OBJ model and explicitly assign texture
        model_path = 'assets/models/player/base.obj'
        texture_path = 'assets/models/player/texture_diffuse.png'
        
        # Logging safety checks
        print(f"[PlayerVisual] Loading model: {model_path} (Exists: {os.path.exists(model_path)})")
        print(f"[PlayerVisual] Loading texture: {texture_path} (Exists: {os.path.exists(texture_path)})")
        
        self.model_visual = Entity(
            parent=self.model_pivot,
            model=model_path,
            texture=texture_path,
            color=color.white, # Neutral multiplier to prevent overriding texture colors
            double_sided=True, # Prevent invisible backfaces
            rotation=(0, 180, 0), # Start with 180 based on standard character forward axis
            scale=1.12 # Slightly larger player visual (~12%)
        )
        print(f"[PlayerVisual] Model visual entity created successfully.")
        
        # Logical states
        self.state: str = "IDLE"
        self.is_moving: bool = False
        
        # Physics states
        self.vertical_velocity: float = 0.0
        self.is_grounded: bool = False



    def get_forward(self) -> Tuple[float, float, float]:
        """
        Retrieve the current visual forward direction vector.
        
        Returns:
            Tuple[float, float, float]: The (x, y, z) direction vector of the visual model.
        """
        return (self.model_pivot.forward.x, self.model_pivot.forward.y, self.model_pivot.forward.z)

    def set_forward(self, x: float, y: float, z: float) -> None:
        """
        Update the player's visual facing direction vector.
        Rotates ONLY the visual model pivot to face the moving direction horizontally.
        
        Args:
            x (float): X direction component.
            y (float): Y direction component.
            z (float): Z direction component.
        """
        if x != 0.0 or z != 0.0:
            # Calculate the horizontal yaw angle in degrees
            target_y_rotation = math.degrees(math.atan2(x, z))
            
            # MODEL_YAW_OFFSET corrects the native model orientation
            MODEL_YAW_OFFSET = 180
            
            # Rotate ONLY the visual model pivot, not the Player root.
            # This ensures the collision box stays upright and the model never pitches/rolls into the ground.
            self.model_pivot.rotation_y = target_y_rotation + MODEL_YAW_OFFSET


