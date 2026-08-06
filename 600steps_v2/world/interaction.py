"""
Handles gameplay interactions with buildings and other world objects.
"""
from ursina import Text, held_keys, invoke, destroy, color
import math
from typing import Optional
from .campus import Campus
from player.player import Player
import utils.constants as const

class InteractionManager:
    """
    Detects player proximity to buildings and handles interaction inputs.
    """
    
    def __init__(self, player: Player, campus: Campus) -> None:
        """
        Initializes the interaction system.
        
        Args:
            player (Player): The player entity to check distance from.
            campus (Campus): The campus containing the buildings.
        """
        self.player = player
        self.campus = campus
        self.nearest_building = None
        self.last_found = None
        self.on_interact = None
        
        # UI Prompt Text
        self.prompt = Text(
            text="",
            position=(0, -0.35),
            origin=(0, 0),
            scale=2,
            enabled=False
        )
        
        # Prevents multiple triggers from holding the key
        self.was_pressed = False

    def update(self) -> None:
        """
        Checks distance to buildings and updates the interaction prompt.
        Should be called every frame.
        """
        self._find_nearest_building()
        self._update_prompt()
        self._check_input()

    def _find_nearest_building(self) -> None:
        """
        Finds the nearest building entrance within interaction range.
        Uses 2D (X, Z) distance to ignore Y height differences.
        """
        self.nearest_building = None
        min_dist = const.INTERACTION_DISTANCE
        
        px, py, pz = self.player.position
        
        for building in self.campus.buildings:
            bx, by, bz = building.entrance_position
            
            # Calculate 2D distance on X-Z plane to the entrance
            dist = math.sqrt((px - bx)**2 + (pz - bz)**2)
            
            if dist <= min_dist:
                min_dist = dist
                self.nearest_building = building

    def _update_prompt(self) -> None:
        """
        Shows or hides the interaction prompt based on proximity.
        """
        if self.nearest_building:
            # 7. Debug prompt: Print only when entering range for the first time
            if self.nearest_building != self.last_found:
                print(f"Found building: {self.nearest_building.name}")
                self.last_found = self.nearest_building
                
            self.prompt.text = f"[E] Enter {self.nearest_building.name}"
            self.prompt.enabled = True
        else:
            self.last_found = None
            self.prompt.enabled = False

    def _check_input(self) -> None:
        """
        Checks if the player presses the interaction key ('e').
        Triggers only once per press.
        """
        is_pressed = held_keys['e']
        
        if is_pressed and not self.was_pressed:
            print("Pressed E")
            if self.nearest_building:
                print(f"Entering {self.nearest_building.name}...")
                
                # Show temporary on-screen message
                temp_msg = Text(
                    text=f"Entered {self.nearest_building.name}",
                    position=(0, 0),
                    origin=(0, 0),
                    scale=2.5,
                    color=color.green
                )
                
                # Destroy the message after 2 seconds
                invoke(destroy, temp_msg, delay=2.0)
                
                # Hide the prompt immediately
                self.prompt.enabled = False
                
                # Trigger callback
                if self.on_interact:
                    self.on_interact(self.nearest_building.name)
                
                # Clear nearest_building so interaction doesn't re-trigger
                self.nearest_building = None
        
        self.was_pressed = is_pressed
