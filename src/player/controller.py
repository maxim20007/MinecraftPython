"""Player controller setup."""

from ursina.prefabs.first_person_controller import FirstPersonController

from settings import PLAYER_GRAVITY, PLAYER_JUMP_HEIGHT, PLAYER_SPEED


def create_player(start_position: tuple[float, float, float]) -> FirstPersonController:
    player = FirstPersonController(
        position=start_position,
        speed=PLAYER_SPEED,
        jump_height=PLAYER_JUMP_HEIGHT,
        gravity=PLAYER_GRAVITY,
    )
    player.cursor.visible = False
    return player
