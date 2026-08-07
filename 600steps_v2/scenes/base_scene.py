"""
Base class for all game scenes.
"""
from ursina import Entity

class BaseScene(Entity):
    """
    Abstract base class representing a generic scene.
    Inherits from Ursina Entity to allow parenting of scene objects,
    which automatically enables/disables them with the scene.
    """
    
    def __init__(self, **kwargs) -> None:
        """Initialize the scene as an Ursina Entity."""
        print(f"[TRACE] BaseScene: __init__ started for {self.__class__.__name__}")
        super().__init__(**kwargs)
        print(f"[TRACE] BaseScene: Calling setup for {self.__class__.__name__}")
        self.setup()
        print(f"[TRACE] BaseScene: __init__ finished for {self.__class__.__name__}")
        
    def setup(self) -> None:
        """
        Instantiate scene-specific objects here.
        Child entities should set `parent=self` to tie their lifecycle to this scene.
        """
        pass
        
    def on_enter(self, **kwargs) -> None:
        """
        Called automatically when the scene becomes active.
        """
        pass
        
    def update_scene(self, delta_time: float) -> None:
        """
        Called every frame while the scene is active.
        
        Args:
            delta_time (float): Time since last frame.
        """
        pass
        
    def on_exit(self) -> None:
        """
        Called automatically when leaving the scene.
        """
        pass
