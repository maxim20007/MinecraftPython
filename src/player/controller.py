"""Player controller setup."""

from ursina import color
from ursina.prefabs.first_person_controller import FirstPersonController

from settings import (
    CURSOR_COLOR,
    PLAYER_GRAVITY,
    PLAYER_INITIAL_PITCH,
    PLAYER_INITIAL_YAW,
    PLAYER_JUMP_HEIGHT,
    PLAYER_SPEED,
)


def create_player(start_position: tuple[float, float, float]) -> FirstPersonController:
    player = FirstPersonController(
        position=start_position,
        speed=PLAYER_SPEED,
        jump_height=PLAYER_JUMP_HEIGHT,
        gravity=PLAYER_GRAVITY,
    )
    player.rotation_y = PLAYER_INITIAL_YAW
    player.camera_pivot.rotation_x = PLAYER_INITIAL_PITCH
    player.cursor.visible = True
    player.cursor.color = CURSOR_COLOR if CURSOR_COLOR else color.white
    player.cursor.scale = 0.02
    return player
