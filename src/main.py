"""Entry point for the first playable Minecraft-like prototype."""

import random

from ursina import AmbientLight, DirectionalLight, Sky, Ursina, Vec3, window

from player.controller import create_player
from settings import (
    AMBIENT_LIGHT_COLOR,
    CHUNK_GRID_RADIUS,
    PLAYER_START_POSITION,
    SKY_COLOR,
    SUNLIGHT_COLOR,
    SUNLIGHT_DIRECTION,
)
from world.chunk import Chunk, ChunkCoord


def build_world(seed: int) -> list[Chunk]:
    chunks: list[Chunk] = []
    for chunk_x in range(-CHUNK_GRID_RADIUS, CHUNK_GRID_RADIUS + 1):
        for chunk_z in range(-CHUNK_GRID_RADIUS, CHUNK_GRID_RADIUS + 1):
            chunks.append(Chunk(ChunkCoord(chunk_x, chunk_z), seed=seed))
    return chunks


def setup_lighting() -> None:
    AmbientLight(color=AMBIENT_LIGHT_COLOR)
    sun = DirectionalLight(color=SUNLIGHT_COLOR)
    sun.look_at(Vec3(*SUNLIGHT_DIRECTION))


def main() -> None:
    app = Ursina(title="Minecraft Python MVP")

    window.color = SKY_COLOR
    window.exit_button.visible = False

    Sky(color=SKY_COLOR)
    setup_lighting()

    seed = random.randint(0, 10_000_000)
    _chunks = build_world(seed)
    _player = create_player(PLAYER_START_POSITION)

    app.run()


if __name__ == "__main__":
    main()
