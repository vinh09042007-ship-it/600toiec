from ursina import Entity, Text, color, invoke

class NotificationUI:
    """
    Handles displaying temporary slide-in/fade-out notifications.
    """
    def __init__(self, camera_ui):
        self.camera_ui = camera_ui
        self.bg = Entity(
            parent=camera_ui,
            model='quad',
            color=color.rgba(0, 0, 0, 0.85),
            scale=(0.8, 0.15),
            position=(0, 0.35),
            enabled=False
        )
        
        self.text = Text(
            parent=camera_ui,
            text=" ",
            position=(0, 0.35),
            origin=(0, 0),
            scale=1.5,
            color=color.gold,
            enabled=False
        )
        self.text.wordwrap = 40
        
    def show(self, message: str, duration: float = 3.0):
        """Displays a notification for a set duration."""
        self.text.text = message
        
        num_lines = message.count('\n') + 1
        if num_lines > 2:
            self.bg.scale = (0.9, 0.15 + (num_lines * 0.05))
            duration = max(duration, num_lines * 0.8)
        else:
            self.bg.scale = (0.8, 0.15)
            
        self.bg.enabled = True
        self.text.enabled = True
        
        # Auto-hide after duration
        invoke(self.hide, delay=duration)
        
    def hide(self):
        self.bg.enabled = False
        self.text.enabled = False
