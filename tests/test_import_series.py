from datetime import date
from decimal import Decimal

from src.domain.entities import Observation
from src.application.use_cases.import_series import ImportEconomicSeries


class FakeProvider:
    def __init__(self, observations):
        self.observations = observations

    def get_observations(self, series_id):
        return self.observations


class InMemoryRepository:
    def __init__(self):
        self.items = []

    def save_all(self, observations):
        self.items.extend(observations)


def test_importa_observacoes():
    observation = Observation(
        series_id="11",
        date=date(2026, 9, 28),
        value=Decimal("0.050788"),
    )

    repository = InMemoryRepository()

    use_case = ImportEconomicSeries(
        provider=FakeProvider([observation]),
        repository=repository,
    )

    quantidade = use_case.execute("11")

    assert quantidade == 1
    assert repository.items == [observation]


def test_importacao_sem_registros():
    repository = InMemoryRepository()

    use_case = ImportEconomicSeries(
        provider=FakeProvider([]),
        repository=repository,
    )

    quantidade = use_case.execute("11")

    assert quantidade == 0
    assert repository.items == []