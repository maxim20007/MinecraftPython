"""Entry point for the playable Minecraft-like prototype."""

import random

from ursina import (
    AmbientLight,
    DirectionalLight,
    Entity,
    Text,
    Ursina,
    Vec3,
    color,
    raycast,
    time,
    window,
    application,
)
from ursina.prefabs.sky import Sky

from player.controller import create_player
from settings import (
    AMBIENT_LIGHT_COLOR,
    BLOCK_OUTLINE_COLOR,
    CHUNK_SIZE,
    CHUNK_UPDATE_INTERVAL,
    PLAYER_SPAWN_HEIGHT_OFFSET,
    REACH_DISTANCE,
    SKY_COLOR,
    SUNLIGHT_COLOR,
    SUNLIGHT_DIRECTION,
)
from world.blocks import HOTBAR_ORDER
from world.generator import surface_height
from world.world_manager import WorldManager


class Game(Entity):
    def __init__(self, seed: int):
        super().__init__()
        self.seed = seed
        self.world = WorldManager(seed=seed)

        spawn = self._choose_spawn()
        self.player = create_player(spawn)
        self.world.ensure_chunks_around(self.player.position)

        self.selected_block_type = HOTBAR_ORDER[0]
        self._chunk_update_timer = 0.0
        self.target_position: tuple[int, int, int] | None = None

        self.block_outline = Entity(
            model="cube",
            color=BLOCK_OUTLINE_COLOR,
            wireframe=True,
            scale=1.01,
            enabled=False,
            unlit=True,
        )

        self.hotbar_text = Text(
            text="",
            position=(-0.86, 0.45),
            color=color.white,
            scale=1.1,
            origin=(0, 0),
        )
        self._update_hotbar_text()

    def _choose_spawn(self) -> tuple[float, float, float]:
        center = CHUNK_SIZE // 2
        y = surface_height(center, center, self.seed) + PLAYER_SPAWN_HEIGHT_OFFSET
        return (center, y, center)

    def _update_hotbar_text(self) -> None:
        lines = ["Блоки: 1-трава, 2-камень, 3-бедрок"]
        lines.append(f"Выбран: {self.selected_block_type}")
        lines.append("ЛКМ: сломать | ПКМ: поставить")
        self.hotbar_text.text = "\n".join(lines)

    def update(self) -> None:
        self._chunk_update_timer += time.dt
        if self._chunk_update_timer >= CHUNK_UPDATE_INTERVAL:
            self.world.ensure_chunks_around(self.player.position)
            self._chunk_update_timer = 0.0

        self._update_target_block()

    def _update_target_block(self) -> None:
        hit = raycast(
            origin=self.player.camera_pivot.world_position,
            direction=self.player.camera_pivot.forward,
            distance=REACH_DISTANCE,
            ignore=(self.player,),
        )

        if hit.hit and hit.entity and hit.entity.collider:
            x = int(round(hit.world_point.x - hit.normal.x * 0.5))
            y = int(round(hit.world_point.y - hit.normal.y * 0.5))
            z = int(round(hit.world_point.z - hit.normal.z * 0.5))
            position = (x, y, z)
            if self.world.get_block(position):
                self.target_position = position
                self.block_outline.enabled = True
                self.block_outline.position = Vec3(*position) + Vec3(0.5, 0.5, 0.5)
                return

        self.target_position = None
        self.block_outline.enabled = False

    def input(self, key: str) -> None:
        if key in ("1", "2", "3"):
            self.selected_block_type = HOTBAR_ORDER[int(key) - 1]
            self._update_hotbar_text()

        if key == "left mouse down" and self.target_position:
            self.world.set_block(self.target_position, None)

        if key == "right mouse down" and self.target_position:
            hit = raycast(
                origin=self.player.camera_pivot.world_position,
                direction=self.player.camera_pivot.forward,
                distance=REACH_DISTANCE,
                ignore=(self.player,),
            )
            if hit.hit:
                place_pos = (
                    int(round(hit.world_point.x + hit.normal.x * 0.5)),
                    int(round(hit.world_point.y + hit.normal.y * 0.5)),
                    int(round(hit.world_point.z + hit.normal.z * 0.5)),
                )
                if place_pos[1] > 0:
                    self.world.set_block(place_pos, self.selected_block_type)

        if key == "scroll up":
            current = HOTBAR_ORDER.index(self.selected_block_type)
            self.selected_block_type = HOTBAR_ORDER[(current + 1) % len(HOTBAR_ORDER)]
            self._update_hotbar_text()

        if key == "scroll down":
            current = HOTBAR_ORDER.index(self.selected_block_type)
            self.selected_block_type = HOTBAR_ORDER[(current - 1) % len(HOTBAR_ORDER)]
            self._update_hotbar_text()

        if key == "escape":
            application.quit()


def setup_lighting() -> None:
    AmbientLight(color=AMBIENT_LIGHT_COLOR)
    sun = DirectionalLight(color=SUNLIGHT_COLOR)
    sun.look_at(Vec3(*SUNLIGHT_DIRECTION))


def main() -> None:
    app = Ursina(title="Minecraft Python")

    window.color = SKY_COLOR
    window.exit_button.visible = False
    window.fps_counter.enabled = True

    Sky()
    setup_lighting()

    seed = random.randint(0, 10_000_000)
    _game = Game(seed)

    app.run()


if __name__ == "__main__":
    main()
