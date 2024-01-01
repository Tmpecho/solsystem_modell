# Simulation Dimensions
SIMULATION_WIDTH: int = 1100
SIMULATION_HEIGHT: int = 800

# Constants for simulation
GAMMA: float = 6.674010551359e-11
AU: float = 1.495978707e11

TRAIL_UPDATE_INTERVAL: float = 0.001
LINE_SKIP_FACTOR: int = 3
MAX_SIMULATION_YEARS: int = 3000  # Automatically stops the simulation after this many years
TIME_ACCELERATION: int = int(1e6)  # default = 1e6
START_DATE = '1730-01-01'

# File Paths
DATA_FILE_PATH_ROOT: str = 'data/'

# Colors
WHITE: tuple[int, int, int] = (255, 255, 255)
BLACK: tuple[int, int, int] = (0, 0, 0)

# --- RUN SETTINGS ---
DEBUG_MODE: bool = False
IS_SUN_STATIONARY: bool = False
TO_SCALE: bool = False
SHOW_GRAPHICAL_VIEW: bool = True  # Setting to True makes the program run much slower and will be affected by lag

# UI Settings
FONT_SIZE: int = 20

SCALE_FACTOR: int = 100  # default = 100
DEFAULT_OBJECT_SIZE: int = 5
SIZE_SCALING_FACTOR = 1000
ZOOM: float = 15  # set to 1.5 to see all planets, 20 for inner planets
