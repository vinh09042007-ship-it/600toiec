from ursina import Entity, color, Text, math, time
from typing import List

class NPCVisual(Entity):
    """
    Constructs a low-poly humanoid using cube primitives.
    Handles the idle animation (breathing/bobbing).
    """
    def __init__(self, skin_color=color.rgb(255, 205, 175), shirt_color=color.cyan, pant_color=color.dark_gray, **kwargs):
        super().__init__(**kwargs)
        
        # Scaling constants to mimic humanoid proportions
        body_scale = (0.8, 1.2, 0.4)
        head_scale = (0.5, 0.5, 0.5)
        arm_scale = (0.2, 1.0, 0.2)
        leg_scale = (0.3, 1.2, 0.3)
        
        # Head
        self.head = Entity(
            parent=self,
            model='cube',
            color=skin_color,
            scale=head_scale,
            position=(0, 2.0, 0)
        )
        
        # Body
        self.body = Entity(
            parent=self,
            model='cube',
            color=shirt_color,
            scale=body_scale,
            position=(0, 1.15, 0)
        )
        
        # Arms
        self.left_arm = Entity(
            parent=self,
            model='cube',
            color=shirt_color,
            scale=arm_scale,
            position=(-0.55, 1.25, 0)
        )
        self.right_arm = Entity(
            parent=self,
            model='cube',
            color=shirt_color,
            scale=arm_scale,
            position=(0.55, 1.25, 0)
        )
        
        # Legs
        self.left_leg = Entity(
            parent=self,
            model='cube',
            color=pant_color,
            scale=leg_scale,
            position=(-0.25, -0.05, 0)
        )
        self.right_leg = Entity(
            parent=self,
            model='cube',
            color=pant_color,
            scale=leg_scale,
            position=(0.25, -0.05, 0)
        )
        
        # Animation properties
        self.anim_speed = 2.0
        self.anim_amplitude = 0.05
        self.base_y = self.y

    def update(self):
        """Idle breathing animation - gentle up/down bobbing."""
        # math.sin is from standard python math module, but ursina math overrides some. 
        # Using built-in math through import math at top
        offset = math.sin(time.time() * self.anim_speed) * self.anim_amplitude
        self.y = self.base_y + offset


class NPC(Entity):
    """
    Logic container for an interactable NPC.
    Separates collision/interaction logic from visual rendering.
    """
    def __init__(self, name: str, role: str, position: tuple[float, float, float], dialogue: List[str], skin_color=color.rgb(255, 205, 175), shirt_color=color.cyan, pant_color=color.dark_gray):
        super().__init__(
            position=position,
            collider='box' # Invisible collider for interaction distance
        )
        
        # Expand collider to comfortably encapsulate the humanoid
        self.collider = 'box'
        
        self.npc_name = name
        self.role = role
        self.dialogue = dialogue
        self.interact_position = position
        
        # Quest Icon
        from world.quest_icons import QuestIcon
        self.quest_icon = QuestIcon(self)
        
        # Visual Model
        self.visual = NPCVisual(
            parent=self,
            skin_color=skin_color,
            shirt_color=shirt_color,
            pant_color=pant_color
        )
        
        # 3D Name Label hovering above the head
        self.name_label = Text(
            parent=self,
            text=self.npc_name,
            position=(0, 2.7, 0),
            origin=(0, 0), # Center alignment
            scale=5,
            color=color.yellow,
            billboard=True # Always faces the camera
        )
