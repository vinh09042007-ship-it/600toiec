"""
The main open-world campus scene.
"""
from ursina import Sky, camera
from .base_scene import BaseScene
from world.campus import Campus
from world.collision import WorldCollision
from player.controller import PlayerController
from player.camera import PlayerCamera
from world.interaction import InteractionManager
import utils.constants as const

class CampusScene(BaseScene):
    """
    Manages the logic and objects for the main Campus environment.
    """
    
    def __init__(self, scene_manager, **kwargs):
        self.scene_manager = scene_manager
        super().__init__(**kwargs)
        
    def setup(self) -> None:
        """Initialize all campus-related systems."""
        # Visual environment
        self.sky = Sky(parent=self)
        self.campus = Campus()
        
        # Parent all campus entities to this scene so they auto-hide
        for entity in self.campus.entities:
            entity.parent = self
            
        # Systems
        self.world_collision = WorldCollision(self.campus.obstacles)
        
        self.player_controller = PlayerController(
            speed=const.PLAYER_SPEED, 
            world_collision=self.world_collision
        )
        self.player_controller.player.parent = self
        
        self.player_camera = PlayerCamera(self.player_controller.player)
        
        self.interaction_manager = InteractionManager(self.player_controller.player, self.campus)
        # Setup callback for interaction
        self.interaction_manager.on_interact = self._on_building_interact

    def _on_building_interact(self, building_name: str) -> None:
        """Callback triggered when the player interacts with a building."""
        self.scene_manager.switch_scene("building", building_name=building_name)

    def on_enter(self, **kwargs) -> None:
        """Called when entering the campus."""
        # Restore camera settings if they were changed
        pass
        
    def update_scene(self, delta_time: float) -> None:
        """Update systems every frame."""
        self.player_controller.update(delta_time)
        self.player_camera.update(delta_time)
        self.interaction_manager.update()

    def on_exit(self) -> None:
        """Called when leaving the campus."""
        # Ensure UI prompt is hidden
        self.interaction_manager.prompt.enabled = False
