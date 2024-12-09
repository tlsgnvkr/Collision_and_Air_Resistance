# DISCLAIMER: In example, 1px of the program is replaced by 0.5cm in the real world.
# Please UNIFORM UNITS when changing the values of variables and constants.

# VARIABLES

FPS = 360                       # Frame per second

WIDTH = 800                     # Width of the monitor
HEIGHT = 600                    # Height of the monitor
WALL = 2                        # Thickness of the wall

COR = 0.7                       # Coefficient of Restitution

## VARIABLES of ball_1

BALL_1_X = WIDTH // 2           # Start Position's x-coordinate
BALL_1_Y = HEIGHT // 2          # Start Position's y-coordinate
BALL_1_R = 12.5                 # Radius
BALL_1_M = 10                   # mass
BALL_1_VX = 0                   # Starting speed in the x-axis direction
BALL_1_VY = 0                   # Starting speed in the y-axis direction

## VARIABLES of ball_2

BALL_2_X = WIDTH // 2 + 10      # Start Position's x-coordinate
BALL_2_Y = 20                   # Start Position's y-coordinate
BALL_2_R = 12.5                 # Radius
BALL_2_M = 15                   # mass
BALL_2_VX = 0                   # Starting speed in the x-axis direction
BALL_2_VY = 1000                # Starting speed in the y-axis direction

# VARIABLES End

# CONSTANTS: DO NOT MODIFY IT IF POSSIBLE.

RHO = 1.225 / (8 * 10 ** 6)     # Density of Air
CD = 0.47                       # Drag Coefficient
G = -1960                       # Gravity

COLORS = {
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "black": (0, 0, 0),
    "cyan": (0, 255, 255),
}                               # Colors

## CONSTANTS of wall_U

WALL_U_X = WIDTH // 2           # Position's x-coordinate
WALL_U_Y = HEIGHT - WALL // 2   # Position's y-coordinate
WALL_U_W = WIDTH                # Width
WALL_U_H = WALL                 # Height

## CONSTANTS of wall_L

WALL_L_X = WALL // 2            # Position's x-coordinate
WALL_L_Y = HEIGHT // 2          # Position's y-coordinate
WALL_L_W = WALL                 # Width
WALL_L_H = HEIGHT               # Height

## CONSTANTS of wall_D

WALL_D_X = WIDTH // 2           # Position's x-coordinate
WALL_D_Y = WALL // 2            # Position's y-coordinate
WALL_D_W = WIDTH                # Width
WALL_D_H = WALL                 # Height

## CONSTANTS of WALL_R

WALL_R_X = WIDTH - WALL // 2    # Position's x-coordinate
WALL_R_Y = HEIGHT // 2          # Position's y-coordinate
WALL_R_W = WALL                 # Width
WALL_R_H = HEIGHT               # Height

# CONSTANTS End
