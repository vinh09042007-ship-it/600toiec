from ursina import Entity, Text, color, invoke

class NotificationUI:
    """
    Handles displaying temporary slide-in/fade-out notifications.
    """
    def __init__(self, camera_ui):
        self.bg = Entity(
            parent=camera_ui,
            model='quad',
            color=color.rgba(0, 0, 0, 0.8),
            scale=(0.6, 0.2),
            position=(0, 0.35),
            enabled=False
        )
        
        self.text = Text(
            parent=self.bg,
            text="",
            origin=(0, 0),
            scale=3,
            color=color.gold
        )
        
    def show(self, message: str, duration: float = 3.0):
        """Displays a notification for a set duration."""
        self.text.text = message
        self.bg.enabled = True
        
        # Auto-hide after duration
        invoke(self.hide, delay=duration)
        
    def hide(self):
        self.bg.enabled = False
