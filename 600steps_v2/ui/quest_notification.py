from ursina import Entity, Text, color, Sequence, Wait, Func, destroy

class QuestNotification:
    """
    Displays brief, non-blocking notifications for quest progress and building unlocks.
    """
    
    @staticmethod
    def show_quest_completed(camera_ui, quest_title: str, unlocked_lesson: str = None, duration: float = 3.0):
        bg = Entity(
            parent=camera_ui,
            model='quad',
            color=color.rgba(0, 0, 0, 0),
            scale=(0.6, 0.25),
            position=(0, 0.35) # Top-center
        )
        
        header = Text(
            parent=bg,
            text="✔ Quest Completed",
            origin=(0, 0),
            position=(0, 0.25),
            scale=3,
            color=color.rgba(0, 255, 0, 0)
        )
        
        title = Text(
            parent=bg,
            text=quest_title,
            origin=(0, 0),
            position=(0, -0.05),
            scale=3,
            color=color.rgba(255, 215, 0, 0)
        )
        
        if unlocked_lesson:
            unlocked = Text(
                parent=bg,
                text=f"+ {unlocked_lesson} Unlocked",
                origin=(0, 0),
                position=(0, -0.35),
                scale=2,
                color=color.rgba(0, 255, 255, 0)
            )
        else:
            unlocked = None
            
        # Fade in
        bg.animate_color(color.rgba(0, 0, 0, 0.8), duration=0.3)
        header.animate_color(color.green, duration=0.3)
        title.animate_color(color.gold, duration=0.3)
        if unlocked:
            unlocked.animate_color(color.cyan, duration=0.3)
            
        # Fade out and destroy
        def fade_out():
            bg.animate_color(color.rgba(0, 0, 0, 0), duration=0.5)
            header.animate_color(color.rgba(0, 255, 0, 0), duration=0.5)
            title.animate_color(color.rgba(255, 215, 0, 0), duration=0.5)
            if unlocked:
                unlocked.animate_color(color.rgba(0, 255, 255, 0), duration=0.5)
                
        def remove():
            destroy(bg)
            
        Sequence(
            Wait(duration),
            Func(fade_out),
            Wait(0.5),
            Func(remove)
        ).start()
        
    @staticmethod
    def show_building_unlocked(camera_ui, building_name: str, duration: float = 2.0):
        bg = Entity(
            parent=camera_ui,
            model='quad',
            color=color.rgba(0, 0, 0, 0),
            scale=(0.5, 0.15),
            position=(0, 0.35) # Top-center
        )
        
        if building_name.lower() == "exam" or building_name.lower() == "exam center":
            bg.scale = (1.0, 0.4)
            display_text = "FINAL TOEIC EXAM UNLOCKED!\n\nCongratulations!\nAll learning buildings have been completed.\nThe Final TOEIC Exam is now available."
            duration = max(duration, 5.0)
        else:
            display_text = f"[{building_name} Building Unlocked]"
            
        text = Text(
            parent=bg,
            text=display_text,
            origin=(0, 0),
            position=(0, 0),
            scale=2.5,
            color=color.rgba(0, 255, 255, 0)
        )
        
        # Fade in
        bg.animate_color(color.rgba(0, 0, 0, 0.8), duration=0.3)
        text.animate_color(color.cyan, duration=0.3)
        
        # Fade out and destroy
        def fade_out():
            bg.animate_color(color.rgba(0, 0, 0, 0), duration=0.5)
            text.animate_color(color.rgba(0, 255, 255, 0), duration=0.5)
            
        def remove():
            destroy(bg)
            
        Sequence(
            Wait(duration),
            Func(fade_out),
            Wait(0.5),
            Func(remove)
        ).start()
