from typing import Any, Dict, Tuple

import numpy as np

from mapgen import Dungeon


class ModifiedDungeon(Dungeon):
    reward_types = ["basic", "reward_new_cell", "reward_new_explored"]

    def __init__(self, width: int = 20, height: int = 20,
                 max_rooms: int = 3, min_room_xy: int = 5,
                 max_room_xy: int = 10, observation_size: int = 11,
                 vision_radius: int = 5, max_steps: int = 2000,
                 reward_type: str = "basic"):
        super().__init__(width=width, height=height, max_rooms=max_rooms,
                         min_room_xy=min_room_xy, max_room_xy=max_room_xy,
                         vision_radius=vision_radius, max_steps=max_steps,
                         observation_size=observation_size)

        if reward_type not in self.reward_types:
            raise NotImplementedError(f"Such a reward has not been realized! "
                                      f"Available options: {self.reward_types}")
        self.reward_type = reward_type

    @staticmethod
    def _reward_new_cell(info: Dict[str, Any]) -> float:
        """
        Модифицировання награда.
        Награждаем агента за исследование новых клеток.
        При этом награду за исследование даем только тогда,
        когда он проходит по новым клеткам.
        Мотивация: хотим, чтобы агент научился исследовать
        помещение, при этом повторно не проходить по клеткам.
        """
        if info["moved"]:
            if info["is_new"]:
                return 0.1 + 20 * info["total_explored"] / info["total_cells"]
            return -0.5
        return -1.0

    @staticmethod
    def _reward_new_explored(info: Dict[str, Any]) -> float:
        """
        Пример модифицированной награды (слайд 21).
        Мотивируем агента как можно быстрее изучить все помещение.
        """
        if info["moved"]:
            if info["new_explored"] > 0:
                return 0.1 + 20 * info["total_explored"] / info["total_cells"]
            return -0.5
        return -1.0

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, Dict[str, Any]]:
        observation, reward, done, info = super().step(action)

        if self.reward_type == "basic":
            return observation, reward, done, info
        elif self.reward_type == "reward_new_cell":
            return observation, self._reward_new_cell(info), done, info
        elif self.reward_type == "reward_new_explored":
            return observation, self._reward_new_explored(info), done, info
