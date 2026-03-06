"""Procedural terrain generation."""

import math
import random

from settings import (
    BASE_HEIGHT,
    NOISE_LACUNARITY,
    NOISE_OCTAVES,
    NOISE_PERSISTENCE,
    NOISE_SCALE,
    TERRAIN_HEIGHT,
    WORLD_HEIGHT,
)


def _hash_noise(x: int, z: int, seed: int) -> float:
    rng = random.Random((x * 73856093) ^ (z * 19349663) ^ seed)
    return rng.uniform(-1.0, 1.0)


def _smoothstep(t: float) -> float:
    return t * t * (3.0 - 2.0 * t)


def _value_noise(x: float, z: float, seed: int) -> float:
    x0 = math.floor(x)
    z0 = math.floor(z)
    x1 = x0 + 1
    z1 = z0 + 1

    tx = _smoothstep(x - x0)
    tz = _smoothstep(z - z0)

    n00 = _hash_noise(x0, z0, seed)
    n10 = _hash_noise(x1, z0, seed)
    n01 = _hash_noise(x0, z1, seed)
    n11 = _hash_noise(x1, z1, seed)

    ix0 = n00 + (n10 - n00) * tx
    ix1 = n01 + (n11 - n01) * tx
    return ix0 + (ix1 - ix0) * tz


def fractal_noise(x: int, z: int, seed: int) -> float:
    value = 0.0
    amplitude = 1.0
    frequency = 1.0
    normalizer = 0.0

    for octave in range(NOISE_OCTAVES):
        sample_x = (x / NOISE_SCALE) * frequency
        sample_z = (z / NOISE_SCALE) * frequency
        octave_seed = seed + octave * 10_000
        value += _value_noise(sample_x, sample_z, octave_seed) * amplitude
        normalizer += amplitude
        amplitude *= NOISE_PERSISTENCE
        frequency *= NOISE_LACUNARITY

    return value / normalizer if normalizer else 0.0


def surface_height(x: int, z: int, seed: int) -> int:
    """Return terrain surface height for world coordinate (x, z)."""
    normalized = (fractal_noise(x, z, seed) + 1.0) * 0.5
    height = BASE_HEIGHT + int(normalized * TERRAIN_HEIGHT)
    return max(1, min(WORLD_HEIGHT - 2, height))
