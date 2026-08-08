"""
Main entry point for 600steps_v2.
"""
from core.game import Game
def main() -> None:
    """Initialize and run the game."""
    game = Game()
    game.run()
if __name__ == "__main__":
    main() 
