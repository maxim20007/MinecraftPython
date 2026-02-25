"""Block definitions and colors."""

from enum import StrEnum

from settings import rgb255


class BlockType(StrEnum):
    GRASS = "grass"
    STONE = "stone"
    BEDROCK = "bedrock"


BLOCK_COLORS = {
    BlockType.GRASS: rgb255(80, 180, 80),
    BlockType.STONE: rgb255(130, 130, 130),
    BlockType.BEDROCK: rgb255(20, 20, 20),
}
