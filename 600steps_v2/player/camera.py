"""
Defines the Third-Person Camera system for the player.
"""
from ursina import camera, lerp, Vec3
from .player import Player
import utils.constants as const

class PlayerCamera:
    """
    Controls the main camera to follow the player in a third-person perspective.
    Operates independently of input and movement systems.
    """

    def __init__(self, target_player: Player) -> None:
        """
        Initializes the camera system.

        Args:
            target_player (Player): The player entity to follow.
        """
        self.target: Player = target_player
        self.offset: Vec3 = Vec3(*const.CAMERA_OFFSET)
        self.is_cinematic: bool = False

        
        # Initial camera setup (snap to position)
        camera.position = self.target.position + self.offset
        camera.fov = 70
        camera.look_at(self.target.position + Vec3(0, 1.5, 0))

    def update(self, delta_time: float) -> None:
        """
        Updates the camera position to smoothly follow the target.
        Should be called once per frame.

        Args:
            delta_time (float): The time elapsed since the last frame.
        """
        if self.is_cinematic:
            return
            
        # Calculate the desired position
        desired_position = self.target.position + self.offset
        
        # Smoothly interpolate current position towards desired position
        camera.position = lerp(
            camera.position, 
            desired_position, 
            delta_time * const.CAMERA_LERP_SPEED
        )
        
        # Always look at the player's upper body
        camera.look_at(self.target.position + Vec3(0, 1.5, 0))
