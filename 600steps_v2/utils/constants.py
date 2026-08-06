"""
Global constants used across the entire project.
"""

# System constants
GAME_VERSION: str = "0.1.0"
ASSET_FOLDER_NAME: str = "assets"
SAVE_FOLDER_NAME: str = "saves"

# Physics / Entity constants (Placeholders)
PLAYER_SPEED: float = 5.0
PLAYER_GRAVITY: float = -20.0
PLAYER_TERMINAL_VELOCITY: float = -50.0
GROUND_HEIGHT: float = 1.0
INTERACTION_DISTANCE: float = 2.0

# Rendering constants
DEFAULT_LAYER: int = 0
COLLISION_MASK: int = 1

# Camera constants
CAMERA_OFFSET: tuple[float, float, float] = (0.0, 8.0, -12.0)
CAMERA_LERP_SPEED: float = 5.0
