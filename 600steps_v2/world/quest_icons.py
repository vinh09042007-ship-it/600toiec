from ursina import Entity, Text, color

class QuestIcon(Entity):
    """
    Floating 3D icon above an NPC to indicate quest state (!, ?, or ✓).
    """
    def __init__(self, parent_npc, **kwargs):
        super().__init__(
            parent=parent_npc,
            position=(0, 3.5, 0), # Hover above the name label
            **kwargs
        )
        
        self.text_entity = Text(
            parent=self,
            text="",
            scale=8,
            origin=(0, 0),
            billboard=True
        )
        
    def update_state(self, state: str):
        """
        Updates the icon based on quest state.
        Args:
            state: 'offer', 'active', 'ready', or 'none'
        """
        if state == 'offer':
            self.text_entity.text = "!"
            self.text_entity.color = color.yellow
            self.text_entity.enabled = True
        elif state == 'active':
            self.text_entity.text = "?"
            self.text_entity.color = color.gray
            self.text_entity.enabled = True
        elif state == 'ready':
            self.text_entity.text = "?"
            self.text_entity.color = color.green
            self.text_entity.enabled = True
        else:
            self.text_entity.enabled = False
