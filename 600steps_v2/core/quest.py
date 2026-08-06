from dataclasses import dataclass
from typing import Optional

@dataclass
class Quest:
    """
    Defines the structure and parameters of a single Quest.
    """
    id: str
    title: str
    description: str
    objective_text: str
    target_building: str
    target_amount: int
    reward_coin: int
    reward_exp: int
    npc_name: str # The NPC who gives and receives this quest
    receiver_npc: Optional[str] = None # NPC who receives the quest if different from giver
    next_quest_id: Optional[str] = None
    
    # Dialogue hooks
    dialogue_offer: list[str] = None
    dialogue_active: list[str] = None
    dialogue_ready: list[str] = None
    
    def __post_init__(self):
        if self.receiver_npc is None:
            self.receiver_npc = self.npc_name
            
        # Default dialogues if none provided
        if not self.dialogue_offer:
            self.dialogue_offer = [f"I have a task for you: {self.title}", self.description, "Will you help?"]
        if not self.dialogue_active:
            self.dialogue_active = [f"Remember your task: {self.objective_text}"]
        if not self.dialogue_ready:
            self.dialogue_ready = ["Excellent work!", "Here is your reward."]
