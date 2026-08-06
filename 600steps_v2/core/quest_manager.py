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
            title="First Lesson",
            description="Talk to the Professor.",
            objective_text="Visit Grammar Hall and talk to the Professor.",
            target_building="Grammar",
            target_amount=0,
            reward_coin=20,
            reward_exp=40,
            npc_name="Receptionist",
            receiver_npc="Professor",
            next_quest_id="grammar_lesson",
            dialogue_offer=["Welcome to 600 Steps!", "Are you ready to start your learning journey?", "Go meet the Professor in the Grammar building."],
            dialogue_active=["Go meet the Professor in the Grammar building."],
            dialogue_ready=["Ah, the new student.", "Welcome to Grammar Hall."]
        ),
        "grammar_lesson": Quest(
            id="grammar_lesson",
            title="Grammar Basics",
            description="The Professor wants to test your grammar skills.",
            objective_text="Complete 10 Grammar questions.",
            target_building="Grammar",
            target_amount=10,
            reward_coin=50,
            reward_exp=100,
            npc_name="Professor",
            receiver_npc="Professor",
            next_quest_id="reading_lesson",
            dialogue_offer=["Show me what you can do.", "Complete today's lesson."],
            dialogue_active=["Complete today's lesson in the Grammar hall."],
            dialogue_ready=["Excellent work.", "The Reading hall is now open to you."]
        ),
        "reading_lesson": Quest(
            id="reading_lesson",
            title="Reading Comprehension",
            description="The Librarian needs help organizing reading tests.",
            objective_text="Complete 5 Reading questions.",
            target_building="Reading",
            target_amount=5,
            reward_coin=50,
            reward_exp=100,
            npc_name="Librarian",
            receiver_npc="Librarian",
            next_quest_id="listening_lesson",
            dialogue_offer=["Shh... Are you here to read?", "Please complete some reading exercises."],
            dialogue_active=["Read carefully..."],
            dialogue_ready=["Thank you for keeping the library active."]
        ),
        "listening_lesson": Quest(
            id="listening_lesson",
            title="Listening Comprehension",
            description="Practice your listening skills.",
            objective_text="Complete 5 Listening questions.",
            target_building="Listening",
            target_amount=5,
            reward_coin=50,
            reward_exp=100,
            npc_name="Listening Instructor",
            receiver_npc="Listening Instructor",
            next_quest_id="office_quest",
            dialogue_offer=["Let's tune your ears.", "Complete a listening test."],
            dialogue_active=["Focus on the audio."],
            dialogue_ready=["Your hearing is sharp!"]
        ),
        "office_quest": Quest(
            id="office_quest",
            title="Office Tasks",
            description="Help the Office staff.",
            objective_text="Complete Office questions.",
            target_building="Office",
            target_amount=5,
            reward_coin=50,
            reward_exp=100,
            npc_name="Office Staff",
            receiver_npc="Office Staff",
            next_quest_id="exam_quest",
            dialogue_offer=["Welcome to the Office.", "Can you help sort some paperwork?"],
            dialogue_active=["Keep sorting those documents."],
            dialogue_ready=["Thank you for your help!"]
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
            npc_name="Security Guard",
            receiver_npc="Security Guard",
            next_quest_id=None,
            dialogue_offer=["You've proven yourself.", "You may enter the Exam Center."],
            dialogue_active=["Good luck on your exam."],
            dialogue_ready=["Congratulations, you graduated!"]
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

    def get_npc_quest_state(self, npc_name: str) -> str:
        """
        Determines the quest state for a specific NPC.
        Returns: 'offer', 'active', 'ready', or 'none'
        """
        active_quest = self.get_active_quest()
        
        if active_quest:
            if active_quest.receiver_npc == npc_name:
                if self.profile.quest_progress >= active_quest.target_amount:
                    return 'ready'
            if active_quest.npc_name == npc_name:
                return 'active'
            
        next_quest_id = "tutorial_grammar"
        
        if self.profile.completed_quests:
            last_completed_id = self.profile.completed_quests[-1]
            last_completed = self.get_quest(last_completed_id)
            if last_completed and last_completed.next_quest_id:
                next_quest_id = last_completed.next_quest_id
            else:
                next_quest_id = None
                
        if next_quest_id and not active_quest:
            next_quest = self.get_quest(next_quest_id)
            if next_quest and next_quest.npc_name == npc_name:
                return 'offer'
                
        return 'none'

    def interact_with_npc(self, npc_name: str) -> list[str]:
        """
        Called when talking to an NPC. Handles quest state transitions and returns dialogue.
        """
        state = self.get_npc_quest_state(npc_name)
        active_quest = self.get_active_quest()
        
        if state == 'ready' and active_quest:
            dialogue = list(active_quest.dialogue_ready)
            self._complete_active_quest()
            return dialogue
            
        elif state == 'offer':
            next_quest_id = "tutorial_grammar"
            if self.profile.completed_quests:
                last_completed = self.get_quest(self.profile.completed_quests[-1])
                next_quest_id = last_completed.next_quest_id
                
            quest = self.get_quest(next_quest_id)
            dialogue = list(quest.dialogue_offer)
            self._accept_quest(quest.id)
            return dialogue
            
        elif state == 'active' and active_quest:
            return list(active_quest.dialogue_active)
            
        return ["I have nothing for you right now."]

    def _accept_quest(self, quest_id: str):
        print(f"[Quest] Accepted {quest_id}")
        self.profile.active_quest_id = quest_id
        self.profile.quest_progress = 0
        
        quest = self.get_quest(quest_id)
        if self.notification_ui:
            self.notification_ui.show(f"New Quest: {quest.title}")
            
        self.event_bus.emit(Events.QUEST_ACCEPTED, quest=quest)
        
        # Check if building unlocked just by accepting
        if quest_id == "tutorial_grammar":
            print(f"[Building] Grammar unlocked")

    def _complete_active_quest(self):
        quest = self.get_active_quest()
        if not quest: return
        
        print(f"[Quest] Completed {quest.id}")
        
        self.profile.total_coins += quest.reward_coin
        self.profile.total_exp += quest.reward_exp
        
        self.profile.completed_quests.append(quest.id)
        self.profile.active_quest_id = None
        self.profile.quest_progress = 0
        
        if self.notification_ui:
            self.notification_ui.show(f"Quest Complete!\n+{quest.reward_coin} Coins\n+{quest.reward_exp} EXP")
            
        self.event_bus.emit(Events.QUEST_COMPLETED, quest=quest)
        
        # Print debugs for unlock based on what just completed
        if quest.id == "grammar_lesson":
            print("[Building] Reading unlocked")
        elif quest.id == "reading_lesson":
            print("[Building] Listening unlocked")
        elif quest.id == "listening_lesson":
            print("[Building] Office unlocked")
        elif quest.id == "office_quest":
            print("[Building] Exam Center unlocked")

    def add_progress(self, amount: int, building_name: str):
        """Called by QuestionScene on correct answers."""
        quest = self.get_active_quest()
        if not quest: return
        
        if quest.target_building.lower() == building_name.lower():
            if self.profile.quest_progress < quest.target_amount:
                self.profile.quest_progress += amount
                
                if self.profile.quest_progress >= quest.target_amount:
                    if self.notification_ui:
                        self.notification_ui.show("Objective Complete! Return to NPC.")

    def is_building_unlocked(self, building_name: str) -> bool:
        """
        Determines if the building is accessible based on storyline progression.
        """
        building = building_name.lower()
        
        if building == "grammar":
            return bool(self.profile.active_quest_id) or len(self.profile.completed_quests) > 0
            
        if building == "reading":
            return "grammar_lesson" in self.profile.completed_quests
            
        if building == "listening":
            return "reading_lesson" in self.profile.completed_quests
            
        if building == "office":
            return "listening_lesson" in self.profile.completed_quests
            
        if building == "exam" or building == "exam center":
            return "office_quest" in self.profile.completed_quests
            
        return False

    def get_building_lock_requirement(self, building_name: str) -> str:
        """Returns the user-friendly requirement message for a locked building."""
        building = building_name.lower()
        if building == "grammar":
            return "Talk to the Receptionist first."
        if building == "reading":
            return "Complete Grammar Quest first."
        if building == "listening":
            return "Complete Reading Quest first."
        if building == "office":
            return "Complete Listening Quest first."
        if building == "exam" or building == "exam center":
            return "Complete all other quests first."
        return "Not available."
