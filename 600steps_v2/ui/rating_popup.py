from ursina import Entity, Text, color, invoke, destroy, curve

class RatingPopup:
    """
    Displays the final Performance Rating (S, A, B, C) at the end of a mini-game.
    """
    @staticmethod
    def show(camera_ui, rating: str, score: int, coins: int, exp: int, is_exam: bool = False, correct_answers: int = 0, target_score: int = 600):
        bg = Entity(
            parent=camera_ui,
            model='quad',
            color=color.rgba(0, 0, 0, 0.9),
            scale=(1.5, 1.0),
            position=(0, 0)
        )
        
        if is_exam:
            displayed_score = correct_answers * 100
            passed = displayed_score >= target_score
            
            # Animate background
            bg.color = color.rgba(0, 0, 0, 0)
            bg.animate_color(color.rgba(0, 0, 0, 0.95), duration=0.5)
            
            title_text = "🎉 GOAL ACHIEVED!" if passed else "KEEP LEARNING"
            title_color = color.gold if passed else color.azure
            
            title = Text(parent=bg, text=title_text, origin=(0, 0), position=(0, 0.35), scale=0.1, color=color.rgba(title_color.r, title_color.g, title_color.b, 0))
            title.animate_scale(4, duration=0.6, curve=curve.out_back)
            title.animate_color(title_color, duration=0.6)
            
            stats_str = f"Final TOEIC Score:  <gold>{displayed_score}</gold>\nTarget Score:  <light_gray>{target_score}</light_gray>"
            stats = Text(
                parent=bg,
                text=stats_str,
                origin=(0, 0),
                position=(0, 0.1),
                scale=2.5,
                color=color.rgba(255, 255, 255, 0)
            )
            stats.animate_color(color.white, duration=0.8, delay=0.3)
            
            if passed:
                msg = (
                    "Congratulations!\n"
                    "You achieved the TOEIC score you set for yourself.\n\n"
                    "Your hard work has paid off.\n"
                    "Keep learning.\n"
                    "Keep improving.\n"
                    "Aim even higher."
                )
                msg_color = color.green
            else:
                msg = (
                    "You haven't reached your goal yet.\n"
                    "Every practice session makes you stronger.\n\n"
                    "Return to campus,\n"
                    "keep studying,\n"
                    "and try again whenever you're ready."
                )
                msg_color = color.light_gray
                
            feedback = Text(
                parent=bg,
                text=msg,
                origin=(0, 0),
                position=(0, -0.2),
                scale=1.5,
                color=color.rgba(msg_color.r, msg_color.g, msg_color.b, 0)
            )
            feedback.animate_color(msg_color, duration=1.0, delay=0.6)
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
            
        if is_exam:
            instruction = Text(parent=bg, text="Press [ENTER] to Continue", origin=(0, 0), position=(0, -0.45), scale=1.5, color=color.rgba(200,200,200,0))
            instruction.animate_color(color.light_gray, duration=1.0, delay=1.5)
        else:
            instruction = Text(parent=bg, text="Press ESC to Continue", origin=(0, 0), position=(0, -0.45), scale=1.5, color=color.light_gray)
        
        # We attach these elements to the bg so we can destroy bg later (not automatic here, managed by scene)
        return bg
