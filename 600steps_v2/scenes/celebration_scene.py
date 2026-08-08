import random
import os
import math
from ursina import Entity, color, Text, camera, Sky, destroy, time, Vec3, Sequence, Func, Wait, Audio, mouse
from scenes.base_scene import BaseScene
from player.controller import PlayerController
from player.camera import PlayerCamera
from world.npc import NPC
import utils.constants as const
from core.save_manager import SaveManager

class Confetti(Entity):
    def __init__(self, **kwargs):
        super().__init__(model='quad', double_sided=True, **kwargs)
        self.velocity = Vec3(random.uniform(-2, 2), random.uniform(-3, -6), random.uniform(-2, 2))
        self.rot_speed = Vec3(random.uniform(100, 300), random.uniform(100, 300), random.uniform(100, 300))
        
    def update(self):
        self.position += self.velocity * time.dt
        self.rotation += self.rot_speed * time.dt
        if self.y < 0:
            self.y = random.uniform(15, 25)
            self.x = random.uniform(-10, 10)
            self.z = random.uniform(0, 10)

class CelebrationScene(BaseScene):
    def __init__(self, scene_manager, **kwargs):
        self.scene_manager = scene_manager
        super().__init__(**kwargs)
        
    def setup(self) -> None:
        self.entities_to_destroy = []
        self.confetti_list = []
        self.ceremony_sequence = None
        self.audio_track = None
        self.can_exit = False
        self.current_score_anim = 0
        
        # 1. Environment
        self.sky = Sky(parent=self)
        self.ground = Entity(parent=self, model='plane', scale=(100, 1, 100), color=color.green, collider='box')
        
        # 2. Player and Camera
        from world.collision import WorldCollision
        self.world_collision = WorldCollision([]) 
        
        self.player_controller = PlayerController(speed=const.PLAYER_SPEED, world_collision=self.world_collision)
        self.player_controller.player.parent = self
        self.player_controller.player.position = (0, 0, -3)
        self.player_camera = PlayerCamera(self.player_controller.player)
        
        # 3. Teacher
        self.teacher = NPC(
            name="Exam Supervisor",
            role="",
            position=(0, 0, 8),
            dialogue=[],
            shirt_color=color.black,
            pant_color=color.dark_gray
        )
        self.teacher.parent = self
        self.teacher.look_at(self.player_controller.player)
        self.entities_to_destroy.append(self.teacher)
        
        # 4. Podium & Certificate Placeholder
        self.podium = Entity(parent=self, model='cube', color=color.rgb(139/255, 69/255, 19/255), scale=(1.2, 1.0, 1.0), position=(0, 0.5, 3))
        self.cert_3d = Entity(parent=self.podium, model='cube', color=color.white, scale=(0.6, 0.05, 0.4), position=(0, 0.5, 0))
        self.entities_to_destroy.extend([self.podium, self.cert_3d])
        
        # UI Container (CRITICAL: MUST BE DISABLED ON CREATION)
        self.ui_container = Entity(parent=camera.ui, enabled=False)
        self.entities_to_destroy.append(self.ui_container)
        
        # Phase 1 UI
        self.blackout = Entity(parent=self.ui_container, model='quad', color=color.black, scale=10, z=1)
        self.score_label = Text(parent=self.ui_container, text="", origin=(0, 0), scale=3, position=(0, 0.1), color=color.white, z=0, enabled=False)
        
        # Phase 2 UI
        self.dialogue_bg = Entity(parent=self.ui_container, model='quad', color=color.rgba(0,0,0,0.8), scale=(1.2, 0.2), position=(0, -0.35), enabled=False)
        self.dialogue_text = Text(parent=self.ui_container, text="", origin=(0, 0), scale=1.5, position=(0, -0.35), enabled=False)
        
        # Phase 4 UI
        self.final_title = Text(parent=self.ui_container, text="CONGRATULATIONS!", origin=(0, 0), scale=4, position=(0, 0.25), color=color.gold, enabled=False, z=-1)
        self.final_sub = Text(parent=self.ui_container, text="", origin=(0, 0), scale=2, position=(0, 0), color=color.white, enabled=False, z=-1)
        self.prompt_text = Text(parent=self.ui_container, text="[ENTER] to Return to Campus", origin=(0, 0), scale=1.5, position=(0, -0.3), color=color.rgba(0.8, 0.8, 0.8, 0), z=-1)

    def on_enter(self, **kwargs) -> None:
        self.final_score = int(kwargs.get("final_score", 600))
        self.correct_answers = int(kwargs.get("correct_answers", 6))
        self.profile = self.scene_manager.player_profile
        self.target = getattr(self.profile, 'target_toeic_score', 600)
        self.player_name = getattr(self.profile, 'name', "Student")
        
        # Enable UI container safely only when scene is active
        self.ui_container.enabled = True
        self.blackout.color = color.black # Ensure opaque blackout starts
        
        mouse.locked = True
        self.player_controller.player.rotation = (0, 0, 0)
        self.teacher.position = (0, 0, 8)
        self.teacher.look_at(self.player_controller.player)
        
        self.can_exit = False
        self.start_graduation_sequence()
        
    def start_graduation_sequence(self):
        def set_text(obj, val): obj.text = val
        def set_enabled(obj, val): obj.enabled = val
        
        def animate_score():
            from ursina import invoke
            self.current_score_anim = 0
            self.score_label.text = f"FINAL SCORE: {self.current_score_anim}"
            def count_up():
                if not self.enabled: return
                self.current_score_anim += min(20, self.final_score - self.current_score_anim)
                self.score_label.text = f"FINAL SCORE: {self.current_score_anim}"
                if self.current_score_anim < self.final_score:
                    invoke(count_up, delay=0.02)
            count_up()
            
        def create_confetti():
            colors = [color.red, color.yellow, color.blue, color.green, color.magenta, color.cyan]
            for _ in range(80):
                c = Confetti(
                    parent=self, 
                    color=random.choice(colors), 
                    scale=random.uniform(0.1, 0.3), 
                    position=(random.uniform(-10, 10), random.uniform(10, 25), random.uniform(-5, 10)), 
                    rotation=(random.uniform(0, 360), random.uniform(0, 360), random.uniform(0, 360))
                )
                self.confetti_list.append(c)
                
        def play_sound():
            sfx_path = 'assets/audio/sfx/success.mp3'
            if os.path.exists(sfx_path):
                self.audio_track = Audio(sfx_path, autoplay=True, volume=0.5, loop=False)
            elif os.path.exists('assets/audio/ui/success.ogg'):
                self.audio_track = Audio('assets/audio/ui/success.ogg', autoplay=True, volume=0.5, loop=False)
                
        def mark_game_completed():
            self.profile.game_completed = True
            SaveManager.save_profile(self.profile)

        self.ceremony_sequence = Sequence(
            # Phase 1: Reveal
            Wait(1.0),
            Func(set_enabled, self.score_label, True),
            Func(set_text, self.score_label, "CONGRATULATIONS!"),
            Wait(2.0),
            Func(set_text, self.score_label, "YOU ACHIEVED YOUR 600 TOEIC GOAL!"),
            Wait(2.5),
            
            # Phase 2: Stage & Walk
            Func(self.score_label.animate_color, color.rgba(1, 1, 1, 0), 0.5),
            Wait(0.5),
            Func(self.blackout.animate_color, color.rgba(0,0,0,0), 1.5),
            Wait(1.5),
            Func(self.teacher.animate_position, (0, 0, 5), 2.0),
            Wait(2.0),
            
            # Phase 3: Congratulations Dialogue
            Func(set_enabled, self.dialogue_bg, True),
            Func(set_enabled, self.dialogue_text, True),
            Func(set_text, self.dialogue_text, "Congratulations!"),
            Wait(2.0),
            Func(set_text, self.dialogue_text, "You worked hard and reached your goal."),
            Wait(2.5),
            Func(set_text, self.dialogue_text, f"Your TOEIC score is {self.final_score}!"),
            Wait(2.5),
            Func(set_text, self.dialogue_text, "You should be proud of yourself."),
            Wait(2.5),
            Func(set_enabled, self.dialogue_bg, False),
            Func(set_enabled, self.dialogue_text, False),
            
            # Phase 4: Podium Moment & Celebration
            Func(self.player_controller.player.animate_position, (0, 0, 1.5), 2.0),
            Wait(2.0),
            Func(create_confetti),
            Func(play_sound),
            Wait(3.0),
            
            # Phase 5: Final Message
            Func(mark_game_completed),
            Func(set_enabled, self.final_title, True),
            Func(set_text, self.final_title, "600 TOEIC JOURNEY COMPLETE"),
            Func(set_enabled, self.final_sub, True),
            Func(set_text, self.final_sub, f"Congratulations!\nYou achieved your goal of 600 TOEIC.\n\nFinal TOEIC Score: {self.final_score}"),
            Wait(4.0),
            Func(self.final_title.animate_color, color.rgba(1, 0.84, 0, 0), 0.5),
            Func(self.final_sub.animate_color, color.rgba(1, 1, 1, 0), 0.5),
            Wait(1.0),
            
            # Phase 6: Next Goal
            Func(set_enabled, self.final_title, False),
            Func(set_text, self.final_sub, "You have completed the journey.\nThis is not the end — it is the beginning of your next goal."),
            Func(self.final_sub.animate_color, color.white, 1.0),
            Wait(4.0),
            Func(set_text, self.prompt_text, "[ENTER] Continue"),
            Func(self.prompt_text.animate_color, color.rgba(0.8, 0.8, 0.8, 1), 1.0),
            Func(setattr, self, 'can_exit', True)
        )
        self.ceremony_sequence.start()
        
    def input(self, key: str) -> None:
        if not self.enabled: return
        if self.can_exit and key in ('enter', 'return'):
            if hasattr(self.scene_manager, 'transition_manager'):
                self.scene_manager.transition_manager.transition_to(self.scene_manager, "campus")
            else:
                self.scene_manager.switch_scene("campus")

    def update_scene(self, delta_time: float) -> None:
        if hasattr(self, 'blackout') and self.blackout.color[3] == 0 and not self.can_exit:
            camera.rotation_y += 5 * delta_time
            camera.x = 2 * math.sin(time.time() * 0.5)

    def on_exit(self) -> None:
        self.ui_container.enabled = False
        
        if self.ceremony_sequence:
            self.ceremony_sequence.kill()
            
        if hasattr(self, 'audio_track') and self.audio_track:
            try:
                self.audio_track.stop()
            except Exception:
                pass
            destroy(self.audio_track)
            self.audio_track = None
            
        for c in self.confetti_list:
            destroy(c)
        self.confetti_list.clear()
        
        mouse.locked = False
        camera.rotation_y = 0
        camera.x = 0

