"""Game settings for the first MVP iteration."""

from ursina import color

# World
CHUNK_SIZE = 16
WORLD_HEIGHT = 32
BASE_HEIGHT = 8
HEIGHT_VARIATION = 2

# Keep first run light-weight to avoid long black loading screens.
# 0 = one chunk, 1 = 3x3 chunks.
CHUNK_GRID_RADIUS = 0

# Player
PLAYER_START_POSITION = (8, 12, 8)
PLAYER_SPEED = 5
PLAYER_JUMP_HEIGHT = 1.2
PLAYER_GRAVITY = 1

# Make initial view point slightly towards terrain.
PLAYER_INITIAL_YAW = 45
PLAYER_INITIAL_PITCH = -15

# Visuals
SKY_COLOR = color.rgb(135, 206, 235)
AMBIENT_LIGHT_COLOR = color.rgba(255, 255, 255, 0.55)
SUNLIGHT_COLOR = color.rgb(255, 244, 214)
SUNLIGHT_DIRECTION = (1, -1, -0.6)
