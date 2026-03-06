"""Block definitions, default colors and optional textures."""

from enum import StrEnum

from ursina import color

from settings import DEFAULT_BLOCK_TEXTURE


class BlockType(StrEnum):
    GRASS = "grass"
    STONE = "stone"
    BEDROCK = "bedrock"


# Разные цвета по умолчанию (даже без текстур).
BLOCK_COLORS = {
    BlockType.GRASS: color.rgb(80, 180, 80),
    BlockType.STONE: color.rgb(130, 130, 130),
    BlockType.BEDROCK: color.rgb(20, 20, 20),
}

# Текстуры опциональны: если файл отсутствует, рендерим чистыми цветами.
DEFAULT_TEXTURE_PATH = str(DEFAULT_BLOCK_TEXTURE) if DEFAULT_BLOCK_TEXTURE.exists() else None

BLOCK_TEXTURES: dict[BlockType, str | None] = {
    BlockType.GRASS: DEFAULT_TEXTURE_PATH,
    BlockType.STONE: DEFAULT_TEXTURE_PATH,
    BlockType.BEDROCK: DEFAULT_TEXTURE_PATH,
}

HOTBAR_ORDER = [BlockType.GRASS, BlockType.STONE, BlockType.BEDROCK]
