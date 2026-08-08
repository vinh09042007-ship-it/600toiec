"""
The main open-world campus scene.
"""
from ursina import Sky, camera, color, Sequence, Func, Wait, Entity, Text, destroy, invoke, curve, Vec3
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
from world.ambient_life import AmbientLifeManager

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
        self.ambient_life = AmbientLifeManager(self.campus, self.world_collision, self, self.player_controller.player)
        
        # Subscribe to world state changes
        self.scene_manager.quest_manager.event_bus.subscribe(Events.QUEST_STATE_CHANGED, self._refresh_world_state)

    def _spawn_npcs(self) -> None:
        """Instantiates NPCs in the campus."""
        # Standard skin color
        skin = color.rgb(255, 205, 175)
        
        # Teacher scientist 3D model for station professors
        teacher_model = 'assets/models/teacher_scientist/base'
        teacher_texture = 'assets/models/teacher_scientist/texture_diffuse.png'
        teacher_scale = 1.12
        
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
                custom_model=teacher_model,
                custom_texture=teacher_texture,
                custom_scale=teacher_scale
            ),
            NPC(
                name="Vocabulary Professor", 
                role="Vocab Instructor",
                position=(16, 0, 16), 
                dialogue=["Welcome to Vocabulary Hall."], 
                custom_model=teacher_model,
                custom_texture=teacher_texture,
                custom_scale=teacher_scale
            ),
            NPC(
                name="Listening Professor", 
                role="Audio Instructor",
                position=(16, 0, 46), 
                dialogue=["Welcome to Listening Hall."], 
                custom_model=teacher_model,
                custom_texture=teacher_texture,
                custom_scale=teacher_scale
            ),
            NPC(
                name="Reading Professor", 
                role="Reading Instructor",
                position=(-16, 0, 46), 
                dialogue=["Welcome to Reading Hall."], 
                custom_model=teacher_model,
                custom_texture=teacher_texture,
                custom_scale=teacher_scale
            ),
            NPC(
                name="Exam Supervisor", 
                role="Exam Security",
                position=(4, 0, 74), 
                dialogue=["The Exam building is restricted."], 
                custom_model=teacher_model,
                custom_texture=teacher_texture,
                custom_scale=teacher_scale
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
        
        # Debug print for completion status as requested
        completed_steps = 600 if getattr(self.scene_manager.player_profile, 'game_completed', False) else 0
        print(f"Completed: {completed_steps} / 600")
        
        # Check if the game has just been completed via active exam transition
        is_completed = kwargs.get("game_completed", False)
        if is_completed:
            # Save the state to the profile if not already there
            if not getattr(self.scene_manager.player_profile, 'game_completed', False):
                self.scene_manager.player_profile.game_completed = True
                from core.save_manager import SaveManager
                SaveManager.save_profile(self.scene_manager.player_profile)
                
            self.start_graduation_sequence()
            
    def start_graduation_sequence(self) -> None:
        """Play cinematic graduation ceremony sequence."""
        if getattr(self, 'victory_overlay_shown', False):
            return
            
        self.victory_overlay_shown = True
        self.game_completed = True # Locks update loop
        self.player_camera.is_cinematic = True
        if hasattr(self, 'ambient_life'):
            self.ambient_life.set_enabled(False)
        
        # 1. Create Stage and Podium (Tracked for cleanup)
        self.graduation_props = []
        
        # Stage Platform
        stage_base = Entity(parent=self, model='cube', scale=(8, 0.2, 6), position=(0, 0.1, 10), color=color.rgb(190/255, 160/255, 115/255)) # Warm beige
        self.graduation_props.append(stage_base)
        
        stage_border = Entity(parent=self, model='cube', scale=(8.2, 0.18, 6.2), position=(0, 0.09, 10), color=color.rgb(75/255, 45/255, 25/255)) # Dark brown border
        self.graduation_props.append(stage_border)
        
        carpet = Entity(parent=self, model='cube', scale=(1.5, 0.05, 5), position=(0, 0.21, 9.5), color=color.rgb(90/255, 20/255, 30/255)) # Dark burgundy
        self.graduation_props.append(carpet)
        
        # Podium Assembly
        podium_base = Entity(parent=self, model='cube', scale=(2, 0.5, 2), position=(0, 0.45, 11), color=color.rgb(85/255, 55/255, 30/255))
        self.graduation_props.append(podium_base)
        
        podium_left = Entity(parent=self, model='cube', scale=(0.2, 0.55, 2.1), position=(-0.9, 0.45, 11), color=color.rgb(60/255, 35/255, 15/255))
        self.graduation_props.append(podium_left)
        
        podium_right = Entity(parent=self, model='cube', scale=(0.2, 0.55, 2.1), position=(0.9, 0.45, 11), color=color.rgb(60/255, 35/255, 15/255))
        self.graduation_props.append(podium_right)
        
        podium_front = Entity(parent=self, model='cube', scale=(1.6, 0.4, 0.1), position=(0, 0.45, 9.95), color=color.rgb(140/255, 95/255, 55/255))
        self.graduation_props.append(podium_front)
        
        podium_emblem = Entity(parent=self, model='quad', scale=(0.3, 0.3, 0.1), position=(0, 0.45, 9.89), rotation_z=45, color=color.rgb(220/255, 170/255, 40/255))
        self.graduation_props.append(podium_emblem)
        
        # 2. Spawn Teacher
        # Podium top is at y = 0.45 + 0.25 = 0.7. Teacher feet are at -0.65 from center, so center must be 0.7 + 0.65 = 1.35
        self.teacher = NPC(
            name="Teacher",
            role="Mentor",
            position=(0, 1.35, 11),
            dialogue=[],
            skin_color=color.rgb(255/255, 205/255, 175/255),
            shirt_color=color.dark_gray,
            pant_color=color.black
        )
        self.teacher.parent = self
        
        # 3. Position Player
        # Save original transform to restore later
        self.original_player_pos = self.player_controller.player.position
        self.original_player_rot = self.player_controller.player.model_pivot.rotation_y
        
        # Stage surface is at Y=0.2. Player root offset is Y=1.0. Total = 1.2
        self.player_controller.player.position = (0, 1.2, 8)
        import math
        target_y = math.degrees(math.atan2(0, 1))
        self.player_controller.player.model_pivot.rotation_y = target_y + 180
        
        # Teacher explicitly faces the player on the horizontal plane only
        dx = self.player_controller.player.x - self.teacher.x
        dz = self.player_controller.player.z - self.teacher.z
        teacher_yaw = math.degrees(math.atan2(dx, dz))
        self.teacher.rotation = (0, teacher_yaw, 0) # Force absolute upright rotation
        
        # 4. Cinematic Camera
        # Start at a wide establishing shot ~15 meters away, forcing roll (Z) to 0
        camera.position = (12, 6, -3)
        camera.rotation = (10, -50, 0)
        
        # Smoothly transition to beautiful medium-wide 3/4 side angle (8s move, 2s settle = 10s)
        # Use individual property animation to guarantee rotation_z is NEVER interpolated or tilted
        camera.animate('x', 6, duration=10.0, curve=curve.in_out_sine)
        camera.animate('y', 2.5, duration=10.0, curve=curve.in_out_sine)
        camera.animate('z', 3, duration=10.0, curve=curve.in_out_sine)
        camera.animate('rotation_x', 5, duration=10.0, curve=curve.in_out_sine)
        camera.animate('rotation_y', -45, duration=10.0, curve=curve.in_out_sine)
        camera.rotation_z = 0
        
        # 5. Dialogue UI
        # Use an unscaled container so Text entities do not inherit distorted scale
        self.dialogue_container = Entity(parent=camera.ui, enabled=False)
        self.dialogue_bg = Entity(parent=self.dialogue_container, model='quad', scale=(1.4, 0.25), position=(0, -0.35), color=color.rgba(0, 0, 0, 0.85))
        self.dialogue_name = Text(parent=self.dialogue_container, text="TEACHER", origin=(-0.5, 0.5), position=(-0.65, -0.25), color=color.gold, scale=1.2)
        self.dialogue_text = Text(parent=self.dialogue_container, text="", origin=(-0.5, 0.5), position=(-0.65, -0.32), color=color.white, scale=1.3)
        
        import textwrap
        def set_dialogue(text):
            self.dialogue_container.enabled = True
            self.dialogue_text.text = '\n'.join(textwrap.wrap(text, width=55))
            
        def hide_dialogue():
            self.dialogue_container.enabled = False
        def spawn_firework(target_pos, c, size='medium'):
            if not getattr(self, 'victory_overlay_shown', False): return
            import random
            import math
            
            # Launch phase - single rocket entity
            fw = Entity(parent=self, model='sphere', color=c, scale=0.3, position=target_pos + Vec3(0, -8, 0))
            self.graduation_props.append(fw)
            fw.animate_position(target_pos, duration=0.7, curve=curve.out_expo)
            
            # Static trail dots (no recursive spawning)
            for i in range(3):
                t = Entity(parent=self, model='sphere', color=c, scale=0.12,
                           position=target_pos + Vec3(0, -8 + i * 2.5, 0))
                self.graduation_props.append(t)
                t.animate_color(color.clear, duration=0.5)
                destroy(t, delay=0.5)
            
            # Explode after rocket arrives
            def explode():
                if not getattr(self, 'victory_overlay_shown', False):
                    return
                fw.enabled = False
                destroy(fw, delay=0.1)
                
                # Flash
                flash = Entity(parent=self, model='sphere', color=color.white, scale=2, position=target_pos)
                self.graduation_props.append(flash)
                flash.animate_scale(0, duration=0.2)
                destroy(flash, delay=0.2)
                
                # Particles - keep count LOW to avoid freeze
                num = 8 if size == 'small' else (12 if size == 'medium' else 20)
                spread = 3 if size == 'small' else (5 if size == 'medium' else 8)
                
                for i in range(num):
                    angle_h = (i / num) * math.pi * 2
                    angle_v = random.uniform(-0.5, 0.5)
                    dx = math.cos(angle_h) * spread * random.uniform(0.6, 1.0)
                    dy = math.sin(angle_v) * spread * random.uniform(0.6, 1.0)
                    dz = math.sin(angle_h) * spread * random.uniform(0.6, 1.0)
                    
                    p = Entity(parent=self, model='quad', billboard=True, color=c,
                               scale=random.uniform(0.15, 0.4), position=target_pos)
                    self.graduation_props.append(p)
                    p.animate_position(target_pos + Vec3(dx, dy, dz), duration=1.2, curve=curve.out_expo)
                    p.animate_color(color.clear, duration=1.2)
                    destroy(p, delay=1.2)
                    
            invoke(explode, delay=0.7)
            
        def spawn_background_firework():
            if not getattr(self, 'victory_overlay_shown', False) or not getattr(self, 'can_continue', False):
                return
            import random
            x = random.uniform(-10, 10)
            y = random.uniform(10, 16)
            z = random.uniform(14, 20)
            c = random.choice([color.gold, color.rgb(1, 0.2, 0.2), color.blue, color.cyan, color.white, color.rgb(0.6, 0, 0.8)])
            size = random.choice(['small', 'medium'])
            spawn_firework(Vec3(x, y, z), c, size)
            invoke(spawn_background_firework, delay=random.uniform(1.0, 2.5))
            
        def show_victory():
            camera.rotation_z = 0 # Fix any camera tilt immediately upon transitioning
            self.victory_bg = Entity(parent=camera.ui, model='quad', scale=(2, 1.2), color=color.rgba(0, 0, 0, 0.85), z=1)
            self.victory_title = Text(parent=camera.ui, text="CONGRATULATIONS!", origin=(0, 0), scale=4, position=(0, 0.25), color=color.gold, z=0)
            self.victory_sub1 = Text(parent=camera.ui, text="600 STEPS COMPLETED", origin=(0, 0), scale=2, position=(0, 0.05), color=color.white, z=0)
            self.victory_sub2 = Text(parent=camera.ui, text="You completed all\nlearning steps!", origin=(0, 0), scale=1.5, position=(0, -0.15), color=color.light_gray, z=0)
            self.victory_btn = Text(parent=camera.ui, text="[ PRESS ENTER TO CONTINUE ]", origin=(0, 0), scale=1.5, position=(0, -0.35), color=color.azure, z=0)
            self.can_continue = True
            
        self.can_continue = False
        
        def zoom_out_camera():
            camera.animate('x', 12, duration=3.0, curve=curve.in_out_sine)
            camera.animate('y', 6, duration=3.0, curve=curve.in_out_sine)
            camera.animate('z', -3, duration=3.0, curve=curve.in_out_sine)
            camera.animate('rotation_x', 10, duration=3.0, curve=curve.in_out_sine)
            camera.animate('rotation_y', -50, duration=3.0, curve=curve.in_out_sine)
            camera.rotation_z = 0

        self.ceremony_seq = Sequence(
            Wait(10.0), # Wait for the 10s camera pan to complete
            Func(set_dialogue, "Congratulations!"),
            Wait(1.5),
            Func(set_dialogue, "You've completed all 600 learning steps."),
            Wait(2.0),
            Func(set_dialogue, "I've watched you learn, practice, make mistakes, and keep going."),
            Wait(2.5),
            Func(set_dialogue, "Today, you proved that you could finish what you started."),
            Func(spawn_firework, Vec3(8, 10, 16), color.cyan, 'small'),
            Wait(2.5),
            Func(set_dialogue, "Be proud of yourself. You earned this moment."),
            Wait(2.0),
            Func(set_dialogue, "Congratulations on completing your 600-step journey!"),
            # Tăng dần
            Wait(2.5), # Hold final message
            Func(hide_dialogue),
            Func(zoom_out_camera),
            Wait(0.5), # Brief pause while camera is zooming out
            
            # Cao trào
            Func(spawn_firework, Vec3(0, 16, 18), color.gold, 'large'),
            Wait(0.4),
            Func(spawn_firework, Vec3(-8, 13, 16), color.cyan, 'large'),
            Wait(0.4),
            Func(spawn_firework, Vec3(8, 15, 17), color.rgb(150/255, 0/255, 200/255), 'large'),
            Wait(0.4),
            Func(spawn_firework, Vec3(-4, 17, 18), color.white, 'large'),
            Wait(0.4),
            Func(spawn_firework, Vec3(4, 14, 16), color.rgb(255/255, 50/255, 50/255), 'large'),
            Wait(1.5),
            
            Func(show_victory),
            Func(spawn_background_firework)
        )
        self.ceremony_seq.start()
        
    def input(self, key: str) -> None:
        """Handle global scene inputs."""
        if getattr(self, 'can_continue', False) and key in ('enter', 'return'):
            self.end_graduation_sequence()
            
    def end_graduation_sequence(self) -> None:
        """Clean up cinematic and restore normal gameplay."""
        
        # Destroy stage, podium, and teacher
        for prop in self.graduation_props:
            destroy(prop)
        self.graduation_props.clear()
        destroy(self.teacher)
        
        # Destroy UI
        destroy(self.dialogue_container)
        destroy(self.victory_bg)
        destroy(self.victory_title)
        destroy(self.victory_sub1)
        destroy(self.victory_sub2)
        destroy(self.victory_btn)
        
        self.can_continue = False
        self.victory_overlay_shown = False
        self.game_completed = False # Resume update loop
        
        # Restore player state
        if hasattr(self, 'original_player_pos'):
            self.player_controller.player.position = self.original_player_pos
        if hasattr(self, 'original_player_rot'):
            self.player_controller.player.model_pivot.rotation_y = self.original_player_rot
        
        # Cancel any lingering camera animations before restoring gameplay camera
        camera.animate_position(camera.position, duration=0)  # cancel active pos anim
        camera.animate_rotation(camera.rotation, duration=0)  # cancel active rot anim
        
        # Snap camera to correct gameplay position BEFORE re-enabling PlayerCamera
        desired_pos = self.player_controller.player.position + self.player_camera.offset
        camera.position = desired_pos
        camera.rotation = (0, 0, 0)
        camera.look_at(self.player_controller.player.position + Vec3(0, 1.5, 0))
        camera.rotation_z = 0  # Guarantee no roll
        
        self.player_camera.is_cinematic = False  # Now safe to resume follow camera
        if hasattr(self, 'ambient_life'):
            self.ambient_life.set_enabled(True)
        
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
        
        # Stop gameplay progression if the game has ended
        if getattr(self, 'game_completed', False):
            return
            
        # If dialogue is active, freeze player and interaction
        if self.dialogue_manager.is_active:
            self.dialogue_manager.update()
            return
            
        self.player_controller.update(delta_time)
        self.player_camera.update(delta_time)
        self.interaction_manager.update()
        if hasattr(self, 'ambient_life'):
            self.ambient_life.update(delta_time)

    def on_exit(self) -> None:
        """Called when leaving the campus."""
        # Ensure UI prompt is hidden
        self.interaction_manager.prompt.enabled = False
        self.interaction_manager.locked_panel.enabled = False
        self.interaction_manager.locked_text.enabled = False
