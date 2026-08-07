from ursina import Entity, Text, color, Sequence, Wait, Func, destroy, curve

class CertificateCard(Entity):
    """
    Handles the Achievement Badge and Certificate animations.
    """
    def __init__(self, camera_ui, final_score: int):
        super().__init__(parent=camera_ui)
        self.final_score = final_score
        
        # 1. Badge
        self.badge_container = Entity(parent=self, enabled=False)
        self.badge_text = Text(
            parent=self.badge_container,
            text="🏆 TOEIC GOAL ACHIEVED 🏆",
            origin=(0, 0),
            position=(0, 0),
            scale=0.1,
            color=color.rgba(255, 215, 0, 0)
        )
        
        # 2. Certificate
        self.cert_container = Entity(
            parent=self,
            model='quad',
            color=color.rgba(255, 250, 240, 0), # Off-white parchment
            scale=(0.8, 0.6),
            position=(0, -1.0), # Start below screen
            enabled=False
        )
        
        cert_content = (
            "==================================\n\n"
            "TOEIC GOAL ACHIEVED\n\n"
            "Target Score\n600\n\n"
            f"Final Score\n{final_score}\n\n"
            "Congratulations!\n"
            "You successfully completed\n"
            "your TOEIC learning journey.\n\n"
            "=================================="
        )
        
        self.cert_text = Text(
            parent=self.cert_container,
            text=cert_content,
            origin=(0, 0),
            position=(0, 0),
            scale=1.5,
            color=color.rgba(0, 0, 0, 0) # Black text
        )

    def show_badge(self, duration: float = 3.0, on_complete: callable = None):
        self.badge_container.enabled = True
        
        # Animate Badge
        self.badge_text.animate_scale(4, duration=0.8, curve=curve.out_elastic)
        self.badge_text.animate_color(color.gold, duration=0.5)
        
        # Simulate a shine with color oscillation could be done, but we'll stick to basic glow
        
        Sequence(
            Wait(duration),
            Func(self._fade_out_badge, on_complete)
        ).start()
        
    def _fade_out_badge(self, on_complete: callable = None):
        self.badge_text.animate_color(color.rgba(255, 215, 0, 0), duration=1.0)
        if on_complete:
            Sequence(Wait(1.0), Func(on_complete)).start()

    def show_certificate(self, duration: float = 5.0, on_complete: callable = None):
        self.cert_container.enabled = True
        
        # Slide up and fade in
        self.cert_container.animate_position((0, 0), duration=1.5, curve=curve.out_expo)
        self.cert_container.animate_color(color.rgba(255, 250, 240, 0.95), duration=1.5)
        self.cert_text.animate_color(color.black, duration=1.5)
        
        Sequence(
            Wait(duration + 1.5),
            Func(self._fade_out_certificate, on_complete)
        ).start()

    def _fade_out_certificate(self, on_complete: callable = None):
        self.cert_container.animate_color(color.rgba(255, 250, 240, 0), duration=1.0)
        self.cert_text.animate_color(color.rgba(0, 0, 0, 0), duration=1.0)
        self.cert_container.animate_position((0, -1.0), duration=1.0)
        if on_complete:
            Sequence(Wait(1.0), Func(on_complete)).start()
