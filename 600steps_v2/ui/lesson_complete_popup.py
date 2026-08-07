from ursina import Entity, Text, color, held_keys, camera, destroy, Sequence, Wait, Func
import time

class LessonCompletePopup(Entity):
    """
    Displays a centered completion popup after finishing a non-exam lesson.
    """
    def __init__(self, camera_ui, title: str, score: int, total: int, next_lesson: str, on_close: callable):
        super().__init__(parent=camera_ui)
        self.on_close = on_close
        
        # Dark semi-transparent background
        self.bg = Entity(
            parent=self,
            model='quad',
            color=color.rgba(0, 0, 0, 0),
            scale=(1.5, 1.0),
            position=(0, 0)
        )
        
        # Elements (start fully transparent)
        self.header_text = Text(
            parent=self.bg,
            text="Lesson Complete!",
            origin=(0, 0),
            position=(0, 0.35),
            scale=3,
            color=color.rgba(0, 255, 0, 0)
        )
        
        self.title_text = Text(
            parent=self.bg,
            text=title,
            origin=(0, 0),
            position=(0, 0.20),
            scale=4,
            color=color.rgba(255, 215, 0, 0)
        )
        
        self.score_text = Text(
            parent=self.bg,
            text=f"Score:\n{score} / {total} Correct",
            origin=(0, 0),
            position=(0, -0.05),
            scale=2,
            color=color.rgba(255, 255, 255, 0)
        )
        
        if next_lesson:
            self.next_unlocked_header = Text(
                parent=self.bg,
                text="Next Lesson Unlocked",
                origin=(0, 0),
                position=(0, -0.25),
                scale=1.5,
                color=color.rgba(0, 255, 255, 0)
            )
            self.next_unlocked_text = Text(
                parent=self.bg,
                text=next_lesson,
                origin=(0, 0),
                position=(0, -0.32),
                scale=2,
                color=color.rgba(255, 255, 255, 0)
            )
        else:
            self.next_unlocked_header = None
            self.next_unlocked_text = None
            
        self.instruction_text = Text(
            parent=self.bg,
            text="[ENTER] Continue",
            origin=(0, 0),
            position=(0, -0.45),
            scale=1.5,
            color=color.rgba(200, 200, 200, 0)
        )
        
        # Fade in animation
        self.bg.animate_color(color.rgba(0, 0, 0, 0.9), duration=0.5)
        self.header_text.animate_color(color.green, duration=0.5)
        self.title_text.animate_color(color.gold, duration=0.5)
        self.score_text.animate_color(color.white, duration=0.5)
        if self.next_unlocked_header:
            self.next_unlocked_header.animate_color(color.cyan, duration=0.5)
            self.next_unlocked_text.animate_color(color.white, duration=0.5)
        self.instruction_text.animate_color(color.light_gray, duration=0.5)
        
        self.creation_time = time.time()
        self.is_closing = False

    def update(self):
        # Prevent instant closing on pop up (handled in input now, but keeping creation_time check)
        pass
        
    def input(self, key: str):
        if time.time() - self.creation_time < 0.5:
            return
            
        if key == 'enter' or key == 'e':
            self.close_popup()
            return
            
    def close_popup(self):
        if self.is_closing:
            return
            
        self.is_closing = True
        
        # Fade out
        self.bg.animate_color(color.rgba(0, 0, 0, 0), duration=0.3)
        self.header_text.animate_color(color.rgba(0, 255, 0, 0), duration=0.3)
        self.title_text.animate_color(color.rgba(255, 215, 0, 0), duration=0.3)
        self.score_text.animate_color(color.rgba(255, 255, 255, 0), duration=0.3)
        if self.next_unlocked_header:
            self.next_unlocked_header.animate_color(color.rgba(0, 255, 255, 0), duration=0.3)
            self.next_unlocked_text.animate_color(color.rgba(255, 255, 255, 0), duration=0.3)
        self.instruction_text.animate_color(color.rgba(200, 200, 200, 0), duration=0.3)
            
        Sequence(
            Wait(0.3),
            Func(self._finish_close)
        ).start()
            
    def _finish_close(self):
        if self.on_close:
            self.on_close()
        destroy(self)

    @classmethod
    def show(cls, camera_ui, title: str, score: int, total: int, next_lesson: str, on_close: callable):
        return cls(camera_ui, title, score, total, next_lesson, on_close)
