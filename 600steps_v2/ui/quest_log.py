from ursina import Entity, Text, color, held_keys
from core.quest_manager import QuestManager

class QuestLogUI:
    """
    Displays the player's active and completed quests.
    Toggled with the 'J' key.
    """
    def __init__(self, camera_ui, quest_manager: QuestManager):
        self.quest_manager = quest_manager
        
        self.bg = Entity(
            parent=camera_ui,
            model='quad',
            color=color.rgba(0, 0, 0, 0.9),
            scale=(1.2, 0.8),
            enabled=False
        )
        
        self.title_text = Text(
            parent=self.bg,
            text="QUEST JOURNAL",
            origin=(0, 0),
            position=(0, 0.4),
            scale=4,
            color=color.gold
        )
        
        self.content_text = Text(
            parent=self.bg,
            text="",
            origin=(-0.5, 0.5),
            position=(-0.45, 0.25),
            scale=2,
            color=color.white
        )
        
        self.instruction_text = Text(
            parent=self.bg,
            text="[J] Close",
            origin=(0, 0),
            position=(0, -0.45),
            scale=2,
            color=color.light_gray
        )
        
        self.was_j_pressed = False
        
    def _update_content(self):
        active_quest = self.quest_manager.get_active_quest()
        completed = self.quest_manager.profile.completed_quests
        
        content = ""
        
        if active_quest:
            content += f"<gold>ACTIVE QUEST: <white>{active_quest.title}\n"
            content += f"Target: {active_quest.objective_text}\n"
            
            progress = self.quest_manager.profile.quest_progress
            target = active_quest.target_amount
            color_tag = "<green>" if progress >= target else "<red>"
            
            content += f"Progress: {color_tag}{progress} / {target}<white>\n"
            content += f"Rewards: {active_quest.reward_coin} Coins, {active_quest.reward_exp} EXP\n\n"
        else:
            content += "<gray>No active quests.\n\n"
            
        content += f"<gold>COMPLETED QUESTS: <white>{len(completed)}\n"
        for q_id in completed[-5:]: # Show last 5
            q = self.quest_manager.get_quest(q_id)
            if q:
                content += f"- {q.title}\n"
                
        self.content_text.text = content
        
    def update(self):
        is_j_pressed = held_keys['j']
        
        if is_j_pressed and not self.was_j_pressed:
            if self.bg.enabled:
                self.bg.enabled = False
            else:
                self._update_content()
                self.bg.enabled = True
                
        self.was_j_pressed = is_j_pressed
