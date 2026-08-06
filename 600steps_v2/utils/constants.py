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
CAMERA_OFFSET: tuple[float, float, float] = (0.0, 4.0, -12.0)
CAMERA_LERP_SPEED: float = 5.0

# World / Campus constants
GROUND_SCALE: tuple[float, float, float] = (200.0, 1.0, 200.0)
ROAD_WIDTH: float = 4.0
BUILDING_SCALE: tuple[float, float, float] = (8.0, 6.0, 8.0)
EXAM_BUILDING_SCALE: tuple[float, float, float] = (12.0, 10.0, 12.0)

# Campus Layout Positions (X, Z)
POS_SPAWN: tuple[float, float] = (0.0, 0.0)
POS_VOCABULARY: tuple[float, float] = (20.0, 20.0)
POS_GRAMMAR: tuple[float, float] = (-20.0, 20.0)
POS_LISTENING: tuple[float, float] = (20.0, 50.0)
POS_READING: tuple[float, float] = (-20.0, 50.0)
POS_EXAM: tuple[float, float] = (0.0, 80.0)
