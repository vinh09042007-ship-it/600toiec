"""
Score management and reward calculations for the game.
"""

class ScoreManager:
    """
    Manages scoring, combos, and rewards for a practice session.
    Independent of specific quiz content or UI.
    """
    
    def __init__(self, total_questions: int) -> None:
        """Initialize a new score session."""
        self.total_questions = total_questions
        self.answered_questions = 0
        self.correct_answers = 0
        self.wrong_answers = 0
        
        self.current_score = 0
        self.combo_streak = 0
        
        self.earned_coins = 0
        self.earned_exp = 0

    def submit_result(self, is_correct: bool) -> None:
        """
        Updates score and stats based on whether an answer was correct.
        
        Args:
            is_correct (bool): True if the answer was correct, False otherwise.
        """
        self.answered_questions += 1
        
        if is_correct:
            self.correct_answers += 1
            self.combo_streak += 1
            
            # Rewards
            self.current_score += 10
            self.earned_coins += 10
            self.earned_exp += 20
        else:
            self.wrong_answers += 1
            self.combo_streak = 0
            
            # No rewards for wrong answers
            
    def get_accuracy(self) -> float:
        """
        Calculates the percentage of correct answers.
        
        Returns:
            float: Accuracy percentage (0.0 to 100.0)
        """
        if self.total_questions <= 0:
            return 0.0
        return (self.correct_answers / self.total_questions) * 100.0
        
    def get_rank(self) -> str:
        """
        Determines the performance rank based on accuracy.
        
        Returns:
            str: 'S', 'A', 'B', 'C', or 'D'
        """
        accuracy = self.get_accuracy()
        
        if accuracy >= 95.0:
            return "S"
        elif accuracy >= 85.0:
            return "A"
        elif accuracy >= 70.0:
            return "B"
        elif accuracy >= 50.0:
            return "C"
        else:
            return "D"
