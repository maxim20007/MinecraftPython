"""Game settings for the first MVP iteration."""

from ursina import Vec4


def rgb255(r: int, g: int, b: int) -> Vec4:
    """Convert 0-255 RGB values to normalized Ursina color (0-1)."""
    return Vec4(r / 255, g / 255, b / 255, 1)


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
SKY_COLOR = rgb255(135, 206, 235)
AMBIENT_LIGHT_COLOR = Vec4(0.55, 0.55, 0.55, 1)
SUNLIGHT_COLOR = rgb255(255, 244, 214)
SUNLIGHT_DIRECTION = (1, -1, -0.6)
