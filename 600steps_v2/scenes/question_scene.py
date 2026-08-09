"""
Question framework scene for TOEIC gameplay.
"""
from ursina import Entity, Text, color, held_keys, camera, invoke, destroy, time, Audio
from .base_scene import BaseScene
from core.quiz import QuestionManager
from core.score_manager import ScoreManager
from core.question_loader import QuestionLoader
from core.mini_game_manager import MiniGameManager
from ui.combo_popup import ComboPopup
from ui.rating_popup import RatingPopup
from ui.lesson_complete_popup import LessonCompletePopup
from ursina import Sequence, Wait, Func

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
        
        from ursina import window
        window.color = color.rgb(12/255, 20/255, 35/255)
        
        # UI Elements
        # Live Score UI
        self.score_text = Text(text="Score: 0", position=(-0.8, 0.45), scale=1.5, color=color.gold, parent=self)
        self.correct_text = Text(text="Correct: 0", position=(-0.8, 0.4), scale=1.5, color=color.green, parent=self)
        self.wrong_text = Text(text="Wrong: 0", position=(-0.8, 0.35), scale=1.5, color=color.red, parent=self)
        self.combo_text = Text(text="Combo: 0", position=(-0.8, 0.3), scale=1.5, color=color.cyan, parent=self)
        
        self.building_title = Text(
            text="Building Name",
            position=(0, 0.4),
            origin=(0, 0),
            scale=2.5,
            color=color.rgb(0, 230/255, 255/255),
            parent=self
        )
        
        self.question_number = Text(
            text="Question 1 / 1",
            position=(0, 0.3),
            origin=(0, 0),
            scale=1.5,
            color=color.rgb(180/255, 200/255, 215/255),
            parent=self
        )
        
        self.question_text = Text(
            text="Question text here",
            position=(0, 0.15),
            origin=(0, 0),
            scale=2,
            color=color.white,
            parent=self
        )
        
        self.context_text = Text(
            text="",
            position=(0, 0.20),
            origin=(0, 0.5), # Top-center alignment
            scale=1.2,
            color=color.light_gray,
            parent=self,
            enabled=False
        )
        
        self.answer_a = Text(text="A. ", position=(-0.2, 0), scale=1.5, color=color.white, parent=self)
        self.answer_b = Text(text="B. ", position=(-0.2, -0.05), scale=1.5, color=color.white, parent=self)
        self.answer_c = Text(text="C. ", position=(-0.2, -0.1), scale=1.5, color=color.white, parent=self)
        self.answer_d = Text(text="D. ", position=(-0.2, -0.15), scale=1.5, color=color.white, parent=self)
        
        self.instruction_text = Text(
            text="Press 1 / 2 / 3 / 4 to answer.\nESC to return.",
            position=(0, -0.3),
            origin=(0, 0),
            scale=1.5,
            color=color.rgb(0, 230/255, 255/255),
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
        
        self.result_text = Text(
            text="Practice Complete\n\nScore: 0 / 0",
            position=(0, 0),
            origin=(0, 0),
            scale=3,
            color=color.gold,
            parent=self,
            enabled=False
        )
        
        # State
        self.building_name = ""
        self.manager = None
        self.score_manager = None
        self.minigame_manager = None
        self.has_answered = False
        self.question_start_time = 0.0
        self.rating_ui = None
        self.rating_ui = None
        self.current_audio = None
        self.current_question_token = 0
        
        # Debounce
        self.was_key_pressed = False

    def _stop_audio(self) -> None:
        """Safely stops and destroys current audio to prevent overlaps/leaks."""
        if hasattr(self, 'current_audio') and self.current_audio:
            try:
                self.current_audio.stop()
            except Exception:
                pass
            from ursina import destroy
            destroy(self.current_audio)
            self.current_audio = None


    def on_enter(self, **kwargs) -> None:
        """Setup state when entering the question scene."""
        self.building_name = kwargs.get("building_name", "Unknown")
        self.building_title.text = f"{self.building_name} Practice"
        
        # Hide HUD for learning buildings, show for exam
        if hasattr(self.scene_manager, 'hud_ui'):
            if self.building_name.lower() == "exam":
                self.scene_manager.hud_ui.enable()
            else:
                self.scene_manager.hud_ui.disable()
        
        # Load questions dynamically from JSON with a limit
        category = self.building_name.lower()
        loaded_questions = QuestionLoader.load_questions(category)
        
        self.manager = QuestionManager(loaded_questions)
        total_q = self.manager.get_total_questions()
        self.score_manager = ScoreManager(total_questions=total_q)
        self.minigame_manager = MiniGameManager(total_questions=total_q)
        
        # Reset state
        self.has_answered = False
        self.feedback_text.enabled = False
        self.result_text.enabled = False
        if self.rating_ui:
            destroy(self.rating_ui)
            self.rating_ui = None
        
        self.score_text.enabled = True
        self.correct_text.enabled = True
        self.wrong_text.enabled = True
        self.combo_text.enabled = True
        
        self.building_title.enabled = True
        self.question_number.enabled = True
        self.question_text.enabled = True
        self.context_text.enabled = False
        self.answer_a.enabled = True
        self.answer_b.enabled = True
        self.answer_c.enabled = True
        self.answer_d.enabled = True
        self.instruction_text.enabled = True
        
        self.was_key_pressed = True
        
        self._update_score_ui()
        self._display_current_question()
        
        # Attach UI to camera
        self.score_text.parent = camera.ui
        self.correct_text.parent = camera.ui
        self.wrong_text.parent = camera.ui
        self.combo_text.parent = camera.ui
        
        self.building_title.parent = camera.ui
        self.question_number.parent = camera.ui
        self.question_text.parent = camera.ui
        self.context_text.parent = camera.ui
        self.answer_a.parent = camera.ui
        self.answer_b.parent = camera.ui
        self.answer_c.parent = camera.ui
        self.answer_d.parent = camera.ui
        self.instruction_text.parent = camera.ui
        self.feedback_text.parent = camera.ui
        self.result_text.parent = camera.ui

    def _display_current_question(self) -> None:
        """Updates the UI to show the current question."""
        if self.manager.is_finished():
            self._show_completion_screen()
            return
            
        q = self.manager.get_current_question()
        curr_idx = self.manager.current_index + 1
        total = self.manager.get_total_questions()
        
        self.question_number.text = f"Question {curr_idx} / {total}"
        
        category = self.building_name.lower()
        if category in ["reading", "listening", "exam"]:
            if q.context:
                prefix = "Reading Passage\n\n" if category == "reading" else ""
                if category == "exam" and not (hasattr(q, 'audio') and q.audio):
                    prefix = "Reading Passage\n\n"
                    
                self.context_text.text = prefix + q.context
                self.context_text.color = color.light_gray
                self.context_text.enabled = True
                
                # Audio playback logic
                self._stop_audio()
                
                if category in ["listening", "exam"] and hasattr(q, 'audio') and q.audio:
                    from pathlib import Path
                    audio_path = Path(__file__).resolve().parent.parent / "assets" / "audio" / "listening" / q.audio
                    
                    if audio_path.exists():
                        self.current_audio = Audio(f"assets/audio/listening/{q.audio}", autoplay=True, parent=camera.ui)
                        self.current_audio.play()
                        self.context_text.enabled = False
                    else:
                        prefix = f"[DEV WARNING: Missing audio {q.audio}]\n\n"
                        self.context_text.text = prefix + q.context
                        self.context_text.color = color.orange
                        self.context_text.enabled = True
                        
                # Shift UI down to make room
                self.question_text.position = (0, -0.05)
                self.answer_a.position = (-0.2, -0.15)
                self.answer_b.position = (-0.2, -0.2)
                self.answer_c.position = (-0.2, -0.25)
                self.answer_d.position = (-0.2, -0.3)
                self.instruction_text.position = (0, -0.4)
                
                self.question_text.text = q.text
                self.question_text.color = color.white
            else:
                self.context_text.enabled = False
                # Restore default positions
                self.question_text.position = (0, 0.15)
                self.answer_a.position = (-0.2, 0)
                self.answer_b.position = (-0.2, -0.05)
                self.answer_c.position = (-0.2, -0.1)
                self.answer_d.position = (-0.2, -0.15)
                self.instruction_text.position = (0, -0.3)
                
                self.question_text.text = "[MISSING DATA] This question requires a passage/script.\n\n" + q.text
                self.question_text.color = color.orange
        else:
            self.context_text.enabled = False
            # Restore default positions
            self.question_text.position = (0, 0.15)
            self.answer_a.position = (-0.2, 0)
            self.answer_b.position = (-0.2, -0.05)
            self.answer_c.position = (-0.2, -0.1)
            self.answer_d.position = (-0.2, -0.15)
            self.instruction_text.position = (0, -0.3)
            
            self.question_text.text = q.text
            self.question_text.color = color.white

        self.answer_a.text = f"A. {q.choices[0]}"
        self.answer_b.text = f"B. {q.choices[1]}"
        self.answer_c.text = f"C. {q.choices[2]}"
        self.answer_d.text = f"D. {q.choices[3]}"
        
        self.question_start_time = time.time()

    def _update_score_ui(self) -> None:
        """Updates the live score tracking texts."""
        self.score_text.text = f"Score: {self.score_manager.current_score}"
        self.correct_text.text = f"Correct: {self.score_manager.correct_answers}"
        self.wrong_text.text = f"Wrong: {self.score_manager.wrong_answers}"
        self.combo_text.text = f"Combo: {self.score_manager.combo_streak}"

    def _show_completion_screen(self) -> None:
        """Hides the question UI and shows the detailed final score."""
        self.score_text.enabled = False
        self.correct_text.enabled = False
        self.wrong_text.enabled = False
        self.combo_text.enabled = False
        
        self.building_title.enabled = False
        self.question_number.enabled = False
        self.question_text.enabled = False
        self.context_text.enabled = False
        self.answer_a.enabled = False
        self.answer_b.enabled = False
        self.answer_c.enabled = False
        self.answer_d.enabled = False
        self.feedback_text.enabled = False
        self.instruction_text.enabled = False
        
        # Merge session stats into the persistent global profile
        profile = self.scene_manager.player_profile
        profile.add_practice_result(self.score_manager, self.building_name)
        
        rating = self.minigame_manager.calculate_rating()
        
        is_exam = self.building_name.lower() == "exam"
        
        if is_exam:
            displayed_score = self.score_manager.correct_answers * 100
            self.exam_passed = displayed_score >= profile.target_toeic_score
            
            if self.exam_passed:
                print(f"[TRACE] QuestionScene: Exam passed, score >= {profile.target_toeic_score}")
                # Auto-complete the quest so progression saves
                if hasattr(self.scene_manager, 'quest_manager'):
                    print("[TRACE] QuestionScene: Auto-completing active exam quest")
                    qm = self.scene_manager.quest_manager
                    active_q = qm.get_active_quest()
                    if active_q and active_q.id == "exam_quest":
                        qm._complete_active_quest()
                        print("[TRACE] QuestionScene: Quest completed")
                
                # Directly transition to graduation sequence without showing popup
                if hasattr(self.scene_manager, 'transition_manager'):
                    self.scene_manager.transition_manager.transition_to(self.scene_manager, "campus", final_score=displayed_score, game_completed=True)
                else:
                    self.scene_manager.switch_scene("campus", final_score=displayed_score, game_completed=True)
                return
            else:
                self.rating_ui = RatingPopup.show(
                    camera_ui=camera.ui,
                    rating=rating,
                    score=self.score_manager.current_score,
                    coins=self.score_manager.earned_coins,
                    exp=self.score_manager.earned_exp,
                    is_exam=is_exam,
                    correct_answers=self.score_manager.correct_answers,
                    target_score=profile.target_toeic_score
                )
                self.rating_creation_time = time.time()
        else:
            # For practice lessons, show LessonCompletePopup instead
            correct = self.score_manager.correct_answers
            total = self.manager.get_total_questions()
            wrong = total - correct
            accuracy = (correct / total * 100.0) if total > 0 else 0.0
            passed = correct >= 5
            self.session_passed = passed
            
            was_exam_unlocked = False
            qm = None
            if hasattr(self.scene_manager, 'quest_manager'):
                qm = self.scene_manager.quest_manager
                was_exam_unlocked = qm.is_building_unlocked("exam")
            
            if passed:
                building_key = self.building_name.lower()
                if hasattr(profile, f"{building_key}_passed"):
                    setattr(profile, f"{building_key}_passed", True)
                    from core.save_manager import SaveManager
                    SaveManager.save_profile(profile)
                
                if qm:
                    qm.add_progress(1, self.building_name)
            
            if qm and not was_exam_unlocked and qm.is_building_unlocked("exam"):
                from ui.quest_notification import QuestNotification
                try:
                    from ursina import Audio
                    Audio('success', autoplay=True, loop=False)
                except Exception:
                    pass
                QuestNotification.show_building_unlocked(camera.ui, "Exam")
            
            title = f"{self.building_name} Practice"
            self.rating_ui = LessonCompletePopup.show(
                camera_ui=camera.ui,
                title=title,
                correct=correct,
                wrong=wrong,
                accuracy=accuracy,
                passed=passed,
                on_close=self._on_popup_closed
            )
            self.rating_creation_time = time.time()

    def _on_popup_closed(self) -> None:
        """Called when LessonCompletePopup is closed by the player."""
        self.rating_ui = None
        
        # Auto-complete the quest if we meet the target amount
        if hasattr(self.scene_manager, 'quest_manager'):
            qm = self.scene_manager.quest_manager
            active_q = qm.get_active_quest()
            if active_q and active_q.target_building.lower() == self.building_name.lower():
                if getattr(self, 'session_passed', False):
                    qm.profile.quest_progress = active_q.target_amount
                    qm._complete_active_quest()
        
        # Transition back to campus
        if hasattr(self.scene_manager, 'transition_manager'):
            self.scene_manager.transition_manager.transition_to(self.scene_manager, "campus")
        else:
            self.scene_manager.switch_scene("campus")

    def update_scene(self, delta_time: float) -> None:
        """Handle user input for answering and returning."""
        # Handle Answering
        if not self.has_answered:
            pressed_choice = None
            if held_keys['1']: pressed_choice = 1
            elif held_keys['2']: pressed_choice = 2
            elif held_keys['3']: pressed_choice = 3
            elif held_keys['4']: pressed_choice = 4
            
            if pressed_choice is not None and not self.was_key_pressed:
                if not self.manager.is_finished():
                    self._check_answer(pressed_choice)
                
            self.was_key_pressed = pressed_choice is not None

    def input(self, key: str) -> None:
        """Handle discrete key presses for scene transitions."""
        if not self.enabled:
            return
            
        if key in ('escape', 'enter', 'return'):
            # Only handle escape if we are not showing LessonCompletePopup which takes over
            # Or if it's an exam (where rating_ui is RatingPopup entity, which doesn't intercept input by itself)
            is_lesson_popup = self.rating_ui and hasattr(self.rating_ui, 'is_closing')
            if is_lesson_popup:
                return
                
            if self.manager.is_finished():
                if hasattr(self, 'rating_creation_time') and __import__('time').time() - self.rating_creation_time < 1.0:
                    return
                is_exam = self.building_name.lower() == "exam"
                if is_exam and key in ('enter', 'return') and getattr(self, 'exam_passed', False):
                    if hasattr(self.scene_manager, 'transition_manager'):
                        self.scene_manager.transition_manager.transition_to(self.scene_manager, "campus", final_score=self.score_manager.correct_answers * 100, game_completed=True)
                    else:
                        self.scene_manager.switch_scene("campus", final_score=self.score_manager.correct_answers * 100, game_completed=True)
                else:
                    # Normal return to campus or failure return
                    if key in ('escape', 'enter', 'return'): 
                        if hasattr(self.scene_manager, 'transition_manager'):
                            self.scene_manager.transition_manager.transition_to(self.scene_manager, "campus")
                        else:
                            self.scene_manager.switch_scene("campus")
            else:
                if key == 'escape':
                    if hasattr(self.scene_manager, 'transition_manager'):
                        self.scene_manager.transition_manager.transition_to(self.scene_manager, "building", building_name=self.building_name)
                    else:
                        self.scene_manager.switch_scene("building", building_name=self.building_name)

    def _check_answer(self, choice: int) -> None:
        """Check the selected answer and display feedback."""
        self.has_answered = True
        self.feedback_text.enabled = True
        self._stop_audio()
        
        q = self.manager.get_current_question()
        is_correct = self.manager.submit_answer(choice)
        time_taken = time.time() - self.question_start_time
        
        # Record mini-game performance
        self.minigame_manager.submit_result(is_correct, time_taken)
        
        # Register score
        self.score_manager.submit_result(is_correct)
        self._update_score_ui()
        
        if is_correct:
            self.feedback_text.text = "Correct!"
            self.feedback_text.color = color.green
            
            # Fast bonus feedback
            if time_taken <= 3.0:
                ComboPopup.show(camera.ui, "FAST!", position=(0.2, 0.2), popup_color=color.cyan)
                
            # Combo feedback
            if self.minigame_manager.current_combo >= 2:
                ComboPopup.show(camera.ui, f"COMBO x{self.minigame_manager.current_combo}", position=(-0.4, 0.2))
        else:
            correct_letter = ["A", "B", "C", "D"][q.correct_index - 1]
            self.feedback_text.text = f"Wrong!\nCorrect Answer: {correct_letter}"
            self.feedback_text.color = color.red
            
        # Use token to prevent callbacks if scene was exited
        current_token = self.current_question_token
        invoke(self._next_question_callback, current_token, delay=1.5)
        
    def _next_question_callback(self, token: int) -> None:
        """Callback to advance question, validated by token."""
        if token != self.current_question_token:
            return
        if not self.enabled:
            return
        self._next_question()

        
    def _next_question(self) -> None:
        self.feedback_text.enabled = False
        self.manager.next_question()
        self.has_answered = False
        self._display_current_question()

    def on_exit(self) -> None:
        """Cleanup."""
        if hasattr(self.scene_manager, 'hud_ui'):
            self.scene_manager.hud_ui.enable()
            
        self.current_question_token += 1 # Invalidate any pending next_question invokes
        self._stop_audio()
            
        if self.rating_ui:
            destroy(self.rating_ui)
            self.rating_ui = None
            
        # Reparent UI texts back to self
        self.score_text.parent = self
        self.correct_text.parent = self
        self.wrong_text.parent = self
        self.combo_text.parent = self
        
        self.building_title.parent = self
        self.question_number.parent = self
        self.question_text.parent = self
        self.context_text.parent = self
        self.answer_a.parent = self
        self.answer_b.parent = self
        self.answer_c.parent = self
        self.answer_d.parent = self
        self.instruction_text.parent = self
        self.feedback_text.parent = self
        self.result_text.parent = self
