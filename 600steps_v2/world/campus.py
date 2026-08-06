"""
Defines the Campus environment and layout.
"""
from ursina import Entity, color
import utils.constants as const

class Campus:
    """
    Constructs the physical layout of the campus, including ground, roads, and buildings.
    Operates independently of gameplay logic, players, or cameras.
    """
    
    def __init__(self) -> None:
        """Initializes and builds the campus environment."""
        self.entities = []
        self.obstacles = []
        self._build_ground()
        self._build_roads()
        self._build_buildings()

    def _build_ground(self) -> None:
        """Creates the main grassy ground plane."""
        ground = Entity(
            model='plane',
            scale=const.GROUND_SCALE,
            color=color.green,
            collider='box',
            position=(0, 0, 0)
        )
        self.entities.append(ground)

    def _build_roads(self) -> None:
        """Creates the road network connecting all areas."""
        y_road = 0.05  # Slightly above ground to prevent Z-fighting
        
        # Central vertical road (from Spawn at Z=0 to Exam at Z=80)
        road_main = Entity(
            model='cube',
            scale=(const.ROAD_WIDTH, 0.1, 80.0),
            color=color.gray,
            position=(0, y_road, 40.0)
        )
        
        # Horizontal road 1 (Connects Grammar and Vocabulary at Z=20)
        road_h1 = Entity(
            model='cube',
            scale=(40.0, 0.1, const.ROAD_WIDTH),
            color=color.gray,
            position=(0, y_road, const.POS_VOCABULARY[1])
        )
        
        # Horizontal road 2 (Connects Reading and Listening at Z=50)
        road_h2 = Entity(
            model='cube',
            scale=(40.0, 0.1, const.ROAD_WIDTH),
            color=color.gray,
            position=(0, y_road, const.POS_LISTENING[1])
        )
        
        self.entities.extend([road_main, road_h1, road_h2])

    def _build_buildings(self) -> None:
        """Creates the learning area buildings with specific colors."""
        y_pos = const.BUILDING_SCALE[1] / 2  # Rest perfectly on the ground
        
        # Vocabulary Building (Blue)
        vocab = Entity(
            model='cube',
            scale=const.BUILDING_SCALE,
            color=color.blue,
            collider='box',
            position=(const.POS_VOCABULARY[0], y_pos, const.POS_VOCABULARY[1])
        )
        
        # Grammar Building (Yellow)
        grammar = Entity(
            model='cube',
            scale=const.BUILDING_SCALE,
            color=color.yellow,
            collider='box',
            position=(const.POS_GRAMMAR[0], y_pos, const.POS_GRAMMAR[1])
        )
        
        # Reading Building (Orange)
        reading = Entity(
            model='cube',
            scale=const.BUILDING_SCALE,
            color=color.orange,
            collider='box',
            position=(const.POS_READING[0], y_pos, const.POS_READING[1])
        )
        
        # Listening Building (Magenta instead of purple)
        listening = Entity(
            model='cube',
            scale=const.BUILDING_SCALE,
            color=color.magenta,
            collider='box',
            position=(const.POS_LISTENING[0], y_pos, const.POS_LISTENING[1])
        )
        
        # Exam Building (Red, larger)
        exam_y_pos = const.EXAM_BUILDING_SCALE[1] / 2
        exam = Entity(
            model='cube',
            scale=const.EXAM_BUILDING_SCALE,
            color=color.red,
            collider='box',
            position=(const.POS_EXAM[0], exam_y_pos, const.POS_EXAM[1])
        )
        
        self.entities.extend([vocab, grammar, reading, listening, exam])
        self.obstacles.extend([vocab, grammar, reading, listening, exam])
