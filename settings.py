import pygame
from os import path

TITLE = "Shoot 'Em Up"

# Game options / settings
# by default, WIDTH = 480, HEIGHT = 600
# so width is about 32 * 58
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
GREY = (128, 128, 128)
#BUTTON_LIGHT_BLUE = (0, 50, 135, 50)
#BUTTON_SELECTED_BLUE = (51, 105, 205, 50)
#UI_BOX_BLUE = (0, 32, 105, 50)
BUTTON_LIGHT_BLUE = (0, 50, 135)
BUTTON_SELECTED_BLUE = (51, 105, 205)
UI_BOX_BLUE = (0, 32, 105)

# Directories
img_dir = path.join(path.dirname(__file__), 'img')
sfx_dir = path.join(path.dirname(__file__), 'sfx')
font_dir = path.join(path.dirname(__file__), 'font')

#PLAYER_SPEED = 10

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


bomber_ten_squad_coords = [(WIDTH * (1/11), 128), (WIDTH * (2/11), 128), (WIDTH * (3/11), 128), (WIDTH * (4/11), 128),
                    (WIDTH * (5/11), 128), (WIDTH * (6/11), 128), (WIDTH * (7/11), 128), (WIDTH * (8/11), 128),
                    (WIDTH * (9/11), 128), (WIDTH * (10/11), 128)]
cruiser1_eight_squad_coords = [(WIDTH * (1/9), 128), (WIDTH * (2/9), 128), (WIDTH * (3/9), 128), (WIDTH * (4/9), 128),
                    (WIDTH * (5/9), 128), (WIDTH * (6/9), 128), (WIDTH * (7/9), 128), (WIDTH * (8/9), 128)]
cruiser1_six_squad_coords = [(WIDTH * (1/7), 128), (WIDTH * (2/7), 128), (WIDTH * (3/7), 128), (WIDTH * (4/7), 128),
                    (WIDTH * (5/7), 128), (WIDTH * (6/7), 128)]

item_prices = {}
item_prices['gun_power_up'] = 5000
item_prices['gun_2shot_up'] = 7000
item_prices['gun_speed_up'] = 10000
item_prices['shield_up'] = 5000
item_prices['missile_up'] = 10000
item_prices['h_missile_up'] = 15000
item_prices['ship_plating_up'] = 5000
item_prices['booster_up'] = 6000

item_prices['Amethyst Ore'] = 150
item_prices['Aquamarine Ore'] = 180
item_prices['Bronze Ore'] = 80
item_prices['Diamond Ore'] = 300
item_prices['Emerald Ore'] = 220
item_prices['Garnet Ore'] = 100
item_prices['Gold Ore'] = 200
item_prices['Sapphire Ore'] = 210
item_prices['Silver Ore'] = 140
item_prices['Steel Ore'] = 100
item_prices['Titanium Ore'] = 200
item_prices['Topaz Ore'] = 160

item_prices['Amethyst'] = 1800
item_prices['Aquamarine'] = 2160
item_prices['Bronze Plate'] = 960
item_prices['Diamond'] = 3600
item_prices['Emerald'] = 2640
item_prices['Garnet'] = 1200
item_prices['Gold Plate'] = 2400
item_prices['Sapphire'] = 2520
item_prices['Silver Plate'] = 1680
item_prices['Steel Plate'] = 1200
item_prices['Titanium Plate'] = 2400
item_prices['Topaz'] = 1920