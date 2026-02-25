"""World management: chunk streaming, cache and block editing."""

from ursina import Vec3

from settings import CHUNK_SIZE, RENDER_DISTANCE_CHUNKS
from world.blocks import BlockType
from world.chunk import Chunk, ChunkCoord


class WorldManager:
    def __init__(self, seed: int):
        self.seed = seed
        self.loaded_chunks: dict[ChunkCoord, Chunk] = {}
        self.chunk_cache: dict[ChunkCoord, Chunk] = {}

    def world_to_chunk(self, x: int, z: int) -> ChunkCoord:
        return ChunkCoord(x // CHUNK_SIZE, z // CHUNK_SIZE)

    def ensure_chunks_around(self, world_position: Vec3) -> None:
        center = self.world_to_chunk(int(world_position.x), int(world_position.z))
        desired: set[ChunkCoord] = set()

        for cx in range(center.x - RENDER_DISTANCE_CHUNKS, center.x + RENDER_DISTANCE_CHUNKS + 1):
            for cz in range(center.z - RENDER_DISTANCE_CHUNKS, center.z + RENDER_DISTANCE_CHUNKS + 1):
                desired.add(ChunkCoord(cx, cz))

        for coord in list(self.loaded_chunks.keys()):
            if coord not in desired:
                chunk = self.loaded_chunks.pop(coord)
                chunk.disable()

        for coord in desired:
            chunk = self.chunk_cache.get(coord)
            if chunk is None:
                chunk = Chunk(coord, self.seed)
                self.chunk_cache[coord] = chunk
            chunk.enable()
            self.loaded_chunks[coord] = chunk

    def get_block(self, position: tuple[int, int, int]) -> BlockType | None:
        coord = self.world_to_chunk(position[0], position[2])
        chunk = self.loaded_chunks.get(coord)
        return chunk.get_block(position) if chunk else None

    def set_block(self, position: tuple[int, int, int], block_type: BlockType | None) -> bool:
        coord = self.world_to_chunk(position[0], position[2])
        chunk = self.loaded_chunks.get(coord)
        if not chunk:
            return False
        chunk.set_block(position, block_type)
        self._rebuild_adjacent_if_border(coord, position)
        return True

    def _rebuild_adjacent_if_border(self, coord: ChunkCoord, position: tuple[int, int, int]) -> None:
        local_x = position[0] - coord.x * CHUNK_SIZE
        local_z = position[2] - coord.z * CHUNK_SIZE

        neighbors: list[ChunkCoord] = []
        if local_x == 0:
            neighbors.append(ChunkCoord(coord.x - 1, coord.z))
        if local_x == CHUNK_SIZE - 1:
            neighbors.append(ChunkCoord(coord.x + 1, coord.z))
        if local_z == 0:
            neighbors.append(ChunkCoord(coord.x, coord.z - 1))
        if local_z == CHUNK_SIZE - 1:
            neighbors.append(ChunkCoord(coord.x, coord.z + 1))

        for neighbor_coord in neighbors:
            neighbor = self.loaded_chunks.get(neighbor_coord)
            if neighbor:
                neighbor.rebuild_mesh()
