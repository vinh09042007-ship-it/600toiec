from ursina import Entity, Text, color
from core.events import Events
from core.quest_manager import QuestManager

class QuestHUD(Entity):
    """
    Displays the current active quest dynamically on the HUD.
    Subscribes to EventBus to avoid polling.
    """
    def __init__(self, camera_ui, event_bus, quest_manager: QuestManager):
        super().__init__(parent=camera_ui)
        self.quest_manager = quest_manager
        
        # UI Elements
        # Background box at the top right of the screen
        self.bg = Entity(
            parent=self,
            model='quad',
            color=color.rgba(0, 0, 0, 0.8),
            scale=(0.4, 0.25),
            position=(0.65, 0.35),
            enabled=False
        )
        
        # Parent text to self to avoid inheriting the non-uniform scale of the bg
        self.header_text = Text(
            parent=self,
            text="Current Quest",
            position=(0.48, 0.45),
            origin=(-0.5, 0.5), # Top-Left alignment within the box
            scale=1.5,
            color=color.gold,
            enabled=False
        )
        
        self.title_text = Text(
            parent=self,
            text=" ",
            position=(0.48, 0.35),
            origin=(-0.5, 0.5),
            scale=1.2,
            color=color.white,
            enabled=False
        )
        self.title_text.wordwrap = 20
        
        self.progress_text = Text(
            parent=self,
            text="",
            position=(0.48, 0.26),
            origin=(-0.5, 0.5),
            scale=1.2,
            color=color.cyan,
            enabled=False
        )
        
        # Subscribe to events
        event_bus.subscribe(Events.QUEST_ACCEPTED, self._on_quest_accepted)
        event_bus.subscribe(Events.QUEST_PROGRESS, self._on_quest_progress)
        event_bus.subscribe(Events.QUEST_COMPLETED, self._on_quest_completed)
        
        # Initialize display if there's already an active quest
        self._refresh_display()

    def _refresh_display(self):
        active_quest = self.quest_manager.get_active_quest()
        if active_quest:
            self.title_text.text = active_quest.title
            
            progress = self.quest_manager.profile.quest_progress
            target = active_quest.target_amount
            
            if target > 0:
                self.progress_text.text = f"{progress} / {target} {active_quest.objective_text.split()[-1]}"
            else:
                self.progress_text.text = active_quest.objective_text
                
            self.bg.enabled = True
            self.header_text.enabled = True
            self.title_text.enabled = True
            self.progress_text.enabled = True
        else:
            self.bg.enabled = False
            self.header_text.enabled = False
            self.title_text.enabled = False
            self.progress_text.enabled = False

    def _on_quest_accepted(self, quest, **kwargs):
        self._refresh_display()
        
    def _on_quest_progress(self, quest, current, **kwargs):
        if self.bg.enabled:
            target = quest.target_amount
            if target > 0:
                self.progress_text.text = f"{current} / {target} {quest.objective_text.split()[-1]}"
            
    def _on_quest_completed(self, quest, **kwargs):
        self.bg.enabled = False
        self.header_text.enabled = False
        self.title_text.enabled = False
        self.progress_text.enabled = False
