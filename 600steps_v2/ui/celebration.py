from ursina import Entity, Text, color, invoke, destroy, curve

class QuestCelebration(Entity):
    """
    Displays a grand celebration overlay when a quest is completed.
    Subscribes to EventBus.
    """
    def __init__(self, camera_ui, event_bus):
        super().__init__(parent=camera_ui)
        self.camera_ui = camera_ui
        
        # Subscribe to event
        from core.events import Events
        event_bus.subscribe(Events.QUEST_COMPLETED, self.show_celebration)
        
    def show_celebration(self, quest, **kwargs):
        # Create a temporary container for the celebration
        container = Entity(parent=self.camera_ui, scale=0.1)
        
        # Semi-transparent background
        bg = Entity(parent=container, model='quad', color=color.rgba(0, 0, 0, 0.6), scale=(2, 1), position=(0, 0, 1))
        
        title = Text(
            parent=container,
            text="✔ Quest Complete!",
            origin=(0, 0),
            position=(0, 0.2),
            scale=5,
            color=color.green
        )
        
        rewards_text = f"+{quest.reward_coin} Coins\n+{quest.reward_exp} EXP"
        rewards = Text(
            parent=container,
            text=rewards_text,
            origin=(0, 0),
            position=(0, -0.1),
            scale=3,
            color=color.gold
        )
        
        # Add unlock text if applicable
        unlocks = {
            "tutorial_grammar": "Grammar Hall Unlocked!",
            "grammar_lesson": "Reading Hall Unlocked!",
            "reading_lesson": "Listening Hall Unlocked!",
            "listening_lesson": "Office Unlocked!",
            "office_quest": "Exam Center Unlocked!"
        }
        
        if quest.id in unlocks:
            unlock_text = Text(
                parent=container,
                text=unlocks[quest.id],
                origin=(0, 0),
                position=(0, -0.3),
                scale=2.5,
                color=color.cyan
            )
            
        # Animate in
        container.animate_scale(1, duration=0.5, curve=curve.out_back)
        
        # Animate out after 3 seconds
        invoke(container.animate_scale, 0, duration=0.3, curve=curve.in_back, delay=3.0)
        
        # Destroy entirely after animation finishes
        invoke(destroy, container, delay=3.4)
