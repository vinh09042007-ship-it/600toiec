from ursina import Entity, Text, color, held_keys
from world.npc import NPC

class DialogueManager(Entity):
    """
    Manages the rendering and flow of NPC dialogues.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_active = False
        self.current_npc = None
        self.dialogue_index = 0
        
        # UI Elements
        # Background box at the bottom of the screen
        self.bg = Entity(
            parent=self, 
            model='quad',
            color=color.rgba(0, 0, 0, 0.8),
            scale=(1.4, 0.35),
            position=(0, -0.35),
            enabled=False
        )
        
        # Parent text to self to avoid inheriting the non-uniform scale of the bg
        self.name_text = Text(
            parent=self,
            text="",
            position=(-0.65, -0.22),
            origin=(-0.5, 0.5), # Top-Left
            scale=4,
            color=color.gold,
            enabled=False
        )
        
        self.dialogue_text = Text(
            parent=self,
            text=" ",
            position=(-0.65, -0.28),
            origin=(-0.5, 0.5), # Top-Left
            scale=3.5,
            color=color.white,
            enabled=False
        )
        self.dialogue_text.wordwrap = 45
        
        self.instruction_text = Text(
            parent=self,
            text="[SPACE] Next   [ESC] Close",
            position=(0.65, -0.48),
            origin=(0.5, -0.5), # Bottom-Right
            scale=2,
            color=color.light_gray,
            enabled=False
        )
        
        self.on_dialogue_end = None

    def attach_to_camera(self, camera_ui):
        """Attaches the dialogue UI to the camera's UI layer."""
        self.parent = camera_ui
        self.bg.parent = self

    def start_dialogue(self, npc: NPC, on_end_callback=None):
        """Starts a dialogue sequence with the given NPC."""
        self.current_npc = npc
        self.dialogue_index = 0
        self.is_active = True
        self.on_dialogue_end = on_end_callback
        
        self.bg.enabled = True
        self.name_text.enabled = True
        self.dialogue_text.enabled = True
        self.instruction_text.enabled = True
        
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
        if not self.is_active:
            return
            
        print("[Dialogue End] Finished")
        self.is_active = False
        self.current_npc = None
        self.bg.enabled = False
        self.name_text.enabled = False
        self.dialogue_text.enabled = False
        self.instruction_text.enabled = False
        
        if self.on_dialogue_end:
            self.on_dialogue_end()

    def input(self, key):
        """Handles discrete inputs for dialogue."""
        if not self.is_active:
            return
            
        if key == 'space':
            print("[Dialogue] Next line")
            self.dialogue_index += 1
            self._update_text()
            
        elif key == 'escape':
            self.end_dialogue()

    def update(self):
        # Kept for compatibility if called manually
        pass
