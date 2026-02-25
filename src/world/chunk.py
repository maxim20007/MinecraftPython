"""Chunk representation and rendering."""

from dataclasses import dataclass

from ursina import Entity

from settings import CHUNK_SIZE
from world.blocks import BLOCK_COLORS, BlockType
from world.generator import surface_height


@dataclass(frozen=True)
class ChunkCoord:
    x: int
    z: int


class Chunk(Entity):
    """A simple chunk rendered as a collection of colored voxel entities."""

    def __init__(self, coord: ChunkCoord, seed: int):
        super().__init__()
        self.coord = coord
        self.seed = seed
        self._build()

    def _build(self) -> None:
        origin_x = self.coord.x * CHUNK_SIZE
        origin_z = self.coord.z * CHUNK_SIZE

        for local_x in range(CHUNK_SIZE):
            for local_z in range(CHUNK_SIZE):
                world_x = origin_x + local_x
                world_z = origin_z + local_z
                top_y = surface_height(world_x, world_z, self.seed)

                for y in range(top_y + 1):
                    block_type = _block_type_for_y(y, top_y)
                    Entity(
                        parent=self,
                        model="cube",
                        color=BLOCK_COLORS[block_type],
                        position=(world_x, y, world_z),
                        collider="box",
                        texture=None,
                    )


def _block_type_for_y(y: int, top_y: int) -> BlockType:
    if y == 0:
        return BlockType.BEDROCK
    if y == top_y:
        return BlockType.GRASS
    return BlockType.STONE
