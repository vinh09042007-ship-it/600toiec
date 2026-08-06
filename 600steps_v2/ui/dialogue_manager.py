from ursina import Entity, Text, color, held_keys
from world.npc import NPC

class DialogueManager:
    """
    Manages the rendering and flow of NPC dialogues.
    """
    def __init__(self):
        self.is_active = False
        self.current_npc = None
        self.dialogue_index = 0
        
        # UI Elements
        self.bg = Entity(
            parent=None, # Will be attached to camera.ui
            model='quad',
            color=color.rgba(0, 0, 0, 0.8),
            scale=(1.2, 0.3),
            position=(0, -0.35),
            enabled=False
        )
        
        self.name_text = Text(
            parent=self.bg,
            text="",
            position=(-0.45, 0.4),
            origin=(-0.5, 0.5),
            scale=3,
            color=color.gold
        )
        
        self.dialogue_text = Text(
            parent=self.bg,
            text="",
            position=(-0.45, 0.1),
            origin=(-0.5, 0.5),
            scale=2,
            color=color.white
        )
        
        self.instruction_text = Text(
            parent=self.bg,
            text="[SPACE] Next   [ESC] Close",
            position=(0.45, -0.3),
            origin=(0.5, -0.5),
            scale=1.5,
            color=color.light_gray
        )
        
        self.was_space_pressed = False
        self.on_dialogue_end = None

    def attach_to_camera(self, camera_ui):
        """Attaches the dialogue UI to the camera's UI layer."""
        self.bg.parent = camera_ui

    def start_dialogue(self, npc: NPC, on_end_callback=None):
        """Starts a dialogue sequence with the given NPC."""
        self.current_npc = npc
        self.dialogue_index = 0
        self.is_active = True
        self.was_space_pressed = True # Prevent accidental double skip if SPACE was held
        self.on_dialogue_end = on_end_callback
        
        self.bg.enabled = True
        self.name_text.text = npc.npc_name
        self._update_text()

    def _update_text(self):
        """Updates the dialogue text to the current line."""
        if self.current_npc and self.dialogue_index < len(self.current_npc.dialogue):
            self.dialogue_text.text = self.current_npc.dialogue[self.dialogue_index]
        else:
            self.end_dialogue()

    def end_dialogue(self):
        """Closes the dialogue UI."""
        self.is_active = False
        self.current_npc = None
        self.bg.enabled = False
        if self.on_dialogue_end:
            self.on_dialogue_end()

    def update(self):
        """Handles dialogue progression inputs. Called every frame when active."""
        if not self.is_active:
            return

        is_space_pressed = held_keys['space']
        if is_space_pressed and not self.was_space_pressed:
            self.dialogue_index += 1
            self._update_text()
            
        self.was_space_pressed = is_space_pressed

        if held_keys['escape']:
            self.end_dialogue()
