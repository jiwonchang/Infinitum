import pygame
from os import path

TITLE = "Shoot 'Em Up"

# Game options / settings
# by default, WIDTH = 480, HEIGHT = 600
# so width is about 32 * 57
WIDTH = 1856
# and height is about 32 * 32
HEIGHT = 1024
FPS = 60

# power up time should be 5000 milliseconds (5 seconds) but can make longer for testing purposes
POWERUP_TIME = 10000

# shield regen rate
SHIELD_REGEN_TIME = 10

# color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTGREY = (100, 100, 100)

# Directories
img_dir = path.join(path.dirname(__file__), 'img')
sfx_dir = path.join(path.dirname(__file__), 'sfx')

PLAYER_SPEED = 10

GRIDSIZE = 32
GRIDWIDTH = WIDTH / GRIDSIZE
GRIDHEIGHT = HEIGHT / GRIDSIZE

vec = pygame.math.Vector2

def cross(v1, v2):
    a = (v1[0], v1[1], 0)
    b = (v2[0], v2[1], 0)
    cross_prod = [a[1]*b[2] - a[2]*b[1],
                  a[2]*b[0] - a[0]*b[2],
                  a[0]*b[1] - a[1]*b[0]]
    return cross_prod[2]
