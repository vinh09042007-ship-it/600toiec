"""
Defines the PlayerController to handle player logic and lifecycle.
"""
from typing import Tuple
from .player import Player
from .input import PlayerInput
from .movement import PlayerMovement
from .physics import PlayerPhysics
from world.collision import WorldCollision

class PlayerController:
    """
    Manages the Player entity.
    Coordinates input processing and movement logic per frame.
    """
    
    def __init__(self, speed: float, world_collision: WorldCollision) -> None:
        """
        Initialize the controller and its subsystems.
        
        Args:
            speed (float): Base speed injected into the Player.
            world_collision (WorldCollision): The world collision system.
        """
        self.player: Player = Player(speed=speed)
        self.input_system: PlayerInput = PlayerInput()
        self.world_collision: WorldCollision = world_collision
        self.movement_system: PlayerMovement = PlayerMovement(self.player)
        self.physics_system: PlayerPhysics = PlayerPhysics(self.player)

    def update(self, delta_time: float) -> None:
        """
        Update the player logic once per frame.
        
        Args:
            delta_time (float): The time elapsed since the last frame.
        """
        # Step 1: Read user input (pure data)
        move_vector = self.input_system.get_move_vector()
        
        # Step 2: Calculate desired position based on input
        desired_pos = self.movement_system.calculate_desired_position(move_vector, delta_time)
        
        # Step 3: Ask WorldCollision if movement is allowed
        if self.world_collision.is_position_valid(desired_pos[0], desired_pos[2]):
            self.player.position = desired_pos
            self.player.state = "RUNNING" if self.player.is_moving else "IDLE"
        else:
            self.player.state = "IDLE"
        
        # Step 4: Apply physics
        self.physics_system.update(delta_time)

    def get_player_position(self) -> Tuple[float, float, float]:
        """
        Convenience method to retrieve the player's current position.
        
        Returns:
            Tuple[float, float, float]: The (x, y, z) coordinates.
        """
        return self.player.position
