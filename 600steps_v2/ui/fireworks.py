from ursina import Entity, color, time, destroy, camera
import random
import math

class FireworkParticle(Entity):
    def __init__(self, position, color_choice, velocity, **kwargs):
        super().__init__(
            model='sphere',
            position=position,
            scale=(0.1, 0.1, 0.1),
            color=color_choice,
            **kwargs
        )
        self.velocity = velocity
        self.lifetime = random.uniform(0.5, 1.5)
        self.spawn_time = time.time()
        
    def update(self):
        dt = time.dt
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        self.z += self.velocity[2] * dt
        
        # Gravity effect
        self.velocity = (self.velocity[0], self.velocity[1] - (9.8 * dt), self.velocity[2])
        
        # Fade out
        life_ratio = (time.time() - self.spawn_time) / self.lifetime
        self.color = color.rgba(self.color.r, self.color.g, self.color.b, max(0, 1 - life_ratio))
        
        if time.time() - self.spawn_time > self.lifetime:
            destroy(self)

class FireworksManager(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spawn_rate = 1.0 # One firework explosion per second
        self.last_spawn = time.time()
        self.colors = [color.red, color.gold, color.cyan, color.magenta, color.green]
        
    def update(self):
        if time.time() - self.last_spawn > 1.0 / self.spawn_rate:
            self.last_spawn = time.time()
            self._explode()
            
    def _explode(self):
        # Explosion position
        pos = (self.x + random.uniform(-15, 15), self.y + random.uniform(10, 20), self.z + random.uniform(5, 15))
        c = random.choice(self.colors)
        
        # Simple camera shake
        if hasattr(camera, 'shake'):
            camera.shake(duration=0.2, magnitude=0.05)
            
        for _ in range(30):
            # Spherical velocity
            theta = random.uniform(0, 2 * math.pi)
            phi = random.uniform(0, math.pi)
            speed = random.uniform(2, 8)
            
            vx = speed * math.sin(phi) * math.cos(theta)
            vy = speed * math.sin(phi) * math.sin(theta)
            vz = speed * math.cos(phi)
            
            FireworkParticle(position=pos, color_choice=c, velocity=(vx, vy, vz), parent=self.parent)
