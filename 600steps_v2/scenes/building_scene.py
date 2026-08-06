"""
A generic placeholder scene for inside buildings.
"""
from ursina import Entity, Text, color, held_keys, camera, Vec3
from .base_scene import BaseScene

class BuildingScene(BaseScene):
    """
    Placeholder scene showing a simple interior.
    """
    
    def __init__(self, scene_manager, **kwargs):
        self.scene_manager = scene_manager
        super().__init__(**kwargs)
        
    def setup(self) -> None:
        # Room Dimensions
        room_size = 20
        wall_height = 8
        wall_thickness = 1
        
        # Simple floor
        self.floor = Entity(
            parent=self,
            model='plane',
            scale=(room_size, 1, room_size),
            color=color.dark_gray,
            position=(0, 0, 0)
        )
        
        # Four walls
        # North wall (Front)
        Entity(parent=self, model='cube', color=color.gray, 
               scale=(room_size, wall_height, wall_thickness), 
               position=(0, wall_height/2, room_size/2))
        # South wall (Back)
        Entity(parent=self, model='cube', color=color.gray, 
               scale=(room_size, wall_height, wall_thickness), 
               position=(0, wall_height/2, -room_size/2))
        # East wall (Right)
        Entity(parent=self, model='cube', color=color.gray, 
               scale=(wall_thickness, wall_height, room_size), 
               position=(room_size/2, wall_height/2, 0))
        # West wall (Left)
        Entity(parent=self, model='cube', color=color.gray, 
               scale=(wall_thickness, wall_height, room_size), 
               position=(-room_size/2, wall_height/2, 0))
               
        # Descriptions Configuration
        self.descriptions = {
            "Vocabulary": "Practice English vocabulary.",
            "Grammar": "Practice grammar questions.",
            "Listening": "Practice listening exercises.",
            "Reading": "Practice reading comprehension.",
            "Exam": "Start a full TOEIC simulation."
        }
        
        # UI Texts
        self.title_text = Text(
            text="Building Name",
            position=(0, 0.25),
            origin=(0, 0),
            scale=3,
            color=color.white,
            parent=self
        )
        
        self.desc_text = Text(
            text="Building Description",
            position=(0, 0.15),
            origin=(0, 0),
            scale=1.5,
            color=color.light_gray,
            parent=self
        )
        
        self.instruction_text = Text(
            text="ENTER to Start\nESC to Return",
            position=(0, -0.2),
            origin=(0, 0),
            scale=1.5,
            color=color.white,
            parent=self
        )
        
        # Debounce for enter key
        self.was_enter_pressed = False
        
        self.building_name = ""

    def on_enter(self, **kwargs) -> None:
        """
        Setup state for the specific building entered.
        """
        self.building_name = kwargs.get("building_name", "Unknown")
        self.title_text.text = f"{self.building_name} Building"
        self.desc_text.text = self.descriptions.get(self.building_name, "Welcome.")
        
        # We must detach the UI elements from the 3D scene and attach to UI camera so they render as 2D Text
        from ursina import camera
        self.title_text.parent = camera.ui
        self.desc_text.parent = camera.ui
        self.instruction_text.parent = camera.ui
        
        self.was_enter_pressed = True # Prevent accidental immediate trigger
        
        # Override camera
        self.old_fov = camera.fov
        camera.fov = 60
        camera.position = (0, 15, -15)
        camera.look_at((0, 0, 0))
        
    def update_scene(self, delta_time: float) -> None:
        """Handle input inside the building."""
        # Handle Return
        if held_keys['escape']:
            self.scene_manager.switch_scene("campus")
            
        # Handle Start Interaction
        is_enter_pressed = held_keys['enter']
        if is_enter_pressed and not self.was_enter_pressed:
            self.scene_manager.switch_scene("question", building_name=self.building_name)
        self.was_enter_pressed = is_enter_pressed

    def on_exit(self) -> None:
        """Cleanup and restore previous camera settings."""
        # Reparent UI texts back to self so they hide with the scene
        self.title_text.parent = self
        self.desc_text.parent = self
        self.instruction_text.parent = self
        
        # Restore camera FOV (Position and rotation will be handled by PlayerCamera in CampusScene)
        camera.fov = self.old_fov
