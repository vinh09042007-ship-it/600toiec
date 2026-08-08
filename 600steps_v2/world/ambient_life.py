import random
import math
from ursina import Entity, color, time, Vec3, destroy

class AmbientNPC(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Randomize colors and scale
        skin_colors = [color.rgb(255, 205, 175), color.rgb(141, 85, 36), color.rgb(198, 134, 66), color.rgb(224, 172, 105), color.rgb(241, 194, 125)]
        shirt_colors = [color.red, color.blue, color.green, color.yellow, color.cyan, color.magenta, color.orange, color.white, color.gray]
        pant_colors = [color.dark_gray, color.black, color.rgb(40, 40, 80), color.rgb(100, 100, 100)]
        
        skin_color = random.choice(skin_colors)
        shirt_color = random.choice(shirt_colors)
        pant_color = random.choice(pant_colors)
        scale_variance = random.uniform(0.9, 1.1)
        self.scale = scale_variance
        
        body_scale = (0.8, 1.2, 0.4)
        head_scale = (0.5, 0.5, 0.5)
        arm_scale = (0.2, 1.0, 0.2)
        leg_scale = (0.3, 1.2, 0.3)
        
        # Parent pivot for animation
        self.model_pivot = Entity(parent=self, position=(0, 1, 0))
        
        self.head = Entity(parent=self.model_pivot, model='cube', color=skin_color, scale=head_scale, position=(0, 1.0, 0))
        self.body = Entity(parent=self.model_pivot, model='cube', color=shirt_color, scale=body_scale, position=(0, 0.15, 0))
        
        self.left_arm = Entity(parent=self.model_pivot, model='cube', color=shirt_color, scale=arm_scale, position=(-0.55, 0.25, 0))
        self.right_arm = Entity(parent=self.model_pivot, model='cube', color=shirt_color, scale=arm_scale, position=(0.55, 0.25, 0))
        
        self.left_leg = Entity(parent=self.model_pivot, model='cube', color=pant_color, scale=leg_scale, position=(-0.25, -1.05, 0))
        self.right_leg = Entity(parent=self.model_pivot, model='cube', color=pant_color, scale=leg_scale, position=(0.25, -1.05, 0))
        
        # Optional hair
        if random.random() > 0.3:
            hair_colors = [color.black, color.gray, color.rgb(139, 69, 19), color.rgb(210, 180, 140)]
            self.hair = Entity(parent=self.head, model='cube', color=random.choice(hair_colors), scale=(1.05, 0.3, 1.05), position=(0, 0.4, 0))
        
        # State
        self.state = "IDLE"
        self.target_pos = None
        self.speed = random.uniform(2.0, 3.0)
        self.idle_timer = 0
        self.anim_time = random.uniform(0, 10)
        
    def set_destination(self, target):
        self.target_pos = target
        self.state = "WALKING"
        # Face target
        if self.target_pos:
            dx = self.target_pos.x - self.x
            dz = self.target_pos.z - self.z
            target_y_rotation = math.degrees(math.atan2(dx, dz))
            self.rotation_y = target_y_rotation

    def update_logic(self, dt):
        if self.state == "IDLE":
            self.idle_timer -= dt
            self.left_leg.position = (-0.25, -1.05, 0)
            self.right_leg.position = (0.25, -1.05, 0)
            self.left_arm.position = (-0.55, 0.25, 0)
            self.right_arm.position = (0.55, 0.25, 0)
            if self.idle_timer <= 0:
                self.state = "NEEDS_DESTINATION"
        
        elif self.state == "WALKING" and self.target_pos:
            # Move towards target
            dir_vec = self.target_pos - self.position
            dist = dir_vec.length()
            if dist < 0.2:
                self.state = "IDLE"
                self.idle_timer = random.uniform(2.0, 4.0)
                self.target_pos = None
            else:
                dir_vec = dir_vec.normalized()
                self.position += dir_vec * self.speed * dt
                
                # Animation
                self.anim_time += dt * self.speed * 4
                swing = math.sin(self.anim_time) * 0.3
                self.left_leg.position = (-0.25, -1.05, swing)
                self.right_leg.position = (0.25, -1.05, -swing)
                self.left_arm.position = (-0.55, 0.25, -swing)
                self.right_arm.position = (0.55, 0.25, swing)

class AmbientDog(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        dog_colors = [color.rgb(139, 69, 19), color.rgb(205, 133, 63), color.rgb(245, 222, 179), color.white, color.gray]
        c = random.choice(dog_colors)
        
        self.scale = random.uniform(0.7, 1.0)
        self.model_pivot = Entity(parent=self, position=(0, 0.5, 0))
        
        self.body = Entity(parent=self.model_pivot, model='cube', color=c, scale=(0.4, 0.4, 0.8), position=(0, 0, 0))
        self.head = Entity(parent=self.model_pivot, model='cube', color=c, scale=(0.3, 0.3, 0.3), position=(0, 0.3, 0.4))
        
        leg_scale = (0.1, 0.4, 0.1)
        self.fl_leg = Entity(parent=self.model_pivot, model='cube', color=c, scale=leg_scale, position=(-0.15, -0.2, 0.3))
        self.fr_leg = Entity(parent=self.model_pivot, model='cube', color=c, scale=leg_scale, position=(0.15, -0.2, 0.3))
        self.bl_leg = Entity(parent=self.model_pivot, model='cube', color=c, scale=leg_scale, position=(-0.15, -0.2, -0.3))
        self.br_leg = Entity(parent=self.model_pivot, model='cube', color=c, scale=leg_scale, position=(0.15, -0.2, -0.3))
        
        self.tail = Entity(parent=self.model_pivot, model='cube', color=c, scale=(0.05, 0.3, 0.05), position=(0, 0.1, -0.4))
        
        self.state = "IDLE"
        self.target_pos = None
        self.speed = random.uniform(1.0, 1.5)
        self.idle_timer = 0
        self.anim_time = random.uniform(0, 10)
        
    def set_destination(self, target):
        self.target_pos = target
        self.state = "WALKING"
        if self.target_pos:
            dx = self.target_pos.x - self.x
            dz = self.target_pos.z - self.z
            self.rotation_y = math.degrees(math.atan2(dx, dz))

    def update_logic(self, dt):
        if self.state == "IDLE":
            self.idle_timer -= dt
            # Tail wag
            self.anim_time += dt * 5
            self.tail.rotation_z = math.sin(self.anim_time) * 20
            
            self.fl_leg.position = (-0.15, -0.2, 0.3)
            self.fr_leg.position = (0.15, -0.2, 0.3)
            self.bl_leg.position = (-0.15, -0.2, -0.3)
            self.br_leg.position = (0.15, -0.2, -0.3)
            
            if self.idle_timer <= 0:
                self.state = "NEEDS_DESTINATION"
        elif self.state == "WALKING" and self.target_pos:
            dir_vec = self.target_pos - self.position
            dist = dir_vec.length()
            if dist < 0.2:
                self.state = "IDLE"
                self.idle_timer = random.uniform(2.0, 5.0)
                self.target_pos = None
            else:
                dir_vec = dir_vec.normalized()
                self.position += dir_vec * self.speed * dt
                
                self.anim_time += dt * self.speed * 8
                swing = math.sin(self.anim_time) * 0.1
                self.fl_leg.position = (-0.15, -0.2, 0.3 + swing)
                self.fr_leg.position = (0.15, -0.2, 0.3 - swing)
                self.bl_leg.position = (-0.15, -0.2, -0.3 - swing)
                self.br_leg.position = (0.15, -0.2, -0.3 + swing)
                
                self.tail.rotation_z = math.sin(self.anim_time * 0.5) * 10

class AmbientCat(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cat_colors = [color.black, color.white, color.gray, color.orange, color.rgb(139, 69, 19)]
        c = random.choice(cat_colors)
        
        self.scale = random.uniform(0.6, 0.8)
        self.model_pivot = Entity(parent=self, position=(0, 0.4, 0))
        
        self.body = Entity(parent=self.model_pivot, model='cube', color=c, scale=(0.25, 0.25, 0.5), position=(0, 0, 0))
        self.head = Entity(parent=self.model_pivot, model='cube', color=c, scale=(0.2, 0.2, 0.2), position=(0, 0.15, 0.25))
        
        # Ears (triangular, using quads/cubes approximated)
        self.l_ear = Entity(parent=self.head, model='cube', color=c, scale=(0.2, 0.4, 0.1), position=(-0.25, 0.4, 0))
        self.r_ear = Entity(parent=self.head, model='cube', color=c, scale=(0.2, 0.4, 0.1), position=(0.25, 0.4, 0))
        
        leg_scale = (0.08, 0.3, 0.08)
        self.fl_leg = Entity(parent=self.model_pivot, model='cube', color=c, scale=leg_scale, position=(-0.1, -0.15, 0.2))
        self.fr_leg = Entity(parent=self.model_pivot, model='cube', color=c, scale=leg_scale, position=(0.1, -0.15, 0.2))
        self.bl_leg = Entity(parent=self.model_pivot, model='cube', color=c, scale=leg_scale, position=(-0.1, -0.15, -0.2))
        self.br_leg = Entity(parent=self.model_pivot, model='cube', color=c, scale=leg_scale, position=(0.1, -0.15, -0.2))
        
        self.tail = Entity(parent=self.model_pivot, model='cube', color=c, scale=(0.04, 0.3, 0.04), position=(0, 0.1, -0.25))
        self.tail.rotation_x = -30
        
        self.state = "IDLE"
        self.target_pos = None
        self.speed = random.uniform(1.0, 1.5)
        self.idle_timer = 0
        self.anim_time = random.uniform(0, 10)
        
    def set_destination(self, target):
        self.target_pos = target
        self.state = "WALKING"
        if self.target_pos:
            dx = self.target_pos.x - self.x
            dz = self.target_pos.z - self.z
            self.rotation_y = math.degrees(math.atan2(dx, dz))

    def update_logic(self, dt):
        if self.state == "IDLE":
            self.idle_timer -= dt
            self.anim_time += dt * 2
            self.tail.rotation_z = math.sin(self.anim_time) * 15
            
            self.fl_leg.position = (-0.1, -0.15, 0.2)
            self.fr_leg.position = (0.1, -0.15, 0.2)
            self.bl_leg.position = (-0.1, -0.15, -0.2)
            self.br_leg.position = (0.1, -0.15, -0.2)
            
            if self.idle_timer <= 0:
                self.state = "NEEDS_DESTINATION"
        elif self.state == "WALKING" and self.target_pos:
            dir_vec = self.target_pos - self.position
            dist = dir_vec.length()
            if dist < 0.2:
                self.state = "IDLE"
                self.idle_timer = random.uniform(2.0, 5.0)
                self.target_pos = None
            else:
                dir_vec = dir_vec.normalized()
                self.position += dir_vec * self.speed * dt
                
                self.anim_time += dt * self.speed * 8
                swing = math.sin(self.anim_time) * 0.08
                self.fl_leg.position = (-0.1, -0.15, 0.2 + swing)
                self.fr_leg.position = (0.1, -0.15, 0.2 - swing)
                self.bl_leg.position = (-0.1, -0.15, -0.2 - swing)
                self.br_leg.position = (0.1, -0.15, -0.2 + swing)
                
                self.tail.rotation_z = math.sin(self.anim_time * 0.5) * 5

class AmbientBird(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        bird_colors = [color.red, color.blue, color.cyan, color.yellow, color.gray, color.white]
        c = random.choice(bird_colors)
        
        self.scale = random.uniform(0.3, 0.5)
        self.model_pivot = Entity(parent=self, position=(0, 0.2, 0))
        
        self.body = Entity(parent=self.model_pivot, model='cube', color=c, scale=(0.2, 0.2, 0.3), position=(0, 0, 0))
        self.beak = Entity(parent=self.model_pivot, model='cube', color=color.orange, scale=(0.05, 0.05, 0.1), position=(0, 0.05, 0.15))
        
        self.l_wing = Entity(parent=self.model_pivot, model='quad', color=c, scale=(0.3, 0.2), position=(-0.1, 0, 0), double_sided=True)
        self.r_wing = Entity(parent=self.model_pivot, model='quad', color=c, scale=(0.3, 0.2), position=(0.1, 0, 0), double_sided=True)
        self.l_wing.rotation_x = 90
        self.r_wing.rotation_x = 90
        
        self.state = "IDLE"
        self.target_pos = None
        self.start_pos = None
        self.fly_timer = 0
        self.fly_duration = 0
        self.idle_timer = 0
        self.anim_time = 0
        
    def set_destination(self, target):
        self.target_pos = target
        self.start_pos = Vec3(self.position)
        self.state = "FLYING"
        dist = (target - self.position).length()
        self.fly_duration = dist / random.uniform(3.0, 5.0)
        self.fly_timer = 0
        if self.target_pos:
            dx = self.target_pos.x - self.x
            dz = self.target_pos.z - self.z
            self.rotation_y = math.degrees(math.atan2(dx, dz))

    def update_logic(self, dt):
        if self.state == "IDLE":
            self.idle_timer -= dt
            self.l_wing.rotation_y = 0
            self.r_wing.rotation_y = 0
            if self.idle_timer <= 0:
                self.state = "NEEDS_DESTINATION"
                
            # Occasional hop
            if random.random() < 0.02:
                self.model_pivot.y = 0.3
            else:
                self.model_pivot.y = max(0.2, self.model_pivot.y - dt * 2)
                
        elif self.state == "FLYING" and self.target_pos:
            self.fly_timer += dt
            t = self.fly_timer / self.fly_duration
            if t >= 1.0:
                self.position = self.target_pos
                self.model_pivot.y = 0.2
                self.state = "IDLE"
                self.idle_timer = random.uniform(1.0, 4.0)
                self.target_pos = None
            else:
                # Lerp position
                curr_pos = self.start_pos + (self.target_pos - self.start_pos) * t
                self.position = curr_pos
                # Parabolic height
                self.model_pivot.y = 0.2 + math.sin(t * math.pi) * 1.5
                
                # Wing flap
                self.anim_time += dt * 30
                flap = math.sin(self.anim_time) * 45
                self.l_wing.rotation_y = flap
                self.r_wing.rotation_y = -flap

class AmbientLifeManager:
    def __init__(self, campus, world_collision, parent_entity, player):
        self.campus = campus
        self.world_collision = world_collision
        self.parent_entity = parent_entity
        self.player = player
        self.entities = []
        self.enabled = True
        
        self.spawn_entities()
        
    def spawn_entities(self):
        # 8 NPCs
        for _ in range(8):
            npc = AmbientNPC(parent=self.parent_entity)
            pos = self.get_random_valid_pos(is_animal=False)
            npc.position = pos
            npc.state = "NEEDS_DESTINATION"
            self.entities.append(npc)
            
        # 3 Dogs
        for _ in range(3):
            dog = AmbientDog(parent=self.parent_entity)
            dog.position = self.get_random_valid_pos(is_animal=True)
            dog.state = "NEEDS_DESTINATION"
            self.entities.append(dog)
            
        # 3 Cats
        for _ in range(3):
            cat = AmbientCat(parent=self.parent_entity)
            cat.position = self.get_random_valid_pos(is_animal=True)
            cat.state = "NEEDS_DESTINATION"
            self.entities.append(cat)
            
        # 4 Birds
        for _ in range(4):
            bird = AmbientBird(parent=self.parent_entity)
            bird.position = self.get_random_valid_pos(is_animal=True)
            bird.state = "NEEDS_DESTINATION"
            self.entities.append(bird)
            
    def is_pos_safe(self, x, z, is_animal):
        # Avoid graduation stage area
        if -6 <= x <= 6 and 6 <= z <= 15:
            return False
            
        # Avoid player
        if self.player:
            dist_to_player = math.sqrt((x - self.player.x)**2 + (z - self.player.z)**2)
            if dist_to_player < 3.0:
                return False
                
        # If animal, avoid roads
        if is_animal:
            # Main road
            if -3 <= x <= 3:
                return False
            # Horizontal roads
            if 18 <= z <= 22 or 48 <= z <= 52:
                return False
                
        # Check world collision
        if not self.world_collision.is_position_valid(x, z):
            return False
            
        return True
        
    def get_random_valid_pos(self, is_animal):
        for _ in range(50):
            x = random.uniform(-30, 30)
            z = random.uniform(0, 75)
            if self.is_pos_safe(x, z, is_animal):
                return Vec3(x, 0, z)
        return Vec3(0, 0, 0)
        
    def update(self, dt):
        if not self.enabled:
            return
            
        for entity in self.entities:
            if entity.state == "NEEDS_DESTINATION":
                is_animal = not isinstance(entity, AmbientNPC)
                target = self.get_random_valid_pos(is_animal)
                # Ensure the path distance is reasonable (not too far)
                curr_dist = (target - entity.position).length()
                if curr_dist > 20:
                    dir_vec = (target - entity.position).normalized()
                    target = entity.position + dir_vec * random.uniform(5, 15)
                    # Re-check safety for truncated target
                    if not self.is_pos_safe(target.x, target.z, is_animal):
                        # If truncated target isn't safe, just use the original valid pos 
                        # or force idle this turn
                        target = None 
                
                if target:
                    entity.set_destination(target)
                else:
                    entity.state = "IDLE"
                    entity.idle_timer = random.uniform(1.0, 3.0)
                    
            if hasattr(entity, 'update_logic'):
                entity.update_logic(dt)
                
    def set_enabled(self, enabled):
        self.enabled = enabled
        for e in self.entities:
            e.enabled = enabled
            
    def destroy(self):
        for e in self.entities:
            destroy(e)
        self.entities.clear()
