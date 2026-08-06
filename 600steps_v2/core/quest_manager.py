from core.quest import Quest
from player.profile import PlayerProfile
from typing import Optional, Dict
from ui.notification import NotificationUI
from core.eventbus import EventBus
from core.events import Events

class QuestManager:
    """
    Globally manages quest states, progress tracking, and logic.
    """
    
    # Pre-defined storyline
    QUESTS: Dict[str, Quest] = {
        "tutorial_grammar": Quest(
            id="tutorial_grammar",
            title="Welcome to Campus",
            description="Talk to the Receptionist.",
            objective_text="Visit the Grammar Building.",
            target_building="Grammar",
            target_amount=0,
            reward_coin=0,
            reward_exp=0,
            npc_name="Receptionist",
            receiver_npc="Grammar Professor",
            next_quest_id="grammar_lesson",
            dialogue_offer=[
                "Welcome to the TOEIC Training Campus.",
                "Your goal is to achieve a TOEIC score of 600.",
                "Complete learning buildings, finish small tasks, and then take the final exam.",
                "Good luck!"
            ],
            dialogue_active=["Talk to the Grammar Professor."],
            dialogue_ready=["Welcome to Grammar Hall."]
        ),
        "grammar_lesson": Quest(
            id="grammar_lesson",
            title="Grammar Basics",
            description="Complete the grammar lesson.",
            objective_text="Complete Grammar practice.",
            target_building="Grammar",
            target_amount=10,
            reward_coin=50,
            reward_exp=100,
            npc_name="Grammar Professor",
            receiver_npc="Grammar Professor",
            next_quest_id="vocabulary_lesson",
            dialogue_offer=["Grammar is the foundation of communication.", "Complete today's grammar practice."],
            dialogue_active=["Complete today's grammar practice inside."],
            dialogue_ready=["Excellent work."]
        ),
        "vocabulary_lesson": Quest(
            id="vocabulary_lesson",
            title="Vocabulary Building",
            description="Complete the vocabulary lesson.",
            objective_text="Complete Vocabulary practice.",
            target_building="Vocabulary",
            target_amount=10,
            reward_coin=50,
            reward_exp=100,
            npc_name="Vocabulary Professor",
            receiver_npc="Vocabulary Professor",
            next_quest_id="listening_lesson",
            dialogue_offer=["A strong vocabulary makes every section easier.", "Complete today's vocabulary practice."],
            dialogue_active=["Complete today's vocabulary practice inside."],
            dialogue_ready=["Great job."]
        ),
        "listening_lesson": Quest(
            id="listening_lesson",
            title="Active Listening",
            description="Complete the listening lesson.",
            objective_text="Complete Listening practice.",
            target_building="Listening",
            target_amount=10,
            reward_coin=50,
            reward_exp=100,
            npc_name="Listening Professor",
            receiver_npc="Listening Professor",
            next_quest_id="reading_lesson",
            dialogue_offer=["Listening is an important TOEIC skill.", "Finish today's listening practice."],
            dialogue_active=["Finish today's listening practice inside."],
            dialogue_ready=["Excellent."]
        ),
        "reading_lesson": Quest(
            id="reading_lesson",
            title="Reading Comprehension",
            description="Complete the reading lesson.",
            objective_text="Complete Reading practice.",
            target_building="Reading",
            target_amount=10,
            reward_coin=50,
            reward_exp=100,
            npc_name="Reading Professor",
            receiver_npc="Reading Professor",
            next_quest_id="exam_quest",
            dialogue_offer=["Reading combines grammar and vocabulary.", "Complete today's reading practice."],
            dialogue_active=["Complete today's reading practice inside."],
            dialogue_ready=["Fantastic."]
        ),
        "exam_quest": Quest(
            id="exam_quest",
            title="The Final Exam",
            description="Take the final TOEIC exam.",
            objective_text="Pass the exam in the Exam Center.",
            target_building="Exam",
            target_amount=1,
            reward_coin=500,
            reward_exp=1000,
            npc_name="Exam Supervisor",
            receiver_npc="Exam Supervisor",
            next_quest_id=None,
            dialogue_offer=["You have completed all required training.", "Take the TOEIC Final Exam.", "Good luck."],
            dialogue_active=["The Exam is ready for you."],
            dialogue_ready=["Congratulations on your score!"]
        )
    }

    def __init__(self, profile: PlayerProfile, event_bus: EventBus):
        self.profile = profile
        self.event_bus = event_bus
        
        # UI dependencies (injected later)
        self.notification_ui: Optional[NotificationUI] = None

    def get_quest(self, quest_id: str) -> Optional[Quest]:
        return self.QUESTS.get(quest_id)

    def get_active_quest(self) -> Optional[Quest]:
        if not self.profile.active_quest_id:
            return None
        return self.get_quest(self.profile.active_quest_id)

    def _get_next_available_quest(self) -> Optional[Quest]:
        """Returns the next quest in the chain based on completed quests."""
        if not self.profile.completed_quests:
            return self.get_quest("tutorial_grammar")
        
        last_completed_id = self.profile.completed_quests[-1]
        last_completed = self.get_quest(last_completed_id)
        
        if last_completed and last_completed.next_quest_id:
            return self.get_quest(last_completed.next_quest_id)
            
        return None

    def get_npc_quest_state(self, npc_name: str) -> str:
        """
        Determines the quest state for a specific NPC.
        States are mutually exclusive.
        Returns: 'offer', 'active', 'ready', or 'none'
        """
        active_quest = self.get_active_quest()
        
        if active_quest:
            # READY takes priority if they are the receiver and requirements are met
            if active_quest.receiver_npc == npc_name:
                if self.profile.quest_progress >= active_quest.target_amount:
                    return 'ready'
            
            # ACTIVE if they are involved at all but not ready
            if active_quest.receiver_npc == npc_name or active_quest.npc_name == npc_name:
                return 'active'
                
            return 'none'
            
        # No active quest: Check for an offer
        next_quest = self._get_next_available_quest()
        if next_quest and next_quest.npc_name == npc_name:
            return 'offer'
                
        return 'none'

    def interact_with_npc(self, npc_name: str) -> tuple[list[str], Optional[callable]]:
        """
        Called when talking to an NPC. Handles quest state transitions and returns dialogue.
        Returns a tuple of (dialogue_lines, on_dialogue_end_callback).
        """
        state = self.get_npc_quest_state(npc_name)
        active_quest = self.get_active_quest()
        
        if state == 'ready':
            return list(active_quest.dialogue_ready), self._complete_active_quest
            
        elif state == 'offer':
            next_quest = self._get_next_available_quest()
            return list(next_quest.dialogue_offer), lambda q=next_quest.id: self._accept_quest(q)
            
        elif state == 'active':
            return list(active_quest.dialogue_active), None
            
        return ["I have nothing for you right now."], None

    def _accept_quest(self, quest_id: str):
        self.profile.active_quest_id = quest_id
        self.profile.quest_progress = 0
        
        quest = self.get_quest(quest_id)
        self.event_bus.emit(Events.QUEST_ACCEPTED, quest=quest)
        
        # Save state
        from core.save_manager import SaveManager
        SaveManager.save_profile(self.profile)
        
        self.event_bus.emit(Events.QUEST_STATE_CHANGED)

    def _complete_active_quest(self):
        quest = self.get_active_quest()
        if not quest: return
        
        self.profile.total_coins += quest.reward_coin
        self.profile.total_exp += quest.reward_exp
        
        self.profile.completed_quests.append(quest.id)
        self.profile.active_quest_id = None
        self.profile.quest_progress = 0
        
        self.event_bus.emit(Events.QUEST_COMPLETED, quest=quest)
        
        # Auto-activate next quest in the storyline if one exists
        if quest.next_quest_id:
            next_quest = self.get_quest(quest.next_quest_id)
            if next_quest:
                self._accept_quest(next_quest.id)
        else:
            # Save state only if not auto-activating (auto-activate will save it)
            from core.save_manager import SaveManager
            SaveManager.save_profile(self.profile)
            
        self.event_bus.emit(Events.QUEST_STATE_CHANGED)

    def add_progress(self, amount: int, building_name: str):
        """Called by QuestionScene on correct answers."""
        quest = self.get_active_quest()
        if not quest: return
        
        if quest.target_building.lower() == building_name.lower():
            if self.profile.quest_progress < quest.target_amount:
                self.profile.quest_progress += amount
                
                self.event_bus.emit(Events.QUEST_PROGRESS, quest=quest, current=self.profile.quest_progress)
                
                from core.save_manager import SaveManager
                SaveManager.save_profile(self.profile)
                
                if self.profile.quest_progress >= quest.target_amount:
                    self.event_bus.emit(Events.QUEST_STATE_CHANGED)

    def is_building_unlocked(self, building_name: str) -> bool:
        """
        Determines if the building is accessible using explicit progression checks.
        """
        building = building_name.lower()
        
        result = False
        if building == "grammar":
            result = self.profile.active_quest_id in ["tutorial_grammar", "grammar_lesson"] or "grammar_lesson" in self.profile.completed_quests
        elif building == "vocabulary":
            result = self.profile.active_quest_id == "vocabulary_lesson" or "vocabulary_lesson" in self.profile.completed_quests
        elif building == "listening":
            result = self.profile.active_quest_id == "listening_lesson" or "listening_lesson" in self.profile.completed_quests
        elif building == "reading":
            result = self.profile.active_quest_id == "reading_lesson" or "reading_lesson" in self.profile.completed_quests
        elif building == "exam" or building == "exam center":
            result = self.profile.active_quest_id == "exam_quest" or "exam_quest" in self.profile.completed_quests
            
        return result

    def get_building_lock_requirement(self, building_name: str) -> str:
        """Returns the user-friendly requirement message for a locked building."""
        building = building_name.lower()
        if building == "grammar":
            return "Talk to the Receptionist first."
        if building == "vocabulary":
            return "Complete Grammar Practice first."
        if building == "listening":
            return "Complete Vocabulary Practice first."
        if building == "reading":
            return "Complete Listening Practice first."
        if building == "exam" or building == "exam center":
            return "Complete all required training first."
        return "Not available."
