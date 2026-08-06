"""
Question framework scene for TOEIC gameplay.
"""
from ursina import Entity, Text, color, held_keys, camera, invoke, destroy
from .base_scene import BaseScene

class QuestionScene(BaseScene):
    """
    Reusable scene that displays questions for any building.
    Currently uses a hardcoded temporary question.
    """
    
    def __init__(self, scene_manager, **kwargs):
        self.scene_manager = scene_manager
        super().__init__(**kwargs)
        
    def setup(self) -> None:
        """Initialize UI elements."""
        
        # UI Elements
        self.building_title = Text(
            text="Building Name",
            position=(0, 0.4),
            origin=(0, 0),
            scale=2.5,
            color=color.yellow,
            parent=self
        )
        
        self.question_number = Text(
            text="Question 1",
            position=(0, 0.3),
            origin=(0, 0),
            scale=1.5,
            color=color.light_gray,
            parent=self
        )
        
        self.question_text = Text(
            text="Choose the correct word.",
            position=(0, 0.15),
            origin=(0, 0),
            scale=2,
            color=color.white,
            parent=self
        )
        
        self.answer_a = Text(text="A. go", position=(-0.2, 0), scale=1.5, parent=self)
        self.answer_b = Text(text="B. goes", position=(-0.2, -0.05), scale=1.5, parent=self)
        self.answer_c = Text(text="C. going", position=(-0.2, -0.1), scale=1.5, parent=self)
        self.answer_d = Text(text="D. gone", position=(-0.2, -0.15), scale=1.5, parent=self)
        
        self.instruction_text = Text(
            text="Press 1 / 2 / 3 / 4 to answer.\nESC to return.",
            position=(0, -0.3),
            origin=(0, 0),
            scale=1.5,
            color=color.cyan,
            parent=self
        )
        
        self.feedback_text = Text(
            text="",
            position=(0, -0.45),
            origin=(0, 0),
            scale=2,
            color=color.green,
            parent=self,
            enabled=False
        )
        
        # State
        self.building_name = ""
        self.correct_answer = 2  # B
        self.has_answered = False
        
        # Debounce
        self.was_key_pressed = False

    def on_enter(self, **kwargs) -> None:
        """Setup state when entering the question scene."""
        self.building_name = kwargs.get("building_name", "Unknown")
        self.building_title.text = f"{self.building_name} Practice"
        
        # Reset state
        self.has_answered = False
        self.feedback_text.enabled = False
        self.was_key_pressed = True
        
        # Attach UI to camera
        self.building_title.parent = camera.ui
        self.question_number.parent = camera.ui
        self.question_text.parent = camera.ui
        self.answer_a.parent = camera.ui
        self.answer_b.parent = camera.ui
        self.answer_c.parent = camera.ui
        self.answer_d.parent = camera.ui
        self.instruction_text.parent = camera.ui
        self.feedback_text.parent = camera.ui

    def update_scene(self, delta_time: float) -> None:
        """Handle user input for answering and returning."""
        # Handle Return
        if held_keys['escape']:
            self.scene_manager.switch_scene("building", building_name=self.building_name)
            
        # Handle Answering
        if not self.has_answered:
            pressed_choice = None
            if held_keys['1']: pressed_choice = 1
            elif held_keys['2']: pressed_choice = 2
            elif held_keys['3']: pressed_choice = 3
            elif held_keys['4']: pressed_choice = 4
            
            if pressed_choice is not None and not self.was_key_pressed:
                self._check_answer(pressed_choice)
                
            self.was_key_pressed = pressed_choice is not None

    def _check_answer(self, choice: int) -> None:
        """Check the selected answer and display feedback."""
        self.has_answered = True
        self.feedback_text.enabled = True
        
        if choice == self.correct_answer:
            self.feedback_text.text = "Correct!"
            self.feedback_text.color = color.green
        else:
            self.feedback_text.text = "Wrong!\nCorrect Answer: B"
            self.feedback_text.color = color.red
            
        # Hide feedback after 2 seconds
        invoke(self._hide_feedback, delay=2.0)
        
    def _hide_feedback(self) -> None:
        self.feedback_text.enabled = False

    def on_exit(self) -> None:
        """Cleanup."""
        # Reparent UI texts back to self
        self.building_title.parent = self
        self.question_number.parent = self
        self.question_text.parent = self
        self.answer_a.parent = self
        self.answer_b.parent = self
        self.answer_c.parent = self
        self.answer_d.parent = self
        self.instruction_text.parent = self
        self.feedback_text.parent = self
