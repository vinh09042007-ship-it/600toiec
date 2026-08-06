"""
Contains core logic and state management for TOEIC quizzes.
"""
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Question:
    """
    Represents a single multiple-choice question.
    """
    text: str
    choices: List[str]
    correct_index: int  # 1-indexed (1=A, 2=B, 3=C, 4=D)
    context: Optional[str] = None


class QuestionManager:
    """
    Manages a list of questions, tracks the current question, and calculates score.
    """
    
    def __init__(self, questions: List[Question]):
        """Initialize with a list of questions."""
        self.questions = questions
        self.current_index = 0
        self.score = 0
        
    def get_current_question(self) -> Optional[Question]:
        """Returns the current question or None if finished."""
        if self.is_finished():
            return None
        return self.questions[self.current_index]
        
    def get_total_questions(self) -> int:
        """Returns the total number of questions."""
        return len(self.questions)
        
    def submit_answer(self, choice_index: int) -> bool:
        """
        Submits an answer for the current question.
        Returns True if correct, False otherwise.
        """
        if self.is_finished():
            return False
            
        question = self.get_current_question()
        is_correct = (choice_index == question.correct_index)
        
        if is_correct:
            self.score += 1
            
        return is_correct
        
    def next_question(self) -> None:
        """Advances to the next question."""
        if not self.is_finished():
            self.current_index += 1
            
    def is_finished(self) -> bool:
        """Returns True if all questions have been answered."""
        return self.current_index >= len(self.questions)
