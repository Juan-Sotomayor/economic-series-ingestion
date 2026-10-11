from typing import Protocol

from src.domain.entities import Observation


class ObservationRepository(Protocol):
    def save_all(
        self, observations: list[Observation]
    ) -> None:
        ...