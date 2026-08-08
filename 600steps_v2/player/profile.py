"""
Manages the persistent global profile of the player.
"""

class PlayerProfile:
    """
    Stores long-term progression, statistics, and cumulative rewards.
    """
    
    def __init__(self, player_name: str = "Student") -> None:
        self.player_name = player_name
        
        # Resources
        self.total_score = 0
        self.total_exp = 0
        self.total_coins = 0
        self.current_level = 1
        self.target_toeic_score = 600
        
        # Category tracking (number of times practiced)
        self.grammar_completed = 0
        self.vocabulary_completed = 0
        self.listening_completed = 0
        self.reading_completed = 0
        self.exam_completed = 0
        
        # Progression state
        self.grammar_passed = False
        self.vocabulary_passed = False
        self.listening_passed = False
        self.reading_passed = False
        self.game_completed = False
        
        # Quest Tracking
        self.active_quest_id: str | None = None
        self.quest_progress: int = 0
        self.completed_quests: list[str] = []
        
        # Global Statistics
        self.total_correct_answers = 0
        self.total_wrong_answers = 0
        self.total_practices = 0
        self.highest_score = 0

    def add_practice_result(self, score_manager, category: str) -> None:
        """
        Merges a completed practice session's results into the global profile.
        
        Args:
            score_manager (ScoreManager): The session's score data.
            category (str): The name of the building/category practiced.
        """
        self.total_practices += 1
        
        # Accumulate resources
        self.total_score += score_manager.current_score
        self.total_exp += score_manager.earned_exp
        self.total_coins += score_manager.earned_coins
        
        # Check highest score
        if score_manager.current_score > self.highest_score:
            self.highest_score = score_manager.current_score
            
        # Accumulate QA stats
        self.total_correct_answers += score_manager.correct_answers
        self.total_wrong_answers += score_manager.wrong_answers
        
        # Track category completions
        cat_lower = category.lower()
        if "grammar" in cat_lower:
            self.grammar_completed += 1
        elif "vocabulary" in cat_lower:
            self.vocabulary_completed += 1
        elif "listening" in cat_lower:
            self.listening_completed += 1
        elif "reading" in cat_lower:
            self.reading_completed += 1
        elif "exam" in cat_lower:
            self.exam_completed += 1
            
        # Check for level up
        self._check_level_up()
        
        # Auto-save after update
        # Import inside to avoid circular dependencies
        from core.save_manager import SaveManager
        SaveManager.save_profile(self)

    def _check_level_up(self) -> None:
        """Updates the current level based on total EXP."""
        # Level 1: 0-99 EXP, Level 2: 100-199 EXP, etc.
        self.current_level = (self.total_exp // 100) + 1
        
    def get_overall_accuracy(self) -> float:
        """
        Calculates the historical accuracy percentage across all practices.
        
        Returns:
            float: Global accuracy percentage (0.0 to 100.0)
        """
        total = self.total_correct_answers + self.total_wrong_answers
        if total <= 0:
            return 0.0
        return (self.total_correct_answers / total) * 100.0

    def to_dict(self) -> dict:
        """Serializes the profile state into a dictionary."""
        return {
            "player_name": self.player_name,
            "total_score": self.total_score,
            "total_exp": self.total_exp,
            "total_coins": self.total_coins,
            "current_level": self.current_level,
            "target_toeic_score": self.target_toeic_score,
            "total_correct_answers": self.total_correct_answers,
            "total_wrong_answers": self.total_wrong_answers,
            "total_practices": self.total_practices,
            "highest_score": self.highest_score,
            "building_stats": {
                "Grammar": {"completed": self.grammar_completed, "passed": self.grammar_passed},
                "Vocabulary": {"completed": self.vocabulary_completed, "passed": self.vocabulary_passed},
                "Listening": {"completed": self.listening_completed, "passed": self.listening_passed},
                "Reading": {"completed": self.reading_completed, "passed": self.reading_passed},
                "Exam": {"completed": self.exam_completed},
            },
            "active_quest_id": self.active_quest_id,
            "quest_progress": self.quest_progress,
            "completed_quests": self.completed_quests,
            "game_completed": getattr(self, 'game_completed', False)
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'PlayerProfile':
        """Deserializes a dictionary into a PlayerProfile instance."""
        profile = cls(player_name=data.get("player_name", "Student"))
        
        # Resources
        profile.total_score = data.get("total_score", 0)
        profile.total_exp = data.get("total_exp", 0)
        profile.total_coins = data.get("total_coins", 0)
        profile.current_level = data.get("current_level", 1)
        profile.target_toeic_score = data.get("target_toeic_score", 600)
        
        # Global Statistics
        profile.total_correct_answers = data.get("total_correct_answers", 0)
        profile.total_wrong_answers = data.get("total_wrong_answers", 0)
        profile.total_practices = data.get("total_practices", 0)
        profile.highest_score = data.get("highest_score", 0)
        
        # Category tracking
        building_stats = data.get("building_stats", {})
        profile.grammar_completed = building_stats.get("Grammar", {}).get("completed", 0)
        profile.grammar_passed = building_stats.get("Grammar", {}).get("passed", False)
        
        profile.vocabulary_completed = building_stats.get("Vocabulary", {}).get("completed", 0)
        profile.vocabulary_passed = building_stats.get("Vocabulary", {}).get("passed", False)
        
        profile.listening_completed = building_stats.get("Listening", {}).get("completed", 0)
        profile.listening_passed = building_stats.get("Listening", {}).get("passed", False)
        
        profile.reading_completed = building_stats.get("Reading", {}).get("completed", 0)
        profile.reading_passed = building_stats.get("Reading", {}).get("passed", False)
        
        profile.exam_completed = building_stats.get("Exam", {}).get("completed", 0)
        
        # Quests
        profile.active_quest_id = data.get("active_quest_id")
        profile.quest_progress = data.get("quest_progress", 0)
        profile.completed_quests = data.get("completed_quests", [])
        profile.game_completed = data.get("game_completed", False)
        
        return profile
