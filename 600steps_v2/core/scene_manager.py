"""
Manages scene transitions and lifecycles.
"""
from typing import Dict, Any

class SceneManager:
    """
    Handles registering, switching, and updating game scenes.
    """
    
    def __init__(self, player_profile) -> None:
        """Initialize the SceneManager."""
        self.scenes: Dict[str, Any] = {}
        self.active_scene = None
        self.player_profile = player_profile

    def register_scene(self, name: str, scene) -> None:
        """
        Registers a scene instance under a specific name.
        
        Args:
            name (str): The name identifier for the scene.
            scene (BaseScene): The scene instance.
        """
        self.scenes[name] = scene
        # Ensure all scenes are disabled initially
        scene.disable()

    def switch_scene(self, name: str, **kwargs) -> None:
        """
        Switches the active scene to the requested scene.
        
        Args:
            name (str): The name of the scene to switch to.
            **kwargs: Additional arguments to pass to the new scene.
        """
        if name not in self.scenes:
            print(f"Error: Scene '{name}' not found!")
            return
            
        print(f"Switching to scene: {name}")
        
        # Exit the current scene
        if self.active_scene:
            self.active_scene.on_exit()
            self.active_scene.disable()
            
        # Enter the new scene
        print(f"[TRACE] SceneManager: Enabling scene {name}")
        self.active_scene = self.scenes[name]
        self.active_scene.enable()
        print(f"[TRACE] SceneManager: Calling on_enter for {name}")
        self.active_scene.on_enter(**kwargs)
        print(f"[TRACE] SceneManager: on_enter returned for {name}")

    def update(self, delta_time: float) -> None:
        """
        Updates the currently active scene.
        
        Args:
            delta_time (float): The time elapsed since the last frame.
        """
        if self.active_scene:
            self.active_scene.update_scene(delta_time)
