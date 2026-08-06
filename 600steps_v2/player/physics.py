"""
Handles physics calculations for the Player entity.
"""
from .player import Player
import utils.constants as const

class PlayerPhysics:
    """
    Applies physics rules such as gravity to the player.
    Operates independently of input or horizontal movement logic.
    """
    
    def __init__(self, player: Player) -> None:
        """
        Initializes the physics system.
        
        Args:
            player (Player): The player entity to modify.
        """
        self.player = player

    def update(self, delta_time: float) -> None:
        """
        Applies gravity and updates vertical position.
        
        Args:
            delta_time (float): Time elapsed since the last frame.
        """
        if not self.player.is_grounded:
            # Apply gravity
            self.player.vertical_velocity += const.PLAYER_GRAVITY * delta_time
            
            # Clamp to terminal velocity
            if self.player.vertical_velocity < const.PLAYER_TERMINAL_VELOCITY:
                self.player.vertical_velocity = const.PLAYER_TERMINAL_VELOCITY
                
        # Calculate new Y position
        new_y = self.player.y + (self.player.vertical_velocity * delta_time)
        
        # Simple ground collision
        if new_y <= const.GROUND_HEIGHT:
            new_y = const.GROUND_HEIGHT
            self.player.vertical_velocity = 0.0
            self.player.is_grounded = True
        else:
            self.player.is_grounded = False
            
        self.player.y = new_y
