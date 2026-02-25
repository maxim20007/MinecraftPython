"""Game settings for the first MVP iteration."""

from ursina import color

# World
CHUNK_SIZE = 16
WORLD_HEIGHT = 32
BASE_HEIGHT = 8
HEIGHT_VARIATION = 2

# Chunks generated around origin.
# 0 = one chunk, 1 = 3x3 chunks.
CHUNK_GRID_RADIUS = 1

# Player
PLAYER_START_POSITION = (8, 18, 8)
PLAYER_SPEED = 5
PLAYER_JUMP_HEIGHT = 1.2
PLAYER_GRAVITY = 1

# Visuals
SKY_COLOR = color.rgb(135, 206, 235)
AMBIENT_LIGHT_COLOR = color.rgba(255, 255, 255, 0.35)
SUNLIGHT_COLOR = color.rgb(255, 244, 214)
SUNLIGHT_DIRECTION = (1, -1, -0.6)
