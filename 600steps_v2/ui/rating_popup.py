from ursina import Entity, Text, color, invoke, destroy

class RatingPopup:
    """
    Displays the final Performance Rating (S, A, B, C) at the end of a mini-game.
    """
    @staticmethod
    def show(camera_ui, rating: str, score: int, coins: int, exp: int):
        bg = Entity(
            parent=camera_ui,
            model='quad',
            color=color.rgba(0, 0, 0, 0.9),
            scale=(1.5, 1.0),
            position=(0, 0)
        )
        
        # Color based on rating
        rank_colors = {
            "S": color.gold,
            "A": color.green,
            "B": color.azure,
            "C": color.red
        }
        r_color = rank_colors.get(rating, color.white)
        
        title = Text(parent=bg, text="PERFORMANCE RATING", origin=(0, 0), position=(0, 0.4), scale=3, color=color.white)
        
        # The big letter rank
        rank_text = Text(parent=bg, text=rating, origin=(0, 0), position=(0, 0.1), scale=15, color=r_color)
        
        stats = Text(
            parent=bg,
            text=f"Score: {score}\nCoins Earned: +{coins}\nEXP Earned: +{exp}",
            origin=(0, 0),
            position=(0, -0.2),
            scale=2,
            color=color.light_gray
        )
        
        instruction = Text(parent=bg, text="Press ESC to Continue", origin=(0, 0), position=(0, -0.4), scale=1.5, color=color.cyan)
        
        # We attach these elements to the bg so we can destroy bg later (not automatic here, managed by scene)
        return bg
