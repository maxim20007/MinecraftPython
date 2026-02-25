"""Entry point for the first playable Minecraft-like prototype."""

import random

from ursina import Ursina, window

from player.controller import create_player
from settings import CHUNK_GRID_RADIUS, PLAYER_START_POSITION, SKY_COLOR
from world.chunk import Chunk, ChunkCoord


def build_world(seed: int) -> list[Chunk]:
    chunks: list[Chunk] = []
    for chunk_x in range(-CHUNK_GRID_RADIUS, CHUNK_GRID_RADIUS + 1):
        for chunk_z in range(-CHUNK_GRID_RADIUS, CHUNK_GRID_RADIUS + 1):
            chunks.append(Chunk(ChunkCoord(chunk_x, chunk_z), seed=seed))
    return chunks


def main() -> None:
    app = Ursina(title="Minecraft Python MVP")

    window.color = SKY_COLOR
    window.exit_button.visible = False

    seed = random.randint(0, 10_000_000)
    _chunks = build_world(seed)
    _player = create_player(PLAYER_START_POSITION)

    app.run()


if __name__ == "__main__":
    main()
