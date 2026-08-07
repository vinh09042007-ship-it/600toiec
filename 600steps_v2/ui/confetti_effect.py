from ursina import Entity, color, time, destroy
import random

class ConfettiParticle(Entity):
    def __init__(self, position, **kwargs):
        super().__init__(
            model='quad',
            position=position,
            scale=(0.1, 0.1),
            color=random.choice([color.red, color.green, color.blue, color.yellow, color.magenta, color.cyan, color.gold]),
            **kwargs
        )
        self.velocity = (random.uniform(-1, 1), random.uniform(-2, -5), random.uniform(-1, 1))
        self.rotation_speed = (random.uniform(-100, 100), random.uniform(-100, 100), random.uniform(-100, 100))
        self.lifetime = random.uniform(2, 4)
        self.spawn_time = time.time()
        
    def update(self):
        dt = time.dt
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        self.z += self.velocity[2] * dt
        
        self.rotation_x += self.rotation_speed[0] * dt
        self.rotation_y += self.rotation_speed[1] * dt
        self.rotation_z += self.rotation_speed[2] * dt
        
        if time.time() - self.spawn_time > self.lifetime:
            destroy(self)

class ConfettiSpawner(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spawn_rate = 20 # particles per second
        self.last_spawn = time.time()
        
    def update(self):
        if time.time() - self.last_spawn > 1.0 / self.spawn_rate:
            self.last_spawn = time.time()
            # Spawn slightly above the camera/player
            pos = (self.x + random.uniform(-10, 10), self.y + 10, self.z + random.uniform(-5, 5))
            ConfettiParticle(position=pos, parent=self.parent)
