"""
Core Game class managing the application lifecycle.
"""
from core.eventbus import EventBus
from core.gamestate import GameState
from player.controller import PlayerController
import utils.constants as const
import config

from ursina import Ursina, Sky, Entity, color, time

class GameUpdater(Entity):
    """Hidden entity used solely to hook into Ursina's update loop."""
    def __init__(self, game: 'Game') -> None:
        super().__init__()
        self.game = game
        
    def update(self) -> None:
        self.game._update()

class Game:
    """
    Main game controller responsible for initialization and the main loop.
    """
    def __init__(self) -> None:
        """Initialize core systems."""
        # Ursina MUST be initialized before creating any Entities
        self.app = Ursina(title=config.GAME_TITLE, borderless=config.FULLSCREEN)
        
        self.event_bus: EventBus = EventBus()
        self.state: GameState = GameState.MENU
        self.is_running: bool = False
        print(f"Initializing {config.GAME_TITLE} v{config.VERSION}...")

    def init_systems(self) -> None:
        """Initialize all subsystems and background services."""
        # Simple environment for Phase 2.4
        Sky()
        Entity(model='plane', scale=(20, 1, 20), color=color.dark_gray, collider='box')
        
        # Initialize Player System
        self.player_controller = PlayerController(speed=const.PLAYER_SPEED)
        
        # Hook update loop
        self.updater = GameUpdater(self)

    def run(self) -> None:
        """Start the main game loop."""
        self.init_systems()
        self.is_running = True
        
        # Hand over loop control to Ursina Engine
        self.app.run()

    def _process_events(self) -> None:
        """Handle input and system events."""
        pass

    def _update(self) -> None:
        """Update game logic based on current state."""
        # Called every frame by GameUpdater
        self.player_controller.update(time.dt)

    def _render(self) -> None:
        """Render the current state to the screen."""
        pass

    def quit(self) -> None:
        """Terminate the game loop and clean up."""
        self.is_running = False
        self.state = GameState.EXIT
        print("Shutting down...")
        from ursina import application
        application.quit()
