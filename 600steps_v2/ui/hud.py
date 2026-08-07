from ursina import Entity, Text, color, camera, invoke
from core.events import Events
from core.quest_manager import QuestManager
from ui.quest_notification import QuestNotification

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
            scale=(0.4, 0.4),
            position=(0.65, 0.27),
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
        
        self.objective_header = Text(
            parent=self,
            text="Objective:",
            position=(0.48, 0.28),
            origin=(-0.5, 0.5),
            scale=1.2,
            color=color.gold,
            enabled=False
        )
        
        self.progress_text = Text(
            parent=self,
            text=" ",
            position=(0.48, 0.22),
            origin=(-0.5, 0.5),
            scale=1.2,
            color=color.cyan,
            enabled=False
        )
        self.progress_text.wordwrap = 20
        
        self.location_header = Text(
            parent=self,
            text="Location:",
            position=(0.48, 0.12),
            origin=(-0.5, 0.5),
            scale=1.2,
            color=color.gold,
            enabled=False
        )
        
        self.location_text = Text(
            parent=self,
            text="",
            position=(0.48, 0.06),
            origin=(-0.5, 0.5),
            scale=1.2,
            color=color.white,
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
                
            location = ""
            state = self.quest_manager.get_npc_quest_state(active_quest.receiver_npc)
            if state == 'ready' or state == 'offer':
                location = active_quest.receiver_npc or active_quest.npc_name
            else:
                location = active_quest.target_building or ""
                
            self.location_text.text = location
                
            self.bg.enabled = True
            self.header_text.enabled = True
            self.title_text.enabled = True
            self.objective_header.enabled = True
            self.progress_text.enabled = True
            
            if location:
                self.location_header.enabled = True
                self.location_text.enabled = True
            else:
                self.location_header.enabled = False
                self.location_text.enabled = False
        else:
            self.bg.enabled = False
            self.header_text.enabled = False
            self.title_text.enabled = False
            self.objective_header.enabled = False
            self.progress_text.enabled = False
            self.location_header.enabled = False
            self.location_text.enabled = False

    def _on_quest_accepted(self, quest, **kwargs):
        self._refresh_display()
        # If it's not the first tutorial quest, and we just got a new quest,
        # it likely unlocked a building. Delay it so it doesn't overlap with Quest Completed.
        if quest.id != "tutorial_grammar":
            invoke(QuestNotification.show_building_unlocked, camera.ui, quest.target_building, 2.0, delay=3.5)
        
    def _on_quest_progress(self, quest, current, **kwargs):
        if self.bg.enabled:
            target = quest.target_amount
            if target > 0:
                self.progress_text.text = f"{current} / {target} {quest.objective_text.split()[-1]}"
        
        # Show lightweight notification
        QuestNotification.show_quest_updated(camera.ui)
            
    def _on_quest_completed(self, quest, **kwargs):
        self.bg.enabled = False
        self.header_text.enabled = False
        self.title_text.enabled = False
        self.objective_header.enabled = False
        self.progress_text.enabled = False
        self.location_header.enabled = False
        self.location_text.enabled = False
        
        unlocked_lesson = None
        if quest.next_quest_id:
            next_q = self.quest_manager.get_quest(quest.next_quest_id)
            if next_q:
                unlocked_lesson = next_q.title
                
        QuestNotification.show_quest_completed(camera.ui, quest.title, unlocked_lesson, 3.0)
