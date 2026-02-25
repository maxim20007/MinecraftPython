"""Game settings for the first MVP iteration."""

from ursina import color

# World
CHUNK_SIZE = 16
WORLD_HEIGHT = 32
BASE_HEIGHT = 8
HEIGHT_VARIATION = 2

# Chunks grid generated around origin for the first iteration.
CHUNK_GRID_RADIUS = 0

# Player
PLAYER_START_POSITION = (8, 18, 8)
PLAYER_SPEED = 5
PLAYER_JUMP_HEIGHT = 1.2
PLAYER_GRAVITY = 1

# Visuals
SKY_COLOR = color.rgb(135, 206, 235)
