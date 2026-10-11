from typing import Protocol

from src.domain.entities import Observation


class DataProvider(Protocol):
    def get_observations(
        self, series_id: str
    ) -> list[Observation]:
        ...