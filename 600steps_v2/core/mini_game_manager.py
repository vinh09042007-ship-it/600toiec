class MiniGameManager:
    """
    Tracks mini-game performance, speed, and assigns a final rating (S, A, B, C).
    """
    def __init__(self, total_questions: int):
        self.total_questions = total_questions
        self.correct_answers = 0
        self.max_combo = 0
        self.current_combo = 0
        self.total_time_taken = 0.0
        self.fast_answers = 0 # Answers submitted under the threshold

    def submit_result(self, is_correct: bool, time_taken: float, fast_threshold: float = 3.0):
        """Records the outcome of a single action in the mini-game."""
        self.total_time_taken += time_taken
        
        if is_correct:
            self.correct_answers += 1
            self.current_combo += 1
            if self.current_combo > self.max_combo:
                self.max_combo = self.current_combo
                
            if time_taken <= fast_threshold:
                self.fast_answers += 1
        else:
            self.current_combo = 0

    def calculate_rating(self) -> str:
        """
        Calculates the S/A/B/C rating based on accuracy, combo, and speed.
        """
        if self.total_questions <= 0:
            return "C"
            
        accuracy = self.correct_answers / self.total_questions
        speed_ratio = self.fast_answers / self.total_questions
        
        # Criteria for S Rank (Perfect or near perfect + very fast)
        if accuracy == 1.0 and speed_ratio >= 0.8:
            return "S"
            
        # Criteria for A Rank (Good accuracy, decent speed)
        if accuracy >= 0.8:
            return "A"
            
        # Criteria for B Rank (Passable)
        if accuracy >= 0.5:
            return "B"
            
        # C Rank (Fail or poor)
        return "C"
