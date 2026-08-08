"""
Defines the Building class which wraps a visual Entity with metadata.
"""
from ursina import Entity, color, Vec3, Text

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
        
        # Create the actual physical representation in the world (Invisible Collider)
        self.entity = Entity(
            model='cube',
            scale=scale,
            color=color.rgba(0, 0, 0, 0),
            collider='box',
            position=position
        )
        
        # Create a visual root parented to the collider
        self.visual_root = Entity(parent=self.entity)
        
        # Store the explicit entrance position
        self.entrance_position = Vec3(*entrance_position)
        
        # Entrance Feedback: Add a subtle ground indicator
        # Y is 0.01 above ground to prevent z-fighting
        self.entrance_indicator = Entity(
            model='plane',
            color=color.rgba(1, 1, 1, 0.4), # Soft semi-transparent white (normalized 0-1)
            scale=(3, 1, 3), # A comfortable 3x3 standing pad
            position=(self.entrance_position.x, 0.01, self.entrance_position.z)
        )
        
        self.decorations = []
        self._build_visuals()

    def _build_visuals(self) -> None:
        """Adds category-specific 3D decorations and signage to the building."""
        # Add Walls (The main visible block)
        self.walls = Entity(parent=self.visual_root, model='cube', color=self.original_color, scale=(1, 1, 1), position=(0, 0, 0))
        self.decorations.append(self.walls)
        
        # Add Roof
        self.roof = Entity(parent=self.visual_root, model='cube', color=color.dark_gray, scale=(1.05, 0.1, 1.05), position=(0, 0.55, 0))
        self.decorations.append(self.roof)
        
        # Add Entrance Door
        self.door = Entity(parent=self.visual_root, model='cube', color=color.brown, scale=(0.2, 0.4, 0.05), position=(0, -0.3, -0.5))
        self.decorations.append(self.door)
        
        # Common Signage
        sign_text = Text(parent=self.visual_root, text=self.name.upper(), scale=3, origin=(0, 0), color=color.white, position=(0, 0.6, -0.55), z=-0.01, double_sided=True)
        self.decorations.append(sign_text)
        
        # Category specific decor
        if self.category == 'grammar':
            self.walls.color = color.rgb(180/255, 60/255, 60/255) # Brick red
            self.roof.color = color.white # White pitched roof style (represented as flat for simplicity, but distinct color)
            # Columns
            col1 = Entity(parent=self.visual_root, model='cylinder', color=color.white, scale=(0.1, 1, 0.1), position=(-0.4, 0, -0.55))
            col2 = Entity(parent=self.visual_root, model='cylinder', color=color.white, scale=(0.1, 1, 0.1), position=(0.4, 0, -0.55))
            # Windows
            win1 = Entity(parent=self.visual_root, model='cube', color=color.cyan, scale=(0.2, 0.3, 0.05), position=(-0.3, 0.1, -0.5))
            win2 = Entity(parent=self.visual_root, model='cube', color=color.cyan, scale=(0.2, 0.3, 0.05), position=(0.3, 0.1, -0.5))
            self.decorations.extend([col1, col2, win1, win2])
            
        elif self.category == 'vocabulary':
            self.walls.color = color.rgb(200/255, 180/255, 140/255) # Sandstone library
            # Stacked books on roof
            book1 = Entity(parent=self.visual_root, model='cube', color=color.rgb(180/255, 30/255, 30/255), scale=(0.4, 0.1, 0.3), position=(-0.2, 0.65, 0))
            book2 = Entity(parent=self.visual_root, model='cube', color=color.rgb(30/255, 30/255, 180/255), scale=(0.3, 0.1, 0.4), position=(0.1, 0.75, 0), rotation_y=20)
            # Large Windows
            win1 = Entity(parent=self.visual_root, model='cube', color=color.cyan, scale=(0.25, 0.5, 0.05), position=(-0.35, 0, -0.5))
            win2 = Entity(parent=self.visual_root, model='cube', color=color.cyan, scale=(0.25, 0.5, 0.05), position=(0.35, 0, -0.5))
            self.decorations.extend([book1, book2, win1, win2])
            
        elif self.category == 'listening':
            self.walls.color = color.rgb(100/255, 120/255, 140/255) # Tech gray-blue
            # Antenna
            base = Entity(parent=self.visual_root, model='cube', color=color.dark_gray, scale=(0.2, 0.2, 0.2), position=(0, 0.7, 0))
            pole = Entity(parent=self.visual_root, model='cylinder', color=color.gray, scale=(0.02, 0.5, 0.02), position=(0, 0.9, 0))
            dish = Entity(parent=self.visual_root, model='sphere', color=color.light_gray, scale=(0.3, 0.3, 0.1), position=(0, 1.1, 0), rotation_x=-20)
            # Windows
            win1 = Entity(parent=self.visual_root, model='cube', color=color.black, scale=(0.2, 0.2, 0.05), position=(-0.25, 0.1, -0.5))
            win2 = Entity(parent=self.visual_root, model='cube', color=color.black, scale=(0.2, 0.2, 0.05), position=(0.25, 0.1, -0.5))
            self.decorations.extend([base, pole, dish, win1, win2])
            
        elif self.category == 'reading':
            self.walls.color = color.rgb(139/255, 69/255, 19/255) # Warm wood/library
            self.door.scale = (0.4, 0.4, 0.05) # Wide entrance
            # Open book motif
            page1 = Entity(parent=self.visual_root, model='plane', color=color.white, scale=(0.3, 1, 0.4), position=(-0.15, 0.3, -0.51), rotation_x=-90, rotation_y=15)
            page2 = Entity(parent=self.visual_root, model='plane', color=color.white, scale=(0.3, 1, 0.4), position=(0.15, 0.3, -0.51), rotation_x=-90, rotation_y=-15)
            # Windows
            win1 = Entity(parent=self.visual_root, model='cube', color=color.cyan, scale=(0.15, 0.4, 0.05), position=(-0.35, 0, -0.5))
            win2 = Entity(parent=self.visual_root, model='cube', color=color.cyan, scale=(0.15, 0.4, 0.05), position=(0.35, 0, -0.5))
            self.decorations.extend([page1, page2, win1, win2])
            
        elif self.category == 'exam':
            self.walls.color = color.rgb(40/255, 40/255, 50/255) # Dark imposing marble
            self.roof.color = color.black
            self.door.color = color.rgb(218/255, 165/255, 32/255) # Gold door
            self.door.scale = (0.3, 0.5, 0.05) # Grand tall entrance
            # Grand Entrance Canopy
            canopy = Entity(parent=self.visual_root, model='cube', color=color.dark_gray, scale=(0.6, 0.1, 0.3), position=(0, 0.3, -0.65))
            c_leg1 = Entity(parent=self.visual_root, model='cylinder', color=color.gray, scale=(0.05, 0.8, 0.05), position=(-0.25, -0.1, -0.75))
            c_leg2 = Entity(parent=self.visual_root, model='cylinder', color=color.gray, scale=(0.05, 0.8, 0.05), position=(0.25, -0.1, -0.75))
            # Windows
            win1 = Entity(parent=self.visual_root, model='cube', color=color.black, scale=(0.2, 0.6, 0.05), position=(-0.3, 0.1, -0.5))
            win2 = Entity(parent=self.visual_root, model='cube', color=color.black, scale=(0.2, 0.6, 0.05), position=(0.3, 0.1, -0.5))
            self.decorations.extend([canopy, c_leg1, c_leg2, win1, win2])

    def set_lock_state(self, is_locked: bool) -> None:
        """
        Updates the building's visual state based on lock status.
        Locked buildings are darkened.
        """
        if self.is_locked == is_locked:
            return
            
        self.is_locked = is_locked
        if is_locked:
            self.walls.color = color.dark_gray
        else:
            self.walls.color = self.original_color

    def set_active_highlight(self, is_active: bool) -> None:
        """
        Highlights the building entrance if it is the active quest target.
        """
        if is_active:
            self.entrance_indicator.color = color.rgba(1, 0.84, 0, 0.8) # Brighter yellow/gold (normalized)
        else:
            self.entrance_indicator.color = color.rgba(1, 1, 1, 0.4) # Default soft white (normalized)
