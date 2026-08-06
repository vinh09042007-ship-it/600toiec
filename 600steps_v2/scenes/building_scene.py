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
        """Initialize the generic interior."""
        # Simple floor
        self.floor = Entity(
            parent=self,
            model='plane',
            scale=(20, 1, 20),
            color=color.dark_gray,
            position=(0, 0, 0)
        )
        
        # UI Text
        self.title_text = Text(
            text="Inside Building",
            position=(0, 0.2),
            origin=(0, 0),
            scale=3,
            color=color.white,
            parent=self
        )
        
        self.instruction_text = Text(
            text="Press ESC to return.",
            position=(0, 0.1),
            origin=(0, 0),
            scale=1.5,
            color=color.light_gray,
            parent=self
        )
        
        self.building_name = ""

    def on_enter(self, **kwargs) -> None:
        """
        Setup state for the specific building entered.
        """
        self.building_name = kwargs.get("building_name", "Unknown")
        self.title_text.text = f"Inside {self.building_name}"
        
        # We must detach the UI elements from the 3D scene and attach to UI camera so they render as 2D Text
        from ursina import camera
        self.title_text.parent = camera.ui
        self.instruction_text.parent = camera.ui
        
        # Override camera
        self.old_fov = camera.fov
        camera.fov = 60
        camera.position = (0, 15, -15)
        camera.look_at((0, 0, 0))
        
    def update_scene(self, delta_time: float) -> None:
        """Handle input to leave the scene."""
        if held_keys['escape']:
            self.scene_manager.switch_scene("campus")

    def on_exit(self) -> None:
        """Cleanup and restore previous camera settings."""
        # Reparent UI texts back to self so they hide with the scene
        self.title_text.parent = self
        self.instruction_text.parent = self
        
        # Restore camera FOV (Position and rotation will be handled by PlayerCamera in CampusScene)
        camera.fov = self.old_fov
