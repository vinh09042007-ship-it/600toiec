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
from core.events import Events
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
        
        self.interaction_manager = InteractionManager(
            self.player_controller.player, 
            self.campus, 
            quest_manager=self.scene_manager.quest_manager
        )
        self.interaction_manager.on_interact = self._on_building_interact
        self.interaction_manager.on_talk = self._on_npc_talk
        
        self.dialogue_manager = DialogueManager()
        self.dialogue_manager.attach_to_camera(camera.ui)
        
        self._spawn_npcs()
        
        # Subscribe to world state changes
        self.scene_manager.quest_manager.event_bus.subscribe(Events.QUEST_STATE_CHANGED, self._refresh_world_state)

    def _spawn_npcs(self) -> None:
        """Instantiates NPCs in the campus."""
        # Standard skin color
        skin = color.rgb(255, 205, 175)
        
        self.npcs = [
            NPC(
                name="Receptionist", 
                role="Campus Guide",
                position=(3, 0, 3), 
                dialogue=["Welcome to the TOEIC Campus!"], 
                skin_color=skin,
                shirt_color=color.gray, 
                pant_color=color.black
            ),
            NPC(
                name="Grammar Professor", 
                role="Grammar Instructor",
                position=(-16, 0, 16), 
                dialogue=["Welcome to Grammar Hall."], 
                skin_color=skin,
                shirt_color=color.rgb(139, 69, 19), # Brown jacket
                pant_color=color.dark_gray
            ),
            NPC(
                name="Vocabulary Professor", 
                role="Vocab Instructor",
                position=(16, 0, 16), 
                dialogue=["Welcome to Vocabulary Hall."], 
                skin_color=skin,
                shirt_color=color.blue, 
                pant_color=color.dark_gray
            ),
            NPC(
                name="Listening Professor", 
                role="Audio Instructor",
                position=(16, 0, 46), 
                dialogue=["Welcome to Listening Hall."], 
                skin_color=skin,
                shirt_color=color.magenta, 
                pant_color=color.blue
            ),
            NPC(
                name="Reading Professor", 
                role="Reading Instructor",
                position=(-16, 0, 46), 
                dialogue=["Welcome to Reading Hall."], 
                skin_color=skin,
                shirt_color=color.orange, 
                pant_color=color.dark_gray
            ),
            NPC(
                name="Exam Supervisor", 
                role="Exam Security",
                position=(4, 0, 74), 
                dialogue=["The Exam building is restricted."], 
                skin_color=skin,
                shirt_color=color.red, 
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
            if hasattr(self.scene_manager, 'transition_manager'):
                self.scene_manager.transition_manager.transition_to(self.scene_manager, "building", building_name=building_name)
            else:
                self.scene_manager.switch_scene("building", building_name=building_name)
        else:
            requirement = quest_manager.get_building_lock_requirement(building_name)
            if "🔒" in requirement:
                quest_manager.notification_ui.show(requirement)
            else:
                quest_manager.notification_ui.show(f"Building Locked\n{requirement}")

    def _on_npc_talk(self, npc: NPC) -> None:
        """Callback triggered when the player talks to an NPC."""
        print(f"[Interaction] Talking to {npc.npc_name}")
        quest_manager = self.scene_manager.quest_manager
        
        # Get dynamic dialogue and callback from quest manager
        dialogue, callback = quest_manager.interact_with_npc(npc.npc_name)
        npc.dialogue = dialogue # Update the data holder
        
        print(f"[NPC] Returning callback: {callback}")
        
        self.dialogue_manager.start_dialogue(
            npc,
            on_end_callback=lambda n=npc, c=callback: self.after_dialogue(n, c)
        )

    def after_dialogue(self, npc: NPC, callback) -> None:
        """Executes quest and state updates after dialogue finishes."""
        print(f"[Campus Callback] after_dialogue triggered for {npc.npc_name}")
        print(f"[Campus Callback] executing callback: {callback}")
        
        if callback:
            callback()
            print("[NPC] Dialogue updated")
            
        # Refresh interaction prompt dynamically if player is near something
        self.interaction_manager._find_nearest_interactable()
        self.interaction_manager._update_prompt()
        print("[Interaction] refreshed")

    def on_enter(self, **kwargs) -> None:
        """Called when entering the campus."""
        self._refresh_world_state()
        
    def _refresh_world_state(self, *args, **kwargs) -> None:
        """Updates all NPCs and Buildings based on the current quest state."""
        quest_manager = self.scene_manager.quest_manager
        active_quest = quest_manager.get_active_quest()
        
        for npc in self.npcs:
            state = quest_manager.get_npc_quest_state(npc.npc_name)
            npc.quest_icon.update_state(state)
            
        for building in self.campus.buildings:
            is_unlocked = quest_manager.is_building_unlocked(building.name)
            building.set_lock_state(not is_unlocked)
            
            # Highlight if it's the active building
            is_active = active_quest is not None and active_quest.target_building == building.name
            building.set_active_highlight(is_active)
        
    def update_scene(self, delta_time: float) -> None:
        """Update systems every frame."""
            
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
        self.interaction_manager.locked_panel.enabled = False
        self.interaction_manager.locked_text.enabled = False
