from ursina import Entity, Text, color, camera, invoke
from core.events import Events
from core.quest_manager import QuestManager
from ui.quest_notification import QuestNotification

class QuestHUD(Entity):
    """
    Displays the campus progression checklist dynamically on the HUD.
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
            scale=(0.45, 0.45),
            position=(0.65, 0.25),
            enabled=False
        )
        
        self.checklist_text = Text(
            parent=self,
            text="",
            position=(0.43, 0.45),
            origin=(-0.5, 0.5), # Top-Left alignment within the box
            scale=1.1,
            color=color.white,
            enabled=False
        )
        
        # Subscribe to events
        event_bus.subscribe(Events.QUEST_ACCEPTED, self._on_quest_accepted)
        event_bus.subscribe(Events.QUEST_PROGRESS, self._on_quest_progress)
        event_bus.subscribe(Events.QUEST_COMPLETED, self._on_quest_completed)
        event_bus.subscribe(Events.QUEST_STATE_CHANGED, self._on_state_changed)
        
        # Initialize display
        self._refresh_display()

    def _refresh_display(self):
        # The user requested to remove the permanent progression panel from the campus HUD.
        # The checklist is now only shown when approaching the Final Exam building.
        self.bg.enabled = False
        self.checklist_text.enabled = False

    def _on_state_changed(self, **kwargs):
        self._refresh_display()

    def _on_quest_accepted(self, quest, **kwargs):
        self._refresh_display()
        # If it's not the first tutorial quest, and we just got a new quest,
        # it likely unlocked a building. Delay it so it doesn't overlap with Quest Completed.
        if quest.id != "tutorial_grammar":
            invoke(QuestNotification.show_building_unlocked, camera.ui, quest.target_building, 2.0, delay=3.5)
        
    def _on_quest_progress(self, quest, current, **kwargs):
        self._refresh_display()
        # Show lightweight notification
        QuestNotification.show_quest_updated(camera.ui)
            
    def _on_quest_completed(self, quest, **kwargs):
        self._refresh_display()
        
        unlocked_lesson = None
        if quest.next_quest_id:
            next_q = self.quest_manager.get_quest(quest.next_quest_id)
            if next_q:
                unlocked_lesson = next_q.title
                
        QuestNotification.show_quest_completed(camera.ui, quest.title, unlocked_lesson, 3.0)
