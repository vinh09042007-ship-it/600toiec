from ursina import Entity, Text, color, invoke, destroy

class ComboPopup:
    """
    Spawns temporary floating text on the UI layer.
    """
    @staticmethod
    def show(camera_ui, text: str, position: tuple[float, float] = (0, 0), popup_color=color.yellow):
        # Create text entity
        popup = Text(
            parent=camera_ui,
            text=text,
            position=position,
            origin=(0, 0),
            scale=3,
            color=popup_color
        )
        
        # Simple animation: move up slightly over time
        def animate():
            if popup:
                popup.y += 0.005
                popup.alpha -= 0.02
                
        # Register to Ursina's update loop using a dummy entity
        # We use a dummy entity to run the animation update
        animator = Entity(parent=camera_ui)
        animator.update = animate
        
        # Destroy after 1.5 seconds
        invoke(destroy, popup, delay=1.5)
        invoke(destroy, animator, delay=1.5)
