from ursina import Entity, Text, color, Sequence, Wait, Func, destroy, curve
import time

class GoalCelebration(Entity):
    """
    Handles the animated Title and the Final Message crawl.
    """
    def __init__(self, camera_ui, final_score: int):
        super().__init__(parent=camera_ui)
        
        self.final_score = final_score
        
        # 1. Title Container
        self.title_container = Entity(parent=self, enabled=False)
        
        self.congrats_text = Text(
            parent=self.title_container,
            text="🎉 CONGRATULATIONS! 🎉",
            origin=(0, 0),
            position=(0, 0.25),
            scale=0.1, # Start small for scale-in
            color=color.rgba(255, 215, 0, 0)
        )
        
        self.sub_text = Text(
            parent=self.title_container,
            text="You reached your TOEIC goal!",
            origin=(0, 0),
            position=(0, 0.1),
            scale=0.1,
            color=color.rgba(255, 255, 255, 0)
        )
        
        self.target_text = Text(
            parent=self.title_container,
            text="Target Score: 600",
            origin=(0, 0),
            position=(0, 0),
            scale=0.1,
            color=color.rgba(0, 255, 255, 0)
        )
        
        self.score_text = Text(
            parent=self.title_container,
            text=f"Final Score: {final_score}",
            origin=(0, 0),
            position=(0, -0.1),
            scale=0.1,
            color=color.rgba(0, 255, 0, 0)
        )
        
        # 2. Final Message Container
        self.message_container = Entity(parent=self, enabled=False)
        self.message_text = Text(
            parent=self.message_container,
            text="Every lesson,\nevery challenge,\nand every step\nbrought you closer\nto your goal.\n\nCongratulations.\n\nKeep learning.\nKeep growing.\nYour journey continues.",
            origin=(0, 0),
            position=(0, 0),
            scale=2,
            color=color.rgba(255, 255, 255, 0)
        )

    def show_title(self, duration: float = 4.0, on_complete: callable = None):
        self.title_container.enabled = True
        
        # Animate Title (Fade in, scale in, bounce)
        self.congrats_text.animate_scale(4, duration=0.8, curve=curve.out_elastic)
        self.congrats_text.animate_color(color.gold, duration=0.5)
        
        Sequence(
            Wait(0.5),
            Func(self.sub_text.animate_scale, 2, duration=0.5, curve=curve.out_elastic),
            Func(self.sub_text.animate_color, color.white, duration=0.3),
            Wait(0.5),
            Func(self.target_text.animate_scale, 2, duration=0.5, curve=curve.out_elastic),
            Func(self.target_text.animate_color, color.cyan, duration=0.3),
            Wait(0.5),
            Func(self.score_text.animate_scale, 3, duration=0.5, curve=curve.out_elastic),
            Func(self.score_text.animate_color, color.green, duration=0.3),
            Wait(duration),
            Func(self._fade_out_title, on_complete)
        ).start()
        
    def _fade_out_title(self, on_complete: callable = None):
        self.congrats_text.animate_color(color.rgba(255, 215, 0, 0), duration=1.0)
        self.sub_text.animate_color(color.rgba(255, 255, 255, 0), duration=1.0)
        self.target_text.animate_color(color.rgba(0, 255, 255, 0), duration=1.0)
        self.score_text.animate_color(color.rgba(0, 255, 0, 0), duration=1.0)
        
        if on_complete:
            Sequence(Wait(1.0), Func(on_complete)).start()

    def show_final_message(self, on_complete: callable = None):
        self.message_container.enabled = True
        
        # Slow fade in
        self.message_text.animate_color(color.white, duration=3.0)
        
        if on_complete:
            Sequence(Wait(3.0), Func(on_complete)).start()
