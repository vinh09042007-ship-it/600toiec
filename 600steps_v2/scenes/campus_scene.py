"""
The main open-world campus scene.
"""
from ursina import Sky, camera, color
from .base_scene import BaseScene
from world.campus import Campus
from world.collision import WorldCollision
from player.controller import PlayerController
from player.camera import PlayerCamera
from world.interaction import InteractionManager
from world.npc import NPC
from ui.dialogue_manager import DialogueManager
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
        self.interaction_manager.on_interact = self._on_building_interact
        self.interaction_manager.on_talk = self._on_npc_talk
        
        self.dialogue_manager = DialogueManager()
        self.dialogue_manager.attach_to_camera(camera.ui)
        
        self._spawn_npcs()

    def _spawn_npcs(self) -> None:
        """Instantiates NPCs in the campus."""
        # Standard skin color
        skin = color.rgb(255, 205, 175)
        
        self.npcs = [
            NPC(
                name="Professor", 
                role="Grammar Instructor",
                position=(-16, 0, 16), 
                dialogue=[
                    "Welcome to Grammar Hall.",
                    "Come back when you are ready."
                ], 
                skin_color=skin,
                shirt_color=color.rgb(139, 69, 19), # Brown jacket
                pant_color=color.dark_gray
            ),
            
            NPC(
                name="Librarian", 
                role="Reading Guide",
                position=(-16, 0, 46), 
                dialogue=[
                    "Shh! The Reading building is quiet.",
                    "Enjoy your books."
                ], 
                skin_color=skin,
                shirt_color=color.cyan, 
                pant_color=color.white
            ),
            
            NPC(
                name="Receptionist", 
                role="Campus Guide",
                position=(3, 0, 3), 
                dialogue=[
                    "Welcome to the TOEIC Campus!",
                    "Explore the buildings to practice."
                ], 
                skin_color=skin,
                shirt_color=color.gray, 
                pant_color=color.black
            ),
            
            NPC(
                name="Listening Instructor", 
                role="Audio Guide",
                position=(16, 0, 46), 
                dialogue=[
                    "Listen closely to the audio tracks.",
                    "Focus is key here."
                ], 
                skin_color=skin,
                shirt_color=color.magenta, 
                pant_color=color.blue
            ),
            
            NPC(
                name="Security Guard", 
                role="Exam Security",
                position=(4, 0, 74), 
                dialogue=[
                    "The Exam building is restricted.",
                    "Only prepared students may enter."
                ], 
                skin_color=skin,
                shirt_color=color.rgb(0, 0, 128), # Navy blue
                pant_color=color.black
            )
        ]
        
        for npc in self.npcs:
            npc.parent = self
            
        self.interaction_manager.npcs = self.npcs

    def _on_building_interact(self, building_name: str) -> None:
        """Callback triggered when the player interacts with a building."""
        quest_manager = self.scene_manager.quest_manager
        
        if quest_manager.is_building_unlocked(building_name):
            self.scene_manager.switch_scene("building", building_name=building_name)
        else:
            requirement = quest_manager.get_building_lock_requirement(building_name)
            quest_manager.notification_ui.show(f"Building Locked\n{requirement}")

    def _on_npc_talk(self, npc: NPC) -> None:
        """Callback triggered when the player talks to an NPC."""
        quest_manager = self.scene_manager.quest_manager
        
        # Get dynamic dialogue from quest manager
        dialogue = quest_manager.interact_with_npc(npc.npc_name)
        npc.dialogue = dialogue # Update the data holder
        
        self.dialogue_manager.start_dialogue(npc)

    def on_enter(self, **kwargs) -> None:
        """Called when entering the campus."""
        pass
        
    def update_scene(self, delta_time: float) -> None:
        """Update systems every frame."""
        # Update quest icons
        quest_manager = self.scene_manager.quest_manager
        for npc in self.npcs:
            state = quest_manager.get_npc_quest_state(npc.npc_name)
            npc.quest_icon.update_state(state)
            
        # If dialogue is active, freeze player and interaction
        if self.dialogue_manager.is_active:
            self.dialogue_manager.update()
            return
            
        self.player_controller.update(delta_time)
        self.player_camera.update(delta_time)
        self.interaction_manager.update()

    def on_exit(self) -> None:
        """Called when leaving the campus."""
        # Ensure UI prompt is hidden
        self.interaction_manager.prompt.enabled = False
