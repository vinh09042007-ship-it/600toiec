"""
Defines the Building class which wraps a visual Entity with metadata.
"""
from ursina import Entity, color, Vec3

class Building:
    """
    Represents a specific building on the campus.
    Stores both the visual Entity and interaction metadata.
    """
    
    def __init__(self, name: str, category: str, position: tuple[float, float, float], 
                 scale: tuple[float, float, float], building_color: color, 
                 entrance_position: tuple[float, float, float]) -> None:
        """
        Initialize the building and its corresponding 3D Entity.
        
        Args:
            name (str): The display name of the building (e.g., 'Vocabulary').
            category (str): The logic category of the building.
            position (tuple): X, Y, Z coordinates.
            scale (tuple): Width, Height, Depth scale.
            building_color (color): Ursina color for the entity.
            entrance_position (tuple): X, Y, Z coordinates for the entrance.
        """
        self.name = name
        self.category = category
        self.original_color = building_color
        self.is_locked = False
        
        # Create the actual physical representation in the world
        self.entity = Entity(
            model='cube',
            scale=scale,
            color=building_color,
            collider='box',
            position=position
        )
        
        # Store the explicit entrance position
        self.entrance_position = Vec3(*entrance_position)
        
        # Entrance Feedback: Add a subtle ground indicator
        # Y is 0.01 above ground to prevent z-fighting
        self.entrance_indicator = Entity(
            model='plane',
            color=color.rgba(255, 255, 255, 100), # Soft semi-transparent white
            scale=(3, 1, 3), # A comfortable 3x3 standing pad
            position=(self.entrance_position.x, 0.01, self.entrance_position.z)
        )

    def set_lock_state(self, is_locked: bool) -> None:
        """
        Updates the building's visual state based on lock status.
        Locked buildings are darkened.
        """
        if self.is_locked == is_locked:
            return
            
        self.is_locked = is_locked
        if is_locked:
            self.entity.color = color.dark_gray
        else:
            self.entity.color = self.original_color

    def set_active_highlight(self, is_active: bool) -> None:
        """
        Highlights the building entrance if it is the active quest target.
        """
        if is_active:
            self.entrance_indicator.color = color.rgba(255, 215, 0, 200) # Brighter yellow/gold
        else:
            self.entrance_indicator.color = color.rgba(255, 255, 255, 100) # Default soft white
