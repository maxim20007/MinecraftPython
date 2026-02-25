"""Procedural terrain generation for first iteration."""

import random

from settings import BASE_HEIGHT, HEIGHT_VARIATION, WORLD_HEIGHT


def surface_height(x: int, z: int, seed: int) -> int:
    """Return a random surface height for world coordinate (x, z)."""
    rng = random.Random((x * 73856093) ^ (z * 19349663) ^ seed)
    height = BASE_HEIGHT + rng.randint(-HEIGHT_VARIATION, HEIGHT_VARIATION)
    return max(1, min(WORLD_HEIGHT - 1, height))
