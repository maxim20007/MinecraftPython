"""Block definitions, colors and textures."""

from enum import StrEnum

from ursina import color

from settings import DEFAULT_BLOCK_TEXTURE


class BlockType(StrEnum):
    GRASS = "grass"
    STONE = "stone"
    BEDROCK = "bedrock"


BLOCK_COLORS = {
    BlockType.GRASS: color.rgb(80, 180, 80),
    BlockType.STONE: color.rgb(130, 130, 130),
    BlockType.BEDROCK: color.rgb(20, 20, 20),
}

# Пока одна текстура для всех блоков. Можно заменить файлами в assets/textures/blocks.
texture_path = str(DEFAULT_BLOCK_TEXTURE) if DEFAULT_BLOCK_TEXTURE.exists() else 'white_cube'

BLOCK_TEXTURES = {
    BlockType.GRASS: texture_path,
    BlockType.STONE: texture_path,
    BlockType.BEDROCK: texture_path,
}

HOTBAR_ORDER = [BlockType.GRASS, BlockType.STONE, BlockType.BEDROCK]
