from ursina import Entity, color, Text, camera, Sky, destroy
from scenes.base_scene import BaseScene
from player.controller import PlayerController
from player.camera import PlayerCamera
from world.npc import NPC
import utils.constants as const

class CelebrationScene(BaseScene):
    def __init__(self, scene_manager, **kwargs):
        self.scene_manager = scene_manager
        super().__init__(**kwargs)
        
    def setup(self) -> None:
        self.entities_to_destroy = []
        
        # 1. Environment
        self.sky = Sky(color=color.rgb(135, 206, 235), parent=self)
        self.ground = Entity(
            parent=self,
            model='plane',
            scale=(100, 1, 100),
            color=color.rgb(34, 139, 34),
            collider='box'
        )
        
        # 2. Player and Camera
        from world.collision import WorldCollision
        self.world_collision = WorldCollision([]) # Empty collision for now
        
        self.player_controller = PlayerController(
            speed=const.PLAYER_SPEED,
            world_collision=self.world_collision
        )
        self.player_controller.player.parent = self
        self.player_controller.player.position = (0, 0, 0)
        
        self.player_camera = PlayerCamera(self.player_controller.player)
        
        # 3. NPCs
        self.teacher = NPC(
            name="Exam Supervisor",
            role="",
            position=(0, 0, 5),
            dialogue=[],
            shirt_color=color.black,
            pant_color=color.dark_gray
        )
        self.teacher.parent = self
        self.teacher.look_at(self.player_controller.player)
        self.entities_to_destroy.append(self.teacher)
        
        self.student1 = NPC(
            name="Student 1",
            role="",
            position=(-3, 0, 4),
            dialogue=[],
            shirt_color=color.red,
            pant_color=color.blue
        )
        self.student1.parent = self
        self.student1.look_at(self.player_controller.player)
        self.entities_to_destroy.append(self.student1)
        
        self.student2 = NPC(
            name="Student 2",
            role="",
            position=(3, 0, 4),
            dialogue=[],
            shirt_color=color.yellow,
            pant_color=color.blue
        )
        self.student2.parent = self
        self.student2.look_at(self.player_controller.player)
        self.entities_to_destroy.append(self.student2)
        
        # 4. Basic UI Text
        self.ui_container = Entity(parent=camera.ui)
        
        self.title_text = Text(
            parent=self.ui_container,
            text="Congratulations!",
            origin=(0, 0),
            position=(0, 0.2),
            scale=3,
            color=color.gold
        )
        
        self.sub_text = Text(
            parent=self.ui_container,
            text="You reached your TOEIC goal!",
            origin=(0, 0),
            position=(0, 0),
            scale=2,
            color=color.white
        )
        
        self.prompt_text = Text(
            parent=self.ui_container,
            text="[ENTER] to Return to Campus",
            origin=(0, 0),
            position=(0, -0.3),
            scale=1.5,
            color=color.light_gray
        )

    def on_enter(self, **kwargs) -> None:
        self.final_score = kwargs.get("final_score", 600)
        # Force player rotation to look at the teacher initially
        self.player_controller.player.rotation = (0, 0, 0)
        
    def input(self, key: str) -> None:
        if not self.enabled: return
        
        if key == 'enter' or key == 'return':
            self.scene_manager.switch_scene("campus")

    def on_exit(self) -> None:
        for ent in self.entities_to_destroy:
            destroy(ent)
        self.entities_to_destroy.clear()
        
        if hasattr(self, 'ui_container'):
            destroy(self.ui_container)
