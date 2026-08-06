"""
Defines the Campus environment and layout.
"""
from ursina import Entity, color
import utils.constants as const
from .building import Building

class Campus:
    """
    Constructs the physical layout of the campus, including ground, roads, and buildings.
    Operates independently of gameplay logic, players, or cameras.
    """
    
    def __init__(self) -> None:
        """Initializes and builds the campus environment."""
        self.entities = []
        self.obstacles = []
        self.buildings = []
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
        
        # Vocabulary Building
        vocab = Building(
            name="Vocabulary",
            category="vocabulary",
            position=(const.POS_VOCABULARY[0], y_pos, const.POS_VOCABULARY[1]),
            scale=const.BUILDING_SCALE,
            building_color=color.blue,
            entrance_position=(16.0, 0.0, 20.0)
        )
        
        # Grammar Building
        grammar = Building(
            name="Grammar",
            category="grammar",
            position=(const.POS_GRAMMAR[0], y_pos, const.POS_GRAMMAR[1]),
            scale=const.BUILDING_SCALE,
            building_color=color.yellow,
            entrance_position=(-16.0, 0.0, 20.0)
        )
        
        # Reading Building
        reading = Building(
            name="Reading",
            category="reading",
            position=(const.POS_READING[0], y_pos, const.POS_READING[1]),
            scale=const.BUILDING_SCALE,
            building_color=color.orange,
            entrance_position=(-16.0, 0.0, 50.0)
        )
        
        # Listening Building
        listening = Building(
            name="Listening",
            category="listening",
            position=(const.POS_LISTENING[0], y_pos, const.POS_LISTENING[1]),
            scale=const.BUILDING_SCALE,
            building_color=color.magenta,
            entrance_position=(16.0, 0.0, 50.0)
        )
        
        # Exam Building
        exam_y_pos = const.EXAM_BUILDING_SCALE[1] / 2
        exam = Building(
            name="Exam",
            category="exam",
            position=(const.POS_EXAM[0], exam_y_pos, const.POS_EXAM[1]),
            scale=const.EXAM_BUILDING_SCALE,
            building_color=color.red,
            entrance_position=(0.0, 0.0, 74.0)
        )
        
        self.buildings.extend([vocab, grammar, reading, listening, exam])
        
        # Add visual entities to tracking lists
        for b in self.buildings:
            self.entities.append(b.entity)
            self.entities.append(b.entrance_indicator)
            self.obstacles.append(b.entity)
