"""Block definitions and colors."""

from enum import StrEnum

from ursina import color


class BlockType(StrEnum):
    GRASS = "grass"
    STONE = "stone"
    BEDROCK = "bedrock"


BLOCK_COLORS = {
    BlockType.GRASS: color.rgb(80, 180, 80),
    BlockType.STONE: color.rgb(130, 130, 130),
    BlockType.BEDROCK: color.rgb(20, 20, 20),
}
