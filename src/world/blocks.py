"""Block definitions and colors."""

from enum import StrEnum

from ursina import color


class BlockType(StrEnum):
    GRASS = "grass"
    STONE = "stone"
    BEDROCK = "bedrock"


BLOCK_COLORS = {
    BlockType.GRASS: color.lime,
    BlockType.STONE: color.gray,
    BlockType.BEDROCK: color.black,
}
