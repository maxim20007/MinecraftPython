"""Entry point for the first playable Minecraft-like prototype."""

import random

from ursina import AmbientLight, DirectionalLight, Ursina, Vec3, window
from ursina.prefabs.sky import Sky

from player.controller import create_player
from settings import (
    AMBIENT_LIGHT_COLOR,
    CHUNK_GRID_RADIUS,
    CHUNK_SIZE,
    PLAYER_SPAWN_HEIGHT_OFFSET,
    SKY_COLOR,
    SUNLIGHT_COLOR,
    SUNLIGHT_DIRECTION,
)
from world.chunk import Chunk, ChunkCoord
from world.generator import surface_height


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


def choose_spawn(seed: int) -> tuple[float, float, float]:
    center_x = CHUNK_SIZE // 2
    center_z = CHUNK_SIZE // 2
    y = surface_height(center_x, center_z, seed) + PLAYER_SPAWN_HEIGHT_OFFSET
    return (center_x, y, center_z)


def main() -> None:
    app = Ursina(title="Minecraft Python MVP")

    window.color = SKY_COLOR
    window.exit_button.visible = False
    window.fps_counter.enabled = True

    Sky()
    setup_lighting()

    seed = random.randint(0, 10_000_000)
    _chunks = build_world(seed)
    _player = create_player(choose_spawn(seed))

    app.run()


if __name__ == "__main__":
    main()
