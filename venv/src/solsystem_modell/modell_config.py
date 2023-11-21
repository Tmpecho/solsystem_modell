# Simulation Dimensions
SIMULATION_WIDTH: int = 1100
SIMULATION_HEIGHT: int = 800

# Constants
TRAIL_UPDATE_INTERVAL: float = 0.001
FONT_SIZE: int = 20
GAMMA: float = 6.674010551359e-11
AU: float = 1.495978707e11
LINE_SKIP_FACTOR: int = 3
SCALE_FACTOR: int = 10  # default = 100
DEFAULT_OBJECT_SIZE: int = 5
SIZE_SCALING_FACTOR = 100

# File Paths
DATA_FILE_PATH_ROOT: str = "venv/src/solsystem_modell/"

# Colors
WHITE: tuple[int, int, int] = (255, 255, 255)
BLACK: tuple[int, int, int] = (0, 0, 0)

# Settings
SIMULATION_YEARS: int = 100

DEBUG_MODE: bool = True
IS_SUN_STATIONARY: bool = True
ZOOM: float = 1.5  # set to 1.5 to see all planets, 20 for inner planets
TIME_ACCELERATION: int = int(1e7)  # default = 1e6
TO_SCALE: bool = False
SHOW_GRAPHICAL_VIEW: bool = True  # Setting to True makes the program run mcuh slower and will be affected by lag
