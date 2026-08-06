"""
Handles gameplay interactions with buildings and other world objects.
"""
from ursina import Text, held_keys, invoke, destroy, color, Entity, camera
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
        self.npcs = []
        self.nearest_interactable = None
        self.interactable_type = None # 'building' or 'npc'
        self.last_found = None
        self.on_interact = None
        self.on_talk = None
        
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
        Checks distance to interactables and updates the prompt.
        Should be called every frame.
        """
        self._find_nearest_interactable()
        self._update_prompt()
        self._check_input()

    def _find_nearest_interactable(self) -> None:
        """
        Finds the nearest building or NPC within interaction range.
        """
        self.nearest_interactable = None
        self.interactable_type = None
        min_dist = const.INTERACTION_DISTANCE
        
        px, py, pz = self.player.position
        
        # Check Buildings
        for building in self.campus.buildings:
            bx, by, bz = building.entrance_position
            dist = math.sqrt((px - bx)**2 + (pz - bz)**2)
            
            if dist <= min_dist:
                min_dist = dist
                self.nearest_interactable = building
                self.interactable_type = 'building'
                
        # Check NPCs
        for npc in self.npcs:
            nx, ny, nz = npc.interact_position
            dist = math.sqrt((px - nx)**2 + (pz - nz)**2)
            
            if dist <= min_dist:
                min_dist = dist
                self.nearest_interactable = npc
                self.interactable_type = 'npc'

    def _update_prompt(self) -> None:
        """
        Shows or hides the interaction prompt based on proximity.
        """
        if self.nearest_interactable:
            if self.nearest_interactable != self.last_found:
                name = self.nearest_interactable.name if self.interactable_type == 'building' else self.nearest_interactable.npc_name
                print(f"Found {self.interactable_type}: {name}")
                self.last_found = self.nearest_interactable
                
            if self.interactable_type == 'building':
                self.prompt.text = f"[E] Enter {self.nearest_interactable.name}"
            else:
                self.prompt.text = f"[E] Talk to {self.nearest_interactable.npc_name}"
                
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
            if self.nearest_interactable:
                # Hide the prompt immediately
                self.prompt.enabled = False
                
                if self.interactable_type == 'building':
                    print(f"Entering {self.nearest_interactable.name}...")
                    
                    if self.on_interact:
                        self.on_interact(self.nearest_interactable.name)
                        
                elif self.interactable_type == 'npc':
                    print(f"Talking to {self.nearest_interactable.npc_name}...")
                    if self.on_talk:
                        self.on_talk(self.nearest_interactable)
                        
                # Clear nearest so interaction doesn't re-trigger instantly
                self.nearest_interactable = None
        
        self.was_pressed = is_pressed
