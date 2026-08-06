from ursina import Entity, Text, color, invoke, destroy

class RatingPopup:
    """
    Displays the final Performance Rating (S, A, B, C) at the end of a mini-game.
    """
    @staticmethod
    def show(camera_ui, rating: str, score: int, coins: int, exp: int, is_exam: bool = False, correct_answers: int = 0):
        bg = Entity(
            parent=camera_ui,
            model='quad',
            color=color.rgba(0, 0, 0, 0.9),
            scale=(1.5, 1.0),
            position=(0, 0)
        )
        
        if is_exam:
            # Visually scale the score to match TOEIC target of 600 (without changing backend algorithm)
            displayed_score = score * 6
            passed = displayed_score >= 600
            
            status_text = "PASS" if passed else "TRY AGAIN"
            status_color = color.green if passed else color.red
            
            title = Text(parent=bg, text="Final TOEIC Result", origin=(0, 0), position=(0, 0.35), scale=3, color=color.gold)
            
            stats_str = f"Correct Answers: {correct_answers}\nScore: {displayed_score}\nTarget: 600\n\nStatus: "
            stats = Text(
                parent=bg,
                text=stats_str,
                origin=(0, 0),
                position=(0, 0.05),
                scale=2,
                color=color.white
            )
            
            status_display = Text(
                parent=bg,
                text=status_text,
                origin=(-0.5, 0),  # Adjust so it aligns after the word "Status: " visually, or just center it below
                position=(0, -0.1),
                scale=3,
                color=status_color
            )
            
            if passed:
                msg = "Congratulations!\nYou have achieved the required TOEIC score.\nGraduation Ceremony Unlocked!"
            else:
                msg = "You have not yet reached 600.\nYou may study and try again."
                
            feedback = Text(
                parent=bg,
                text=msg,
                origin=(0, 0),
                position=(0, -0.25),
                scale=1.5,
                color=color.cyan
            )
        else:
            # Original rating display
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
            
        instruction = Text(parent=bg, text="Press ESC to Continue", origin=(0, 0), position=(0, -0.45), scale=1.5, color=color.light_gray)
        
        # We attach these elements to the bg so we can destroy bg later (not automatic here, managed by scene)
        return bg
