"""Chunk representation with face-culling mesh generation."""

from dataclasses import dataclass

from ursina import Entity, Mesh

from settings import CHUNK_SIZE
from world.blocks import BLOCK_COLORS, BLOCK_TEXTURES, BlockType
from world.generator import surface_height

Face = tuple[tuple[int, int, int], tuple[tuple[float, float, float], ...]]

FACES: tuple[Face, ...] = (
    ((1, 0, 0), ((1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1))),
    ((-1, 0, 0), ((0, 0, 1), (0, 1, 1), (0, 1, 0), (0, 0, 0))),
    ((0, 1, 0), ((0, 1, 1), (1, 1, 1), (1, 1, 0), (0, 1, 0))),
    ((0, -1, 0), ((0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1))),
    ((0, 0, 1), ((1, 0, 1), (1, 1, 1), (0, 1, 1), (0, 0, 1))),
    ((0, 0, -1), ((0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0))),
)


@dataclass(frozen=True)
class ChunkCoord:
    x: int
    z: int


class Chunk(Entity):
    """Generated chunk with one mesh per block type."""

    def __init__(self, coord: ChunkCoord, seed: int):
        super().__init__()
        self.coord = coord
        self.seed = seed
        self.blocks: dict[tuple[int, int, int], BlockType] = {}
        self._mesh_entities: list[Entity] = []
        self._build_block_map()
        self.rebuild_mesh()

    def _build_block_map(self) -> None:
        origin_x = self.coord.x * CHUNK_SIZE
        origin_z = self.coord.z * CHUNK_SIZE

        for local_x in range(CHUNK_SIZE):
            for local_z in range(CHUNK_SIZE):
                world_x = origin_x + local_x
                world_z = origin_z + local_z
                top_y = surface_height(world_x, world_z, self.seed)
                for y in range(top_y + 1):
                    self.blocks[(world_x, y, world_z)] = _block_type_for_y(y, top_y)

    def set_block(self, position: tuple[int, int, int], block: BlockType | None) -> None:
        if block is None:
            self.blocks.pop(position, None)
        else:
            self.blocks[position] = block
        self.rebuild_mesh()

    def get_block(self, position: tuple[int, int, int]) -> BlockType | None:
        return self.blocks.get(position)

    def rebuild_mesh(self) -> None:
        for mesh_entity in self._mesh_entities:
            mesh_entity.disable()
            mesh_entity.model = None
        self._mesh_entities.clear()

        block_sets: dict[BlockType, set[tuple[int, int, int]]] = {
            block_type: set() for block_type in BlockType
        }
        for position, block_type in self.blocks.items():
            block_sets[block_type].add(position)

        for block_type, positions in block_sets.items():
            if not positions:
                continue

            vertices: list[tuple[float, float, float]] = []
            triangles: list[tuple[int, int, int]] = []
            uvs: list[tuple[float, float]] = []
            index = 0

            for x, y, z in positions:
                for (nx, ny, nz), face_vertices in FACES:
                    neighbor = (x + nx, y + ny, z + nz)
                    if neighbor in self.blocks:
                        continue

                    for vx, vy, vz in face_vertices:
                        vertices.append((x + vx, y + vy, z + vz))
                    triangles.append((index, index + 1, index + 2))
                    triangles.append((index, index + 2, index + 3))
                    uvs.extend(((0, 0), (0, 1), (1, 1), (1, 0)))
                    index += 4

            if not vertices:
                continue

            mesh = Mesh(vertices=vertices, triangles=triangles, uvs=uvs, mode="triangle")
            mesh_entity = Entity(
                parent=self,
                model=mesh,
                texture=BLOCK_TEXTURES[block_type],
                color=BLOCK_COLORS[block_type],
                collider="mesh",
            )
            self._mesh_entities.append(mesh_entity)


def _block_type_for_y(y: int, top_y: int) -> BlockType:
    if y == 0:
        return BlockType.BEDROCK
    if y == top_y:
        return BlockType.GRASS
    return BlockType.STONE
