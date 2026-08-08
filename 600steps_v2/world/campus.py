"""
Defines the Campus environment and layout.
"""
from ursina import Entity, color, Sky
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
        self._build_decorations()

    def _build_ground(self) -> None:
        """Creates the main grassy ground plane and Sky."""
        ground = Entity(
            model='plane',
            scale=const.GROUND_SCALE,
            color=color.rgb(100/255, 180/255, 100/255), # Softer, more natural grass green
            collider='box',
            position=(0, 0, 0)
        )
        # Safe normalized sky color to prevent HDR overexposure
        sky = Sky(color=color.rgb(0.6, 0.8, 0.9))
        self.entities.extend([ground, sky])

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
        sidewalk_main = Entity(
            model='cube',
            scale=(const.ROAD_WIDTH + 2, 0.05, 80.0),
            color=color.light_gray,
            position=(0, y_road - 0.01, 40.0)
        )
        
        # Horizontal road 1 (Connects Grammar and Vocabulary at Z=20)
        road_h1 = Entity(
            model='cube',
            scale=(40.0, 0.1, const.ROAD_WIDTH),
            color=color.gray,
            position=(0, y_road, const.POS_VOCABULARY[1])
        )
        sidewalk_h1 = Entity(
            model='cube',
            scale=(40.0, 0.05, const.ROAD_WIDTH + 2),
            color=color.light_gray,
            position=(0, y_road - 0.01, const.POS_VOCABULARY[1])
        )
        
        # Horizontal road 2 (Connects Reading and Listening at Z=50)
        road_h2 = Entity(
            model='cube',
            scale=(40.0, 0.1, const.ROAD_WIDTH),
            color=color.gray,
            position=(0, y_road, const.POS_LISTENING[1])
        )
        sidewalk_h2 = Entity(
            model='cube',
            scale=(40.0, 0.05, const.ROAD_WIDTH + 2),
            color=color.light_gray,
            position=(0, y_road - 0.01, const.POS_LISTENING[1])
        )
        
        self.entities.extend([road_main, sidewalk_main, road_h1, sidewalk_h1, road_h2, sidewalk_h2])

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

    def _build_decorations(self) -> None:
        """Adds trees, streetlamps, and benches to the campus."""
        
        # Helper for Trees (Multi-part foliage)
        def add_tree(x, z):
            trunk = Entity(model='cylinder', color=color.rgb(139/255, 69/255, 19/255), scale=(1, 4, 1), position=(x, 2, z))
            leaf_base = Entity(model='sphere', color=color.rgb(44/255, 149/255, 44/255), scale=(4.5, 3.5, 4.5), position=(x, 4.5, z))
            leaf_mid = Entity(model='sphere', color=color.rgb(54/255, 159/255, 54/255), scale=(3.5, 3.5, 3.5), position=(x, 5.5, z))
            leaf_top = Entity(model='sphere', color=color.rgb(64/255, 169/255, 64/255), scale=(2.5, 2.5, 2.5), position=(x, 6.5, z))
            self.entities.extend([trunk, leaf_base, leaf_mid, leaf_top])
            self.obstacles.append(trunk)
            
        # Helper for Bushes & Flowers
        def add_bush(x, z):
            bush = Entity(model='sphere', color=color.rgb(40/255, 130/255, 40/255), scale=(2, 1.5, 2), position=(x, 0.5, z))
            flower1 = Entity(model='sphere', color=color.rgb(1.0, 0.4, 0.6), scale=(0.3, 0.3, 0.3), position=(x+0.5, 1.2, z+0.5))
            flower2 = Entity(model='sphere', color=color.rgb(0.9, 0.8, 0.2), scale=(0.3, 0.3, 0.3), position=(x-0.5, 1.1, z-0.2))
            self.entities.extend([bush, flower1, flower2])
            self.obstacles.append(bush)
            
        # Trees along the outer border
        for z in range(0, 90, 15):
            add_tree(-35, z)
            add_tree(35, z)
        
        # Trees bridging the empty space between building rows
        add_tree(-20, 35)
        add_tree(20, 35)
        add_tree(-20, 5)
        add_tree(20, 5)
            
        # Benches near buildings (avoiding entrances and roads)
        def add_bench(x, z, rot_y=0):
            seat = Entity(model='cube', color=color.rgb(160/255, 82/255, 45/255), scale=(2, 0.2, 0.8), position=(x, 0.6, z), rotation_y=rot_y)
            legs1 = Entity(model='cube', color=color.dark_gray, scale=(0.2, 0.6, 0.8), position=(x-0.8, 0.3, z), rotation_y=rot_y)
            legs2 = Entity(model='cube', color=color.dark_gray, scale=(0.2, 0.6, 0.8), position=(x+0.8, 0.3, z), rotation_y=rot_y)
            self.entities.extend([seat, legs1, legs2])
            self.obstacles.extend([seat, legs1, legs2])
            
        add_bench(-20, 12, rot_y=0)  # Near Grammar
        add_bench(20, 12, rot_y=0)   # Near Vocab
        add_bench(-20, 42, rot_y=0)  # Near Reading
        # Bushes and Flowers scattered safely
        add_bush(-10, 10)
        add_bush(10, 10)
        add_bush(-15, 30)
        add_bush(15, 30)
        add_bush(-8, 60)
        add_bush(8, 60)
        
        # Palm Trees (3D model decorations)
        palm_model = 'assets/models/palm_tree/base'
        palm_texture = 'assets/models/palm_tree/texture_diffuse.png'
        
        def add_palm_tree(x, z, scale=1.5, rot_y=0):
            palm = Entity(
                model=palm_model,
                texture=palm_texture,
                scale=scale,
                position=(x, 0, z),
                rotation_y=rot_y
            )
            self.entities.append(palm)
            self.obstacles.append(palm)
        
        # Near Grammar Building (left side, Z~20)
        add_palm_tree(-25, 14, scale=1.4, rot_y=10)
        add_palm_tree(-25, 26, scale=1.6, rot_y=45)
        
        # Near Vocabulary Building (right side, Z~20)
        add_palm_tree(25, 14, scale=1.5, rot_y=120)
        add_palm_tree(25, 26, scale=1.3, rot_y=200)
        
        # Near Reading Building (left side, Z~50)
        add_palm_tree(-25, 44, scale=1.6, rot_y=75)
        add_palm_tree(-25, 56, scale=1.4, rot_y=160)
        
        # Near Listening Building (right side, Z~50)
        add_palm_tree(25, 44, scale=1.5, rot_y=250)
        add_palm_tree(25, 56, scale=1.7, rot_y=310)
        
        # Near Exam Building (top area, Z~80)
        add_palm_tree(-10, 78, scale=1.3, rot_y=30)
        add_palm_tree(10, 78, scale=1.5, rot_y=190)
        
        # Entrance area (near spawn)
        add_palm_tree(-8, 2, scale=1.4, rot_y=60)
        add_palm_tree(8, 2, scale=1.3, rot_y=280)
        
        # Campus Welcome Sign
        sign_post = Entity(model='cube', color=color.rgb(139/255, 69/255, 19/255), scale=(0.2, 2, 0.2), position=(3, 1, 2))
        sign_board = Entity(model='cube', color=color.rgb(200/255, 180/255, 140/255), scale=(3, 1, 0.2), position=(3, 1.8, 2), rotation_y=-20)
        from ursina import Text
        sign_text = Text(parent=sign_board, text="600 TOEIC\nCAMPUS", scale=2, origin=(0, 0), color=color.black, position=(0, 0, -0.6))
        self.entities.extend([sign_post, sign_board, sign_text])
        self.obstacles.extend([sign_post])
